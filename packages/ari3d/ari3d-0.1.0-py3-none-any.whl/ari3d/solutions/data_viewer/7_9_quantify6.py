import os
import time
from pathlib import Path

import altair as alt
import anndata
import numpy as np
import pandas as pd
import yaml
from joblib import Parallel, delayed
from scipy.signal import find_peaks, savgol_filter
from tqdm import tqdm

############################### IO #################################


def create_path_recursively(path):
    """Creates a path. Creates missing parent folders."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    return True


def write_dict_to_yml(yml_file, d):
    """Writes a dictionary to a file in yml format."""
    yml_file = Path(yml_file)
    create_path_recursively(yml_file.parent)

    with open(yml_file, "w+") as yml_f:
        yml_f.write(yaml.dump(d, Dumper=yaml.Dumper))

    return True


def get_dict_from_yml(yml_file):
    """Reads a dictionary from a file in yml format."""
    with open(yml_file) as yml_f:
        d = yaml.safe_load(yml_f)

    if not isinstance(d, dict):
        raise TypeError("Yaml file %s invalid!" % str(yml_file))

    return d


def _load_ann_data(path, message):
    try:
        adata = anndata.read_h5ad(path, backed="r")
        with tqdm(total=100, desc="Converting to DataFrame") as pbar_convert:
            df = adata.to_df()
            pbar_convert.update(100)
        df.columns = [
            int("".join(filter(str.isdigit, col)))
            if any(char.isdigit() for char in col)
            else np.nan
            for col in df.columns
        ]
        df.index = df.index.astype(int)
        print(message)
        return df
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")
    return df


def directory():
    path = askdirectory(title="select folder with data")  ## folder 'data'
    return path


def load_histograms(path_bulk_histogram):
    """Load the bulk histograms from the h5ad file and convert it to a DataFrame."""
    print("path histograms:", path_bulk_histogram)
    histogram_ds = _load_ann_data(
        path_bulk_histogram, "h5ad bulk converted to DataFrame successfully."
    )
    initial_bins = len(histogram_ds.columns)

    return histogram_ds, initial_bins


def load_properties(path):
    """Load the properties from the csv file and convert it to a DataFrame."""
    path_and_name = os.path.join(path, "Properties.csv")
    properties_data = pd.read_csv(path_and_name, encoding="unicode_escape")
    return properties_data


def load_in_volume(_path_load_inner_histograms):
    """Load the Inner histograms from the h5ad file and convert it to a DataFrame."""
    return _load_ann_data(
        _path_load_inner_histograms,
        "h5ad inner histogram converted to DataFrame successfully.",
    )


def load_out_volume(_path_load_outer_histograms):
    """Load the Outer histograms from the h5ad file and convert it to a DataFrame."""
    return _load_ann_data(
        _path_load_outer_histograms,
        "h5ad outer histogram converted to DataFrame successfully.",
    )


def load_mesh(_path_load_surface_mesh_histograms):
    """Load the Mesh data from the h5ad file and convert it to a DataFrame."""
    return _load_ann_data(
        _path_load_surface_mesh_histograms,
        "h5ad Surface mesh converted to DataFrame successfully.",
    )


def load_gradient(path_load_gradient):
    """Load the gradient from the csv file and convert it to a DataFrame."""
    gradient = pd.read_csv(path_load_gradient)
    gradient.index = gradient["label"]
    return gradient


def create_histogram_subdata(n, histograms_data, particle_x=0):
    """Create a Sub-dataset for of the histogram data."""
    labels_array = np.array(histograms_data.index)
    labels_array = labels_array[labels_array > 0]
    random_labels = np.random.choice(labels_array, n, replace=False)
    if (
        particle_x > 0
    ):  # add a specific Region to the random dataset. Be sure the label exists
        random_labels = np.append(random_labels, particle_x)

    random_labels = np.sort(random_labels)
    random_labels = pd.DataFrame(random_labels, columns=["Label Index"])

    # get histogram data of chosen labels
    hist_sub_data = histograms_data[
        histograms_data.index.isin(random_labels["Label Index"])
    ]

    return hist_sub_data, random_labels


def load_label_list(data_directory):
    """Load the label List csv containing the label (particle) Indices of interest."""
    path_label_list = os.path.join(data_directory, "labelList.csv")
    label_list = pd.read_csv(path_label_list)
    label_indices = label_list["Label Index"]
    sub_data_from_list = histogramsData[histogramsData.index.isin(label_indices)]

    # show head of list
    label_list.head()

    return sub_data_from_list, label_indices


def process_histogram_row(row, array, binning):
    # allows to input images with any binnig. This function is parallelized and used in the binning.
    num = row.to_numpy()
    num = np.pad(num, (0, 1), "constant")
    num = num.ravel()
    # Define bins and digitization
    rang = int(round(len(num) / binning))
    bins = np.linspace(0, max(array) + 1, rang)
    full_range = np.linspace(0, max(array), len(array) + 1)
    digitized = np.digitize(full_range, bins)
    # Calculate bin sums
    bin_sum = [num[digitized == i].sum() for i in range(1, len(bins))]
    bin_sum = np.array(bin_sum)
    row1 = bin_sum[bin_sum > 0]
    bin_sum[bin_sum > 0] = row1
    yhat = row1
    bin_sum = [num[digitized == i].sum() for i in range(1, len(bins))]
    bin_sum = np.array(bin_sum)
    bin_sum[bin_sum > 0] = yhat
    result1 = bin_sum
    return result1


def binning(bin_input, histograms_data, n_jobs=-1):
    histograms_data_int = np.array(histograms_data.columns).astype(int)
    # Parallel processing
    binned_hist_list = Parallel(n_jobs=n_jobs)(
        delayed(process_histogram_row)(row, histograms_data_int, bin_input)
        for _, row in tqdm(
            histograms_data.iterrows(),
            total=histograms_data.shape[0],
            desc="Processing Rows",
        )
    )
    # Convert lists to DataFrames
    rang = int(round(len(histograms_data.columns) / bin_input))
    bin_ranges = np.linspace(0, len(histograms_data.columns) - 1, rang - 1).astype(int)
    binned_hist_list = np.array(binned_hist_list).reshape(len(binned_hist_list), -1)

    # convert binned histogram do dataset with columns as lower bin range
    binned_hist_list = pd.DataFrame(binned_hist_list, columns=bin_ranges)
    binned_hist_list.index = histograms_data.index

    binned_hist_list[binned_hist_list < 0] = 0
    return binned_hist_list


def normalize_volume(un_normalized):
    un_normalized = pd.DataFrame(un_normalized)
    df_new = un_normalized.loc[:, :].div(un_normalized.sum(axis=1), axis=0)
    df_new = df_new.fillna(0)
    return df_new


def transform_columns_xy(sub_data_ready):
    # transpose dataset
    x = sub_data_ready.transpose()
    # build array as long as particles are available, repeat the index
    bin_indices = np.tile(x.index, len(x.columns))
    # build array with particle names
    name_particles = (
        np.array([np.array([c] * len(x)) for c in x.columns])
        .transpose()
        .flatten(order="F")
    )
    # flatten frequencies of each particle
    frequencies = (
        np.array([np.array(x[f]) for f in x.columns]).transpose().flatten(order="F")
    )

    # build and return dataframe
    return pd.DataFrame(
        {"X": name_particles, "Y": bin_indices, "frequency": frequencies}
    )


def smooth_histograms_savgol(binned_histograms, savgol_window_length, n_jobs=-1):
    smoothed_histogram = Parallel(n_jobs=n_jobs)(
        delayed(
            lambda row: savgol_filter(
                row, window_length=savgol_window_length, polyorder=3
            )
        )(row)
        for _, row in tqdm(
            binned_histograms.iterrows(),
            total=binned_histograms.shape[0],
            desc="Smoothing Rows",
        )
    )

    # convert to data frame
    smoothed_histogram_ds = pd.DataFrame(
        smoothed_histogram,
        columns=binned_histograms.columns,
        index=binned_histograms.index,
    )

    # Clip negative values to 0
    smoothed_histogram_ds[smoothed_histogram_ds < 0] = 0

    # Ensure integer values if required
    smoothed_histogram_ds = smoothed_histogram_ds.astype(int)

    return smoothed_histogram_ds


def process_peaks(
    normalized_data,
    histograms_data,
    properties,
    number_bins,
    peak_width,
    peak_height,
    peak_prominence,
    peak_vertical_distance,
    peak_horizontal_distance,
    num_bins_input,
):
    # binned but maintaining the range, e.g.16bit to 8bit: 256 bins between 0-65535 (0, 256,512,768...)
    normalized_data = pd.DataFrame(normalized_data)
    peaks_position = []
    peaks_height = []

    # iterate over the particles
    for index, row in tqdm(
        normalized_data.iterrows(),
        total=normalized_data.shape[0],
        desc="Processing Peaks",
    ):
        # flatten the row
        row_flatten = np.array(row).ravel()

        # convert to float and pad the array to start from 0
        row_flatten = row_flatten.astype(float)
        row_flatten = np.pad(row_flatten, (0, 1), constant_values=0)

        # grey scale intensity range
        grey_scale = np.array(histograms_data.columns, dtype=float)
        grey_scale = np.pad(grey_scale, (0, 1), constant_values=0)
        grey_scale = grey_scale.astype(int)

        # replace NaN values with 0 and negative values with 0
        row_flatten[np.isnan(row_flatten)] = 0
        row_flatten[row_flatten < 0] = 0

        # Find peaks
        peaks_scipy = find_peaks(
            row_flatten,
            rel_height=0.5,
            width=peak_width,
            height=peak_height,
            prominence=peak_prominence,
            threshold=peak_vertical_distance,
            distance=peak_horizontal_distance,
        )
        # calculate the bin value of the peak
        peak_pos = grey_scale[peaks_scipy[0]]
        peak_pos = peak_pos * num_bins_input

        # append peak positions and heights to lists
        peaks_position.append([peak_pos])
        peaks_height.append([peaks_scipy[1]["peak_heights"]])

    # convert lists to DataFrames
    peaks_positions = pd.DataFrame(peaks_position)
    peaks_height = pd.DataFrame(peaks_height)

    # flatten rows and rename columns
    peaks_positions = pd.concat([peaks_positions[0].str[i] for i in range(22)], axis=1)
    peaks_height = pd.concat([peaks_height[0].str[i] for i in range(22)], axis=1)
    peaks_positions.columns = [f"Peak_{i + 1}" for i in range(22)]
    peaks_height.columns = [f"Peaks_Height_{i + 1}" for i in range(22)]

    # fill NaN values with 0
    peaks_positions = peaks_positions.fillna(0)
    peaks_height = peaks_height.fillna(0)

    # merge to a single DataFrame
    peaks = pd.concat([peaks_positions, peaks_height], axis=1)

    # apply indexing from the normalized data
    peaks.index = normalized_data.index

    # locate properties based on the normalized data index
    properties = properties.loc[normalized_data.index]

    # combine properties with peaks
    peaks = pd.concat([peaks, properties], axis=1)

    # save binning value
    peaks["Binning"] = number_bins

    # replace NaN values with 0, inf with 0, and -inf with 0, typecast to float
    peaks = peaks.astype(float)
    peaks.replace([np.inf, -np.inf], 0, inplace=True)
    peaks.replace([np.nan], 0, inplace=True)

    return peaks


def _process_phase(
    peaks1,
    peaks_height_cols,
    peaks_col,
    phase_start,
    phase_end,
    phase_label,
    background_peak,
):
    # Apply thresholds, set np.nan for values outside the phase range
    peaks_filtered = peaks_col.where(
        (peaks_col >= phase_start) & (peaks_col < phase_end), np.nan
    )

    # get the peak height
    peaks_height = peaks1[peaks_height_cols]

    # Filter out rows with all NaN values, fill NaN values with 0
    peaks_filtered = peaks_filtered.loc[peaks_filtered.any(axis=1), :].fillna(0)

    # merge the filtered peaks with their peak heights
    peaks_filtered = peaks_filtered.merge(
        peaks_height, left_index=True, right_index=True
    )

    # Adjust peak positions and heights
    for i in range(1, 23):
        # remove negative values
        peaks_filtered[f"Peak_{i}"] = peaks_filtered[f"Peak_{i}"].clip(lower=0)

        # set all Peaks_Height values to 0 if the corresponding Peak value is outside the phase range
        peaks_filtered[f"Peaks_Height_{i}"] = (
            peaks_filtered[f"Peaks_Height_{i}"]
            .where(
                (peaks_filtered[f"Peak_{i}"] >= phase_start)
                & (peaks_filtered[f"Peak_{i}"] < phase_end),
                0,
            )
            .where(peaks_filtered[f"Peak_{i}"] >= background_peak, 0)
        )

    # check whether there exist rows where at least one peak is within the phase range
    if peaks_filtered[peaks_height_cols].notna().any().any():
        # Find the index of the maximum height peak for each row
        max_peak_idx = peaks_filtered[peaks_height_cols].idxmax(axis=1)
        # Initialize a new DataFrame with zeros
        peaks_data = pd.DataFrame(
            0,
            index=peaks_filtered.index,
            columns=[f"Peak_{phase_label}", f"Peaks_Height_{phase_label}"],
        )
        for i, col_name in enumerate(peaks_height_cols):
            mask = max_peak_idx == col_name
            # set the peak gray value and height for the row where the peak has the maximum height
            peaks_data[f"Peak_{phase_label}"] = np.where(
                mask, peaks_filtered[f"Peak_{i + 1}"], peaks_data[f"Peak_{phase_label}"]
            )
            peaks_data[f"Peaks_Height_{phase_label}"] = np.where(
                mask,
                peaks_filtered[col_name],
                peaks_data[f"Peaks_Height_{phase_label}"],
            )
    else:
        # Return an empty DataFrame if no valid peaks were found
        peaks_data = pd.DataFrame(
            0,
            index=peaks_col.index,
            columns=[f"Peak_{phase_label}", f"Peaks_Height_{phase_label}"],
        )
    return peaks_data


def arrange_peaks(
    peaks1,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    phase_5_threshold,
    background_peak,
    properties,
):
    # Define column names
    cols = [f"Peak_{i}" for i in range(1, 23)]
    peaks_height_cols = [f"Peaks_Height_{i}" for i in range(1, 23)]

    # Process each phase
    peaks_data_T1 = _process_phase(
        peaks1,
        peaks_height_cols,
        peaks1[cols],
        background_peak,
        phase_1_threshold,
        1,
        background_peak,
    )
    peaks_data_T2 = _process_phase(
        peaks1,
        peaks_height_cols,
        peaks1[cols],
        phase_1_threshold,
        phase_2_threshold,
        2,
        background_peak,
    )
    peaks_data_T3 = _process_phase(
        peaks1,
        peaks_height_cols,
        peaks1[cols],
        phase_2_threshold,
        phase_3_threshold,
        3,
        background_peak,
    )
    peaks_data_T4 = _process_phase(
        peaks1,
        peaks_height_cols,
        peaks1[cols],
        phase_3_threshold,
        phase_4_threshold,
        4,
        background_peak,
    )
    peaks_data_T5 = _process_phase(
        peaks1,
        peaks_height_cols,
        peaks1[cols],
        phase_4_threshold,
        phase_5_threshold,
        5,
        background_peak,
    )
    peaks_data_T6 = _process_phase(
        peaks1,
        peaks_height_cols,
        peaks1[cols],
        phase_5_threshold,
        np.inf,
        6,
        background_peak,
    )

    # Merge all phase data
    all_peaks_data = [
        peaks_data_T1,
        peaks_data_T2,
        peaks_data_T3,
        peaks_data_T4,
        peaks_data_T5,
        peaks_data_T6,
    ]
    non_empty_peaks_data = [df for df in all_peaks_data if not df.empty]

    if non_empty_peaks_data:
        peaks = pd.concat(non_empty_peaks_data, axis=1, join="outer")
    else:
        peaks = pd.DataFrame(
            index=peaks1.index,
            columns=[f"Peak_{i}" for i in range(1, 7)]
            + [f"Peaks_Height_{i}" for i in range(1, 7)],
        )

    # Fill NaN values with 0
    peaks = peaks.fillna(0)
    # replace peal position values less than background peak with background peak
    peaks[["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5", "Peak_6"]] = peaks[
        ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5", "Peak_6"]
    ].replace(0, background_peak)

    # Find the maximum peak value for each row, hence wich phase the peak belongs to
    peaks["Max_peak"] = peaks[
        ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5", "Peak_6"]
    ].max(axis=1)
    peaks = peaks.sort_values(by=["label"])

    # Combine with Properties
    properties_and_peaks = pd.concat([peaks, properties], axis=1)
    properties_and_peaks = properties_and_peaks.dropna()
    properties_and_peaks.replace([np.inf, -np.inf], 0, inplace=True)

    # remove all rows where the maximum peak is less or equal to the background peak
    properties_and_peaks = properties_and_peaks.drop(
        properties_and_peaks[properties_and_peaks.Max_peak <= background_peak].index
    )

    return properties_and_peaks


def _update_peak_positions(
    properties, background_peak, height_threshold, max_value=65535
):
    array = properties[["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]]
    # Fill NaN values with 0
    array = array.fillna(0)
    # Cap values at max_value
    array[array > max_value] = max_value
    for i in range(1, 5):  # Assuming there are 6 peaks (1 to 7)
        peak_position_col = f"Peak_{i}"
        peak_height_col = f"Peaks_Height_{i}"
        # set all peaks to background peak if the peak position is less than the background peak
        array[peak_position_col] = np.where(
            array[peak_position_col] < background_peak,
            background_peak,
            array[peak_position_col],
        )
        # set all peaks to background peak if the peak height is less than a given threshold
        array[peak_position_col] = np.where(
            properties[peak_height_col] < float(height_threshold),
            background_peak,
            array[peak_position_col],
        )
    return array


def quantify_liberated_regions(
    surface_mesh_subdata,
    subdata_properties,
    background_peak,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    regionsAnalysed,
    volumeAnalysed,
):
    #### only liberated regions
    Quantification_1_phases_append = []
    Index_1_phase = []
    Peaks_1_phase = []
    Quantification_Outer_phase_1_append = []
    Surface_quantification_append = []
    regionsLiberated = 0
    for i, (index, row) in enumerate(surface_mesh_subdata.iterrows()):
        # Getting the peaks values
        Peaks = subdata_properties.iloc[[i]].values
        # Condition that only 1 peak has value greater than background
        if np.count_nonzero(Peaks > background_peak) == 1:
            Partical_peak = Peaks[Peaks > background_peak].astype(int)[0]
            # Takes the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase = row.iloc[Partical_peak:65535].sum()
            # Getting sum of all volxels with greay value grater than peak grey  value
            Quantification_1_phases_append.append([Sum_phase])
            Index_1_phase.append(
                [index]
            )  ##########creates 2 lists, one with index and one with peak greyvalue
            Peaks_1_phase.append([Partical_peak])
            # linear equation from peak position to background. creates a list (then array) with each entry is the result of the equation  #todo: what euqation?
            multiples_towards_background_phase_1 = np.linspace(
                0, 1, Partical_peak - background_peak
            )
            No_of_voxels_towards_background_phase_1 = row.iloc[
                background_peak:Partical_peak
            ]
            if len(No_of_voxels_towards_background_phase_1) != len(
                multiples_towards_background_phase_1
            ):  # todo: unnecessary
                multiples_towards_background_phase_1 = (
                    multiples_towards_background_phase_1[
                        : len(No_of_voxels_towards_background_phase_1)
                    ]
                )

            Quantification_Outer_phase_1_array = (
                No_of_voxels_towards_background_phase_1
                * multiples_towards_background_phase_1
            ).sum()
            Quantification_Outer_phase_1_append.append(
                [Quantification_Outer_phase_1_array]
            )
            Surface_quantification_liberated = surface_mesh_subdata.iloc[
                i, background_peak:65535
            ].sum()
            Surface_quantification_append.append([Surface_quantification_liberated])
            regionsLiberated = (
                regionsLiberated + 1
            )  ######################################### ################################## to REPORT
            regionsAnalysed = (
                regionsAnalysed + 1
            )  ######################################### ################################# Pass to other functions
            volumeAnalysed = volumeAnalysed + Quantification_Outer_phase_1_array
    # Outher referes to bins lower grey value than the peak (affected by partial volume)
    Quantification_Outer_phase_1 = pd.DataFrame(
        Quantification_Outer_phase_1_append, columns=["Quantification_Outer_phase_1"]
    )
    Quantification_1_phases = pd.DataFrame(
        Quantification_1_phases_append, columns=["Quantification_phase_1"]
    )
    Surface_quantification = pd.DataFrame(
        Surface_quantification_append, columns=["Surface_quantification"]
    )
    Quantification_1_phases["total_quantification_phase_1"] = (
        Quantification_1_phases["Quantification_phase_1"]
        + Quantification_Outer_phase_1["Quantification_Outer_phase_1"]
    )
    Index_1_phase = pd.DataFrame(Index_1_phase, columns=["Label"])
    Peaks_1_phase = pd.DataFrame(Peaks_1_phase, columns=["Peak_1"])
    Quantification_1_phase_sorted = pd.DataFrame(index=Index_1_phase["Label"])
    # Define phase thresholds for categorizing peaks
    thresholds = [
        background_peak,
        phase_1_threshold,
        phase_2_threshold,
        phase_3_threshold,
        phase_4_threshold,
        Phase_5_threshold,
    ]
    # Loop over specified phases and assign values based on threshold conditions
    for i in range(1, 6):
        mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
            Peaks_1_phase["Peak_1"] <= thresholds[i]
        )
        Quantification_1_phase_sorted[f"Peak_{i}"] = np.where(
            mask, Peaks_1_phase["Peak_1"], 0
        )
        Quantification_1_phase_sorted[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_1_phases["total_quantification_phase_1"], 0
        )
        Quantification_1_phase_sorted[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_quantification["Surface_quantification"], 0
        )
    return (
        Quantification_1_phase_sorted,
        regionsLiberated,
        regionsAnalysed,
        volumeAnalysed,
    )


def quantify_two_phases_particle(
    InHistogram_Subdata,
    OutHistogram_Subdata,
    Gradient_Subdata,
    surface_mesh_subdata,
    array,
    background_peak_pos,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    regionsAnalysed,
    volumeAnalysed,
    background_peak,
    gradient_threshold=0.75,
):
    #### 2 Phases per region
    Quantification_all_2_phases_1 = []
    Quantification_all_2_phases_2 = []
    Quantification_out_of_peaks_phase_1 = []
    Quantification_out_of_peaks_phase_2 = []
    Surface_volume_phase_1_append = []
    Surface_volume_phase_2_append = []
    Quantification_Outer_phase_1 = []
    Quantification_Outer_phase_2 = []
    Peaks_1_phase = []
    Peaks_2_phase = []
    Index_2_phase = []
    i = 0
    regions2Phases = 0
    for (
        index,
        row,
    ) in (
        InHistogram_Subdata.iterrows()
    ):  # todo: check this - why InHistogram_Subdata is used here?
        Peaks = array.iloc[[i]].values
        if (np.count_nonzero(Peaks > background_peak_pos) == 2) and i > -1:
            Partical_peak = Peaks[Peaks > background_peak_pos]
            Partical_peak_1 = int((Partical_peak).flat[0])
            Partical_peak_1 = int(float(Partical_peak_1))
            Gradient_ratio = Gradient_Subdata["Gradient_3"].iloc[i]
            if Gradient_ratio < gradient_threshold:
                Gradient_ratio = gradient_threshold
            Sum_phase_1 = (
                InHistogram_Subdata.iloc[i, background_peak_pos:Partical_peak_1]
                .sum()
                .sum()
            )
            Partical_peak_2 = int((Partical_peak).flat[1])
            Partical_peak_2 = int(float(Partical_peak_2))
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_2 = InHistogram_Subdata.iloc[i, Partical_peak_2:].sum()
            # Appending the phase 1 quantification sum
            Quantification_all_2_phases_2.append([Sum_phase_2])
            Peaks_1_phase.append([Partical_peak_1])
            Peaks_2_phase.append([Partical_peak_2])
            # Creating a vector of linear equatin with which phase 2 transition towards phase 1 voxels will be multiplied
            No_of_voxels = InHistogram_Subdata.iloc[i, Partical_peak_1:Partical_peak_2]
            No_of_voxels = np.array(No_of_voxels)
            multiples_towards_Partical_peak_1 = np.arange(
                0, 1, 1 / ((Partical_peak_2) - Partical_peak_1)
            )
            multiples_towards_Partical_peak_1 = np.array(
                multiples_towards_Partical_peak_1
            )

            if len(multiples_towards_Partical_peak_1) > len(
                No_of_voxels
            ):  # todo: unnecessary?
                multiples_towards_Partical_peak_1 = np.delete(
                    multiples_towards_Partical_peak_1, 0
                )
            elif len(multiples_towards_Partical_peak_1) < len(
                No_of_voxels
            ):  # todo: unnecessary?
                multiples_towards_Partical_peak_1 = np.delete(
                    multiples_towards_Partical_peak_1, 0
                )
            else:
                multiples_towards_Partical_peak_1 = np.arange(
                    0, 1, 1 / ((Partical_peak_2) - Partical_peak_1)
                )

            multiples_towards_Partical_peak_2 = multiples_towards_Partical_peak_1[::-1]
            # Calculting the quantification of phase 2 towards phase 1 voxels
            out_of_peak_volume_2 = No_of_voxels * multiples_towards_Partical_peak_1
            out_of_peak_volume_1 = No_of_voxels * multiples_towards_Partical_peak_2
            # Appending the phase 1 quantification sum
            Quantification_all_2_phases_1.append([Sum_phase_1])
            out_of_peak_volume_1 = out_of_peak_volume_1.sum()
            Quantification_out_of_peaks_phase_1.append([out_of_peak_volume_1])
            out_of_peak_volume_2 = out_of_peak_volume_2.sum()
            Quantification_out_of_peaks_phase_2.append([out_of_peak_volume_2])
            Outer_volume_full_phase_2 = OutHistogram_Subdata.iloc[
                i, Partical_peak_2:
            ].sum()
            multiples_towards_background_phase_1 = np.arange(
                0, 1, 1 / ((Partical_peak_1 - 1) - background_peak_pos)
            )
            multiples_towards_background_phase_1 = np.array(
                multiples_towards_background_phase_1
            )

            if len(
                OutHistogram_Subdata.iloc[i, background_peak_pos:Partical_peak_1]
            ) == len(multiples_towards_background_phase_1):
                No_of_voxels_towards_background_phase_1 = OutHistogram_Subdata.iloc[
                    i, background_peak_pos:Partical_peak_1
                ]
            elif len(
                OutHistogram_Subdata.iloc[i, background_peak_pos:Partical_peak_1]
            ) > len(multiples_towards_background_phase_1):
                No_of_voxels_towards_background_phase_1 = OutHistogram_Subdata.iloc[
                    i, background_peak_pos : Partical_peak_1 - 1
                ]
            else:
                No_of_voxels_towards_background_phase_1 = OutHistogram_Subdata.iloc[
                    i, background_peak_pos : Partical_peak_1 + 1
                ]
            Quantification_Outer_phase_1_array = (
                No_of_voxels_towards_background_phase_1
                * multiples_towards_background_phase_1
            )
            multiples_towards_background_phase_2 = np.arange(
                0, 1, 1 / ((Partical_peak_2 - 1) - background_peak_pos)
            )
            multiples_towards_background_phase_2 = np.array(
                multiples_towards_background_phase_2
            )

            if len(
                OutHistogram_Subdata.iloc[i, background_peak_pos:Partical_peak_2]
            ) == len(multiples_towards_background_phase_2):
                No_of_voxels_towards_background_phase_2 = OutHistogram_Subdata.iloc[
                    i, background_peak_pos:Partical_peak_2
                ]
            elif len(
                OutHistogram_Subdata.iloc[i, background_peak_pos:Partical_peak_2]
            ) > len(multiples_towards_background_phase_2):
                No_of_voxels_towards_background_phase_2 = OutHistogram_Subdata.iloc[
                    i, background_peak_pos : Partical_peak_2 - 1
                ]
            else:
                No_of_voxels_towards_background_phase_2 = OutHistogram_Subdata.iloc[
                    i, background_peak_pos : Partical_peak_2 + 1
                ]
            Quantification_Outer_phase_2_array = (
                No_of_voxels_towards_background_phase_2
                * multiples_towards_background_phase_2
            )
            Vol_to_subtract_from_phase_1 = Quantification_Outer_phase_2_array[
                background_peak_pos:Partical_peak_1
            ]
            Vol_to_subtract_from_phase_1 = Vol_to_subtract_from_phase_1.sum()
            Quantification_Outer_phase_2_array = (
                Quantification_Outer_phase_2_array.sum() - Vol_to_subtract_from_phase_1
            )
            Quantification_Outer_phase_1_array = (
                Quantification_Outer_phase_1_array.sum()
            )
            PVE_adjusted_volume = (
                Outer_volume_full_phase_2
                + Quantification_Outer_phase_1_array
                + Quantification_Outer_phase_2_array
            )

            if Partical_peak_1 < phase_1_threshold:
                Phase_limit = phase_1_threshold
            elif phase_1_threshold <= Partical_peak_1 < phase_2_threshold:
                Phase_limit = phase_2_threshold
            elif phase_2_threshold <= Partical_peak_1 < phase_3_threshold:
                Phase_limit = phase_3_threshold
            elif phase_3_threshold <= Partical_peak_1 < phase_4_threshold:
                Phase_limit = phase_4_threshold

            Surface_ratio = (
                surface_mesh_subdata.iloc[
                    i, background_peak_pos : int(Gradient_ratio * Phase_limit)
                ].sum()
            ) / (surface_mesh_subdata.iloc[i, background_peak_pos:].sum())
            Phase_1_surface_volume = (
                surface_mesh_subdata.iloc[i, background_peak_pos:65535].sum()
                * Surface_ratio
            )
            Phase_2_surface_volume = (
                surface_mesh_subdata.iloc[i, background_peak_pos:65535].sum()
                - Phase_1_surface_volume
            )
            Surface_volume_phase_1_append.append([Phase_1_surface_volume])
            Surface_volume_phase_2_append.append([Phase_2_surface_volume])
            Quantification_Outer_phase_1_volume = Surface_ratio * PVE_adjusted_volume
            Quantification_Outer_phase_2_volume = (
                PVE_adjusted_volume - Quantification_Outer_phase_1_volume
            )
            Quantification_Outer_phase_1.append([Quantification_Outer_phase_1_volume])
            Quantification_Outer_phase_2.append([Quantification_Outer_phase_2_volume])
            Index_2_phase.append([index])
            regions2Phases = (
                regions2Phases + 1
            )  ############################################################################## to REPORT
            regionsAnalysed = (
                regionsAnalysed + 1
            )  ############################################################################ Pass to other functions
            volumeAnalysed = (
                volumeAnalysed
                + Sum_phase_1
                + Sum_phase_2
                + out_of_peak_volume_1
                + out_of_peak_volume_2
                + Quantification_Outer_phase_1_volume
                + Quantification_Outer_phase_2_volume
            )
        i = i + 1
    Index_2_phase = pd.DataFrame(Index_2_phase, columns=["Label"])
    Surface_volume_phase_1 = pd.DataFrame(
        Surface_volume_phase_1_append, columns=["Surface_volume_phase_1"]
    )
    Surface_volume_phase_1.index = Index_2_phase["Label"]
    Surface_volume_phase_2 = pd.DataFrame(
        Surface_volume_phase_2_append, columns=["Surface_volume_phase_2"]
    )
    Surface_volume_phase_2.index = Index_2_phase["Label"]
    Quantification_all_2_phases_1 = pd.DataFrame(
        Quantification_all_2_phases_1, columns=["Phase_1_quantification_outer"]
    )
    Quantification_all_2_phases_1.index = Index_2_phase["Label"]
    Quantification_all_2_phases_2 = pd.DataFrame(
        Quantification_all_2_phases_2, columns=["Phase_2_quantification_outer"]
    )
    Quantification_all_2_phases_2.index = Index_2_phase["Label"]
    Quantification_out_of_peaks_1 = pd.DataFrame(
        Quantification_out_of_peaks_phase_1,
        columns=["Quantification_out_of_peaks_1_outer"],
    )
    Quantification_out_of_peaks_1 = Quantification_out_of_peaks_1.fillna(0)
    Quantification_out_of_peaks_1.index = Index_2_phase["Label"]
    Quantification_out_of_peaks_2 = pd.DataFrame(
        Quantification_out_of_peaks_phase_2,
        columns=["Quantification_out_of_peaks_2_outer"],
    )
    Quantification_out_of_peaks_2 = Quantification_out_of_peaks_2.fillna(0)
    Quantification_out_of_peaks_2.index = Index_2_phase["Label"]
    Quantification_Outer_phase_1 = pd.DataFrame(
        Quantification_Outer_phase_1, columns=["Quantification_Outer_phase_1"]
    )
    Quantification_Outer_phase_1 = Quantification_Outer_phase_1.fillna(0)
    Quantification_Outer_phase_1.index = Index_2_phase["Label"]
    Quantification_Outer_phase_2 = pd.DataFrame(
        Quantification_Outer_phase_2, columns=["Quantification_Outer_phase_2"]
    )
    Quantification_Outer_phase_2 = Quantification_Outer_phase_2.fillna(0)
    Quantification_Outer_phase_2.index = Index_2_phase["Label"]

    Peaks_1_phase = pd.DataFrame(Peaks_1_phase, columns=["Peak_1"])
    Peaks_1_phase.index = Index_2_phase["Label"]
    Peaks_2_phase = pd.DataFrame(Peaks_2_phase, columns=["Peak_2"])
    Peaks_2_phase.index = Index_2_phase["Label"]

    Quantification_2_phases_inner = pd.concat(
        [
            Peaks_1_phase,
            Peaks_2_phase,
            Quantification_all_2_phases_1,
            Quantification_all_2_phases_2,
            Quantification_out_of_peaks_1,
            Quantification_out_of_peaks_2,
        ],
        axis=1,
    )
    Quantification_2_phases_inner["Phase_1_inner_quantification"] = (
        Quantification_2_phases_inner["Phase_1_quantification_outer"]
        + Quantification_2_phases_inner["Quantification_out_of_peaks_1_outer"]
    )
    Quantification_2_phases_inner["Phase_2_inner_quantification"] = (
        Quantification_2_phases_inner["Phase_2_quantification_outer"]
        + Quantification_2_phases_inner["Quantification_out_of_peaks_2_outer"]
    )
    Quantification_2_phases_inner = Quantification_2_phases_inner[
        [
            "Peak_1",
            "Peak_2",
            "Phase_1_inner_quantification",
            "Phase_2_inner_quantification",
        ]
    ]
    Quantification_2_phases = pd.concat(
        [
            Quantification_2_phases_inner,
            Quantification_Outer_phase_1,
            Quantification_Outer_phase_2,
            Peaks_1_phase,
            Peaks_2_phase,
        ],
        axis=1,
    )
    Quantification_2_phases["total_quantification_phase_1"] = (
        Quantification_2_phases["Phase_1_inner_quantification"]
        + Quantification_2_phases["Quantification_Outer_phase_1"]
    )
    Quantification_2_phases["total_quantification_phase_2"] = (
        Quantification_2_phases["Phase_2_inner_quantification"]
        + Quantification_2_phases["Quantification_Outer_phase_2"]
    )
    Quantification_2_phases = Quantification_2_phases[
        [
            "Peak_1",
            "Peak_2",
            "total_quantification_phase_1",
            "total_quantification_phase_2",
        ]
    ]
    Quantification_2_phases["Phase_1_surface_quantification"] = Surface_volume_phase_1[
        "Surface_volume_phase_1"
    ]
    Quantification_2_phases["Phase_2_surface_quantification"] = Surface_volume_phase_2[
        "Surface_volume_phase_2"
    ]

    cols = ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
    Phase_5_threshold = 100000
    thresholds = [
        background_peak,
        phase_1_threshold,
        phase_2_threshold,
        phase_3_threshold,
        phase_4_threshold,
        Phase_5_threshold,
    ]

    Quantification_2_phase_sorted = pd.DataFrame(
        columns=cols + [f"Phase_{i}_quantification" for i in range(1, 6)]
    )
    Quantification_2_phase_sorted_1 = Quantification_2_phase_sorted.copy()
    for i in range(1, 6):
        mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
            Peaks_1_phase["Peak_1"] <= thresholds[i]
        )
        Quantification_2_phase_sorted[f"Peak_{i}"] = np.where(
            mask, Peaks_1_phase["Peak_1"], 0
        )
        Quantification_2_phase_sorted[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_2_phases["total_quantification_phase_1"], 0
        )
        Quantification_2_phase_sorted[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Quantification_2_phases["Phase_1_surface_quantification"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_2_phase["Peak_2"] > thresholds[i - 1]) & (
            Peaks_2_phase["Peak_2"] <= thresholds[i]
        )
        Quantification_2_phase_sorted_1[f"Peak_{i}"] = np.where(
            mask, Peaks_2_phase["Peak_2"], 0
        )
        Quantification_2_phase_sorted_1[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_2_phases["total_quantification_phase_2"], 0
        )
        Quantification_2_phase_sorted_1[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Quantification_2_phases["Phase_2_surface_quantification"], 0
        )

    Quantification_2_phase_sorted = Quantification_2_phase_sorted.mask(
        Quantification_2_phase_sorted == 0, Quantification_2_phase_sorted_1
    )
    Quantification_2_phase_sorted.index = Quantification_2_phases.index

    return (
        Quantification_2_phase_sorted,
        regions2Phases,
        regionsAnalysed,
        volumeAnalysed,
    )


def quantify3_phases_particle(
    Histograms_Subdata,
    Gradient_Subdata,
    surface_mesh_subdata,
    array,
    background_peak,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    regionsAnalysed,
    volumeAnalysed,
    regions3Phases,
):
    #### 3 Phases per region
    Quantification_all_3_phases_1 = []
    Quantification_all_3_phases_2 = []
    Quantification_all_3_phases_3 = []
    Peaks_1_phase = []
    Peaks_2_phase = []
    Peaks_3_phase = []
    Index_3_phase = []
    Surface_volume_phase_1_append = []
    Surface_volume_phase_2_append = []
    Surface_volume_phase_3_append = []
    i = 0
    for index, row in surface_mesh_subdata.iterrows():
        Peaks = array.iloc[[i]].values
        if (np.count_nonzero(Peaks > background_peak) == 3) and i > -1:
            Partical_peak = Peaks[Peaks > background_peak]
            Partical_peak_1 = Partical_peak.flat[0]
            Partical_peak_1 = int(float(Partical_peak_1))
            Partical_peak_2 = Partical_peak.flat[1]
            Partical_peak_2 = int(float(Partical_peak_2))
            Partical_peak_3 = Partical_peak.flat[2]
            Partical_peak_3 = int(float(Partical_peak_3))
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_1 = Histograms_Subdata.iloc[
                i, background_peak : int((Partical_peak_1 + Partical_peak_2) / 2)
            ].sum()
            Sum_phase_1 = Sum_phase_1.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_3_phases_1.append([Sum_phase_1])
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_2 = Histograms_Subdata.iloc[
                i,
                int((Partical_peak_1 + Partical_peak_2) / 2) : int(
                    (Partical_peak_2 + Partical_peak_3) / 2
                ),
            ].sum()
            Sum_phase_2 = Sum_phase_2.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_3_phases_2.append([Sum_phase_2])
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_3 = Histograms_Subdata.iloc[
                i, int((Partical_peak_2 + Partical_peak_3) / 2) : 65535
            ].sum()
            Sum_phase_3 = Sum_phase_3.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_3_phases_3.append([Sum_phase_3])
            Index_3_phase.append([index])
            Peaks_1_phase.append([Partical_peak_1])
            Peaks_2_phase.append([Partical_peak_2])
            Peaks_3_phase.append([Partical_peak_3])
            Gradient_ratio = Gradient_Subdata["Gradient_3"].iloc[i]

            if Partical_peak_1 < phase_1_threshold:
                Phase_limit_1 = phase_1_threshold
            elif phase_1_threshold <= Partical_peak_1 < phase_2_threshold:
                Phase_limit_1 = phase_2_threshold
            elif phase_2_threshold <= Partical_peak_1 < phase_3_threshold:
                Phase_limit_1 = phase_3_threshold
            else:
                Phase_limit_1 = phase_4_threshold

            if phase_1_threshold <= Partical_peak_2 < phase_2_threshold:
                Phase_limit_2 = phase_2_threshold
            elif phase_2_threshold <= Partical_peak_2 < phase_3_threshold:
                Phase_limit_2 = phase_3_threshold
            else:
                Phase_limit_2 = phase_4_threshold
            Phase_1_surface_volume = surface_mesh_subdata.iloc[
                i, background_peak : int(Phase_limit_1 * Gradient_ratio)
            ].sum()
            Phase_2_surface_volume = surface_mesh_subdata.iloc[
                i,
                int(Phase_limit_1 * Gradient_ratio) : int(
                    Phase_limit_2 * Gradient_ratio
                ),
            ].sum()
            Phase_3_surface_volume = surface_mesh_subdata.iloc[
                i, int(Phase_limit_2 * Gradient_ratio) :
            ].sum()
            Surface_volume_phase_1_append.append([Phase_1_surface_volume])
            Surface_volume_phase_2_append.append([Phase_2_surface_volume])
            Surface_volume_phase_3_append.append([Phase_3_surface_volume])
            regions3Phases = (
                regions3Phases + 1
            )  ##################################################################################### to REPORT
            regionsAnalysed = (
                regionsAnalysed + 1
            )  ################################################################################## Pass to other functions
            volumeAnalysed = (
                volumeAnalysed + Sum_phase_1 + Sum_phase_2 + Sum_phase_3
            )  ############################################## Pass to other functions
        i = i + 1
        # Creating Quantification_all of quantification of voxels which have 100% phase 1
    Quantification_all_3_phases_1 = pd.DataFrame(
        Quantification_all_3_phases_1, columns=["total_quantification_phase_1"]
    )
    Quantification_all_3_phases_2 = pd.DataFrame(
        Quantification_all_3_phases_2, columns=["total_quantification_phase_2"]
    )
    Quantification_all_3_phases_3 = pd.DataFrame(
        Quantification_all_3_phases_3, columns=["total_quantification_phase_3"]
    )
    Index_3_phase = pd.DataFrame(Index_3_phase, columns=["Label"])
    Peaks_1_phase = pd.DataFrame(Peaks_1_phase, columns=["Peak_1"])
    Peaks_2_phase = pd.DataFrame(Peaks_2_phase, columns=["Peak_2"])
    Peaks_3_phase = pd.DataFrame(Peaks_3_phase, columns=["Peak_3"])

    Surface_volume_phase_1 = pd.DataFrame(
        Surface_volume_phase_1_append, columns=["Surface_volume_phase_1"]
    )
    Surface_volume_phase_1.index = Index_3_phase["Label"]
    Surface_volume_phase_2 = pd.DataFrame(
        Surface_volume_phase_2_append, columns=["Surface_volume_phase_2"]
    )
    Surface_volume_phase_2.index = Index_3_phase["Label"]
    Surface_volume_phase_3 = pd.DataFrame(
        Surface_volume_phase_3_append, columns=["Surface_volume_phase_3"]
    )
    Surface_volume_phase_3.index = Index_3_phase["Label"]
    Quantification_3_phases = pd.concat(
        [
            Index_3_phase,
            Quantification_all_3_phases_1,
            Quantification_all_3_phases_2,
            Quantification_all_3_phases_3,
            Peaks_1_phase,
            Peaks_2_phase,
            Peaks_3_phase,
        ],
        axis=1,
    )
    cols = ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
    Phase_5_threshold = 100000
    thresholds = [
        background_peak,
        phase_1_threshold,
        phase_2_threshold,
        phase_3_threshold,
        phase_4_threshold,
        Phase_5_threshold,
    ]
    Quantification_3_phase_sorted = pd.DataFrame(
        columns=cols + [f"Phase_{i}_quantification" for i in range(1, 6)]
    )
    Quantification_3_phase_sorted_1 = Quantification_3_phase_sorted.copy()
    Quantification_3_phase_sorted_2 = Quantification_3_phase_sorted.copy()
    for i in range(1, 6):
        mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
            Peaks_1_phase["Peak_1"] <= thresholds[i]
        )
        Quantification_3_phase_sorted[f"Peak_{i}"] = np.where(
            mask, Peaks_1_phase["Peak_1"], 0
        )
        Quantification_3_phase_sorted[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_3_phases["total_quantification_phase_1"], 0
        )
        Quantification_3_phase_sorted[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_1["Surface_volume_phase_1"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_2_phase["Peak_2"] > thresholds[i - 1]) & (
            Peaks_2_phase["Peak_2"] <= thresholds[i]
        )
        Quantification_3_phase_sorted_1[f"Peak_{i}"] = np.where(
            mask, Peaks_2_phase["Peak_2"], 0
        )
        Quantification_3_phase_sorted_1[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_3_phases["total_quantification_phase_2"], 0
        )
        Quantification_3_phase_sorted_1[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_2["Surface_volume_phase_2"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_3_phase["Peak_3"] > thresholds[i - 1]) & (
            Peaks_3_phase["Peak_3"] <= thresholds[i]
        )
        Quantification_3_phase_sorted_2[f"Peak_{i}"] = np.where(
            mask, Peaks_3_phase["Peak_3"], 0
        )
        Quantification_3_phase_sorted_2[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_3_phases["total_quantification_phase_3"], 0
        )
        Quantification_3_phase_sorted_2[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_3["Surface_volume_phase_3"], 0
        )
    Quantification_3_phase_sorted = Quantification_3_phase_sorted.mask(
        Quantification_3_phase_sorted == 0, Quantification_3_phase_sorted_1
    )
    Quantification_3_phase_sorted = Quantification_3_phase_sorted.mask(
        Quantification_3_phase_sorted == 0, Quantification_3_phase_sorted_2
    )
    Quantification_3_phase_sorted.index = Quantification_3_phases["Label"]

    return (
        Quantification_3_phase_sorted,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    )


def quaternary_regions(
    Histograms_Subdata,
    Gradient_Subdata,
    surface_mesh_subdata,
    array,
    background_peak,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    regionsAnalysed,
    volumeAnalysed,
    regions3Phases,
):
    #### 4 Phases per region

    Quantification_all_4_phases_1 = []
    Quantification_all_4_phases_2 = []
    Quantification_all_4_phases_3 = []
    Quantification_all_4_phases_4 = []
    Peaks_1_phase = []
    Peaks_2_phase = []
    Peaks_3_phase = []
    Peaks_4_phase = []
    Index_4_phase = []
    Surface_volume_phase_1_append = []
    Surface_volume_phase_2_append = []
    Surface_volume_phase_3_append = []
    Surface_volume_phase_4_append = []
    i = 0
    for index, row in surface_mesh_subdata.iterrows():
        Peaks = array.iloc[[i]].values
        if (np.count_nonzero(Peaks > background_peak) == 4) and i > -1:
            Partical_peak = Peaks[Peaks > background_peak]
            Partical_peak_1 = Partical_peak.flat[0]
            Partical_peak_1 = int(float(Partical_peak_1))
            Partical_peak_2 = Partical_peak.flat[1]
            Partical_peak_2 = int(float(Partical_peak_2))
            Partical_peak_3 = Partical_peak.flat[2]
            Partical_peak_3 = int(float(Partical_peak_3))
            Partical_peak_4 = Partical_peak.flat[3]
            Partical_peak_4 = int(float(Partical_peak_4))
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_1 = Histograms_Subdata.iloc[
                i, background_peak : int((Partical_peak_1 + Partical_peak_2) / 2)
            ].sum()
            Sum_phase_1 = Sum_phase_1.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_4_phases_1.append([Sum_phase_1])
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_2 = Histograms_Subdata.iloc[
                i,
                int((Partical_peak_1 + Partical_peak_2) / 2) : int(
                    (Partical_peak_2 + Partical_peak_3) / 2
                ),
            ].sum()
            Sum_phase_2 = Sum_phase_2.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_4_phases_2.append([Sum_phase_2])
            Sum_phase_3 = Histograms_Subdata.iloc[
                i,
                int((Partical_peak_2 + Partical_peak_3) / 2) : int(
                    (Partical_peak_3 + Partical_peak_4) / 2
                ),
            ].sum()
            Sum_phase_3 = Sum_phase_3.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_4_phases_3.append([Sum_phase_3])
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_4 = Histograms_Subdata.iloc[
                i, int((Partical_peak_3 + Partical_peak_4) / 2) : 65535
            ].sum()
            Sum_phase_4 = Sum_phase_4.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_4_phases_4.append([Sum_phase_4])

            Index_4_phase.append([index])
            Peaks_1_phase.append([Partical_peak_1])
            Peaks_2_phase.append([Partical_peak_2])
            Peaks_3_phase.append([Partical_peak_3])
            Peaks_4_phase.append([Partical_peak_4])
            Gradient_ratio = Gradient_Subdata["Gradient_3"].iloc[i]
            if Partical_peak_1 < phase_1_threshold:
                Phase_limit_1 = phase_1_threshold
            elif phase_1_threshold <= Partical_peak_1 < phase_2_threshold:
                Phase_limit_1 = phase_2_threshold
            elif phase_2_threshold <= Partical_peak_1 < phase_3_threshold:
                Phase_limit_1 = phase_3_threshold
            else:
                Phase_limit_1 = phase_4_threshold

            if phase_1_threshold <= Partical_peak_2 < phase_2_threshold:
                Phase_limit_2 = phase_2_threshold
            elif phase_2_threshold <= Partical_peak_2 < phase_3_threshold:
                Phase_limit_2 = phase_3_threshold
            else:
                Phase_limit_2 = phase_4_threshold

            if phase_2_threshold <= Partical_peak_3 < phase_3_threshold:
                Phase_limit_3 = phase_3_threshold
            else:
                Phase_limit_3 = phase_4_threshold

            Phase_1_surface_volume = surface_mesh_subdata.iloc[
                i, background_peak : int(Phase_limit_1 * Gradient_ratio)
            ].sum()
            Phase_2_surface_volume = surface_mesh_subdata.iloc[
                i,
                int(Phase_limit_1 * Gradient_ratio) : int(
                    Phase_limit_2 * Gradient_ratio
                ),
            ].sum()
            Phase_3_surface_volume = surface_mesh_subdata.iloc[
                i,
                int(Phase_limit_2 * Gradient_ratio) : int(
                    Phase_limit_3 * Gradient_ratio
                ),
            ].sum()
            Phase_4_surface_volume = surface_mesh_subdata.iloc[
                i, int(Phase_limit_3 * Gradient_ratio) :
            ].sum()
            Surface_volume_phase_1_append.append([Phase_1_surface_volume])
            Surface_volume_phase_2_append.append([Phase_2_surface_volume])
            Surface_volume_phase_3_append.append([Phase_3_surface_volume])
            Surface_volume_phase_4_append.append([Phase_4_surface_volume])
            regions3Phases = (
                regions3Phases + 1
            )  ##################################################################################### Pass to other functions
            regionsAnalysed = (
                regionsAnalysed + 1
            )  ################################################################################## Pass to other functions
            volumeAnalysed = (
                volumeAnalysed + Sum_phase_1 + Sum_phase_2 + Sum_phase_3 + Sum_phase_4
            )  ############################################## Pass to other functions

        i = i + 1

    # Creating Quantification_all of quantification of voxels which have 100% phase 1
    Quantification_all_4_phases_1 = pd.DataFrame(
        Quantification_all_4_phases_1, columns=["total_quantification_phase_1"]
    )
    Quantification_all_4_phases_2 = pd.DataFrame(
        Quantification_all_4_phases_2, columns=["total_quantification_phase_2"]
    )
    Quantification_all_4_phases_3 = pd.DataFrame(
        Quantification_all_4_phases_3, columns=["total_quantification_phase_3"]
    )
    Quantification_all_4_phases_4 = pd.DataFrame(
        Quantification_all_4_phases_4, columns=["total_quantification_phase_4"]
    )
    Index_4_phase = pd.DataFrame(Index_4_phase, columns=["Label"])
    Peaks_1_phase = pd.DataFrame(Peaks_1_phase, columns=["Peak_1"])
    Peaks_2_phase = pd.DataFrame(Peaks_2_phase, columns=["Peak_2"])
    Peaks_3_phase = pd.DataFrame(Peaks_3_phase, columns=["Peak_3"])
    Peaks_4_phase = pd.DataFrame(Peaks_4_phase, columns=["Peak_4"])

    Surface_volume_phase_1 = pd.DataFrame(
        Surface_volume_phase_1_append, columns=["Surface_volume_phase_1"]
    )
    Surface_volume_phase_1.index = Index_4_phase["Label"]
    Surface_volume_phase_2 = pd.DataFrame(
        Surface_volume_phase_2_append, columns=["Surface_volume_phase_2"]
    )
    Surface_volume_phase_2.index = Index_4_phase["Label"]
    Surface_volume_phase_3 = pd.DataFrame(
        Surface_volume_phase_3_append, columns=["Surface_volume_phase_3"]
    )
    Surface_volume_phase_3.index = Index_4_phase["Label"]
    Surface_volume_phase_4 = pd.DataFrame(
        Surface_volume_phase_4_append, columns=["Surface_volume_phase_4"]
    )
    Surface_volume_phase_4.index = Index_4_phase["Label"]
    Quantification_4_phases = pd.concat(
        [
            Index_4_phase,
            Quantification_all_4_phases_1,
            Quantification_all_4_phases_2,
            Quantification_all_4_phases_3,
            Quantification_all_4_phases_4,
            Peaks_1_phase,
            Peaks_2_phase,
            Peaks_3_phase,
            Peaks_4_phase,
        ],
        axis=1,
    )
    cols = ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
    Phase_5_threshold = 100000
    thresholds = [
        background_peak,
        phase_1_threshold,
        phase_2_threshold,
        phase_3_threshold,
        phase_4_threshold,
        Phase_5_threshold,
    ]

    Quantification_4_phase_sorted = pd.DataFrame(
        columns=cols + [f"Phase_{i}_quantification" for i in range(1, 6)]
    )
    Quantification_4_phase_sorted_1 = Quantification_4_phase_sorted.copy()
    Quantification_4_phase_sorted_2 = Quantification_4_phase_sorted.copy()
    Quantification_4_phase_sorted_3 = Quantification_4_phase_sorted.copy()
    for i in range(1, 6):
        mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
            Peaks_1_phase["Peak_1"] <= thresholds[i]
        )
        Quantification_4_phase_sorted[f"Peak_{i}"] = np.where(
            mask, Peaks_1_phase["Peak_1"], 0
        )
        Quantification_4_phase_sorted[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_4_phases["total_quantification_phase_1"], 0
        )
        Quantification_4_phase_sorted[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_1["Surface_volume_phase_1"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_2_phase["Peak_2"] > thresholds[i - 1]) & (
            Peaks_2_phase["Peak_2"] <= thresholds[i]
        )
        Quantification_4_phase_sorted_1[f"Peak_{i}"] = np.where(
            mask, Peaks_2_phase["Peak_2"], 0
        )
        Quantification_4_phase_sorted_1[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_4_phases["total_quantification_phase_2"], 0
        )
        Quantification_4_phase_sorted_1[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_2["Surface_volume_phase_2"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_3_phase["Peak_3"] > thresholds[i - 1]) & (
            Peaks_3_phase["Peak_3"] <= thresholds[i]
        )
        Quantification_4_phase_sorted_2[f"Peak_{i}"] = np.where(
            mask, Peaks_3_phase["Peak_3"], 0
        )
        Quantification_4_phase_sorted_2[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_4_phases["total_quantification_phase_3"], 0
        )
        Quantification_4_phase_sorted_2[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_3["Surface_volume_phase_3"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_4_phase["Peak_4"] > thresholds[i - 1]) & (
            Peaks_4_phase["Peak_4"] <= thresholds[i]
        )
        Quantification_4_phase_sorted_3[f"Peak_{i}"] = np.where(
            mask, Peaks_4_phase["Peak_4"], 0
        )
        Quantification_4_phase_sorted_3[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_4_phases["total_quantification_phase_4"], 0
        )
        Quantification_4_phase_sorted_3[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_4["Surface_volume_phase_4"], 0
        )
    Quantification_4_phase_sorted = Quantification_4_phase_sorted.mask(
        Quantification_4_phase_sorted == 0, Quantification_4_phase_sorted_1
    )
    Quantification_4_phase_sorted = Quantification_4_phase_sorted.mask(
        Quantification_4_phase_sorted == 0, Quantification_4_phase_sorted_2
    )
    Quantification_4_phase_sorted = Quantification_4_phase_sorted.mask(
        Quantification_4_phase_sorted == 0, Quantification_4_phase_sorted_3
    )
    Quantification_4_phase_sorted.index = Quantification_4_phases["Label"]

    return (
        Quantification_4_phase_sorted,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    )


def quinary_regions(
    Histograms_Subdata,
    Gradient_Subdata,
    surface_mesh_subdata,
    array,
    background_peak,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    regionsAnalysed,
    volumeAnalysed,
    regions3Phases,
):
    #### 5 Phases per region
    Quantification_all_5_phases_1 = []
    Quantification_all_5_phases_2 = []
    Quantification_all_5_phases_3 = []
    Quantification_all_5_phases_4 = []
    Quantification_all_5_phases_5 = []
    Peaks_1_phase = []
    Peaks_2_phase = []
    Peaks_3_phase = []
    Peaks_4_phase = []
    Peaks_5_phase = []
    Index_5_phase = []
    Surface_volume_phase_1_append = []
    Surface_volume_phase_2_append = []
    Surface_volume_phase_3_append = []
    Surface_volume_phase_4_append = []
    Surface_volume_phase_5_append = []
    i = 0
    for index, row in surface_mesh_subdata.iterrows():
        Peaks = array.iloc[[i]].values
        if (np.count_nonzero(Peaks > background_peak) == 5) and i > -1:
            Partical_peak = Peaks[Peaks > background_peak]
            Partical_peak_1 = Partical_peak.flat[0]
            Partical_peak_1 = int(float(Partical_peak_1))
            Partical_peak_2 = Partical_peak.flat[1]
            Partical_peak_2 = int(float(Partical_peak_2))
            Partical_peak_3 = Partical_peak.flat[2]
            Partical_peak_3 = int(float(Partical_peak_3))
            Partical_peak_4 = Partical_peak.flat[3]
            Partical_peak_4 = int(float(Partical_peak_4))
            Partical_peak_5 = Partical_peak.flat[4]
            Partical_peak_5 = int(float(Partical_peak_5))
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_1 = Histograms_Subdata.iloc[
                i, background_peak : int((Partical_peak_1 + Partical_peak_2) / 2)
            ].sum()
            Sum_phase_1 = Sum_phase_1.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_5_phases_1.append([Sum_phase_1])
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_2 = Histograms_Subdata.iloc[
                i,
                int((Partical_peak_1 + Partical_peak_2) / 2) : int(
                    (Partical_peak_2 + Partical_peak_3) / 2
                ),
            ].sum()
            Sum_phase_2 = Sum_phase_2.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_5_phases_2.append([Sum_phase_2])
            Sum_phase_3 = Histograms_Subdata.iloc[
                i,
                int((Partical_peak_2 + Partical_peak_3) / 2) : int(
                    (Partical_peak_3 + Partical_peak_4) / 2
                ),
            ].sum()
            Sum_phase_3 = Sum_phase_3.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_5_phases_3.append([Sum_phase_3])
            # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
            Sum_phase_4 = Histograms_Subdata.iloc[
                i,
                int((Partical_peak_3 + Partical_peak_4) / 2) : int(
                    (Partical_peak_4 + Partical_peak_5) / 2
                ),
            ].sum()
            Sum_phase_4 = Sum_phase_4.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_5_phases_4.append([Sum_phase_4])
            Sum_phase_5 = Histograms_Subdata.iloc[
                i, : int((Partical_peak_4 + Partical_peak_5) / 2) : 65535
            ].sum()
            Sum_phase_5 = Sum_phase_5.sum()
            # Appending the phase 1 quantification sum
            Quantification_all_5_phases_5.append([Sum_phase_5])
            Index_5_phase.append([index])
            Peaks_1_phase.append([Partical_peak_1])
            Peaks_2_phase.append([Partical_peak_2])
            Peaks_3_phase.append([Partical_peak_3])
            Peaks_4_phase.append([Partical_peak_4])
            Peaks_5_phase.append([Partical_peak_5])
            Gradient_ratio = Gradient_Subdata["Gradient_3"].iloc[i]
            Phase_limit_1 = phase_1_threshold
            Phase_limit_2 = phase_2_threshold
            Phase_limit_3 = phase_3_threshold
            Phase_limit_4 = phase_4_threshold
            Phase_1_surface_volume = surface_mesh_subdata.iloc[
                i, background_peak : int(Phase_limit_1 * Gradient_ratio)
            ].sum()
            Phase_2_surface_volume = surface_mesh_subdata.iloc[
                i,
                int(Phase_limit_1 * Gradient_ratio) : int(
                    Phase_limit_2 * Gradient_ratio
                ),
            ].sum()
            Phase_3_surface_volume = surface_mesh_subdata.iloc[
                i,
                int(Phase_limit_2 * Gradient_ratio) : int(
                    Phase_limit_3 * Gradient_ratio
                ),
            ].sum()
            Phase_4_surface_volume = surface_mesh_subdata.iloc[
                i,
                int(Phase_limit_3 * Gradient_ratio) : int(
                    Phase_limit_4 * Gradient_ratio
                ),
            ].sum()
            Phase_5_surface_volume = surface_mesh_subdata.iloc[
                i, int(Phase_limit_4 * Gradient_ratio) :
            ].sum()
            Surface_volume_phase_1_append.append([Phase_1_surface_volume])
            Surface_volume_phase_2_append.append([Phase_2_surface_volume])
            Surface_volume_phase_3_append.append([Phase_3_surface_volume])
            Surface_volume_phase_4_append.append([Phase_4_surface_volume])
            Surface_volume_phase_5_append.append([Phase_5_surface_volume])
            regions3Phases = (
                regions3Phases + 1
            )  ##################################################################################### Pass to other functions
            regionsAnalysed = (
                regionsAnalysed + 1
            )  ################################################################################## Pass to other functions
            volumeAnalysed = (
                volumeAnalysed
                + Sum_phase_1
                + Sum_phase_2
                + Sum_phase_3
                + Sum_phase_4
                + Sum_phase_5
            )  ############################################## Pass to other functions

        i = i + 1

    # Creating Quantification_all of quantification of voxels which have 100% phase 1
    Quantification_all_5_phases_1 = pd.DataFrame(
        Quantification_all_5_phases_1, columns=["total_quantification_phase_1"]
    )
    Quantification_all_5_phases_2 = pd.DataFrame(
        Quantification_all_5_phases_2, columns=["total_quantification_phase_2"]
    )
    Quantification_all_5_phases_3 = pd.DataFrame(
        Quantification_all_5_phases_3, columns=["total_quantification_phase_3"]
    )
    Quantification_all_5_phases_4 = pd.DataFrame(
        Quantification_all_5_phases_4, columns=["total_quantification_phase_4"]
    )
    Quantification_all_5_phases_5 = pd.DataFrame(
        Quantification_all_5_phases_5, columns=["total_quantification_phase_5"]
    )
    Index_5_phase = pd.DataFrame(Index_5_phase, columns=["Label"])
    Peaks_1_phase = pd.DataFrame(Peaks_1_phase, columns=["Peak_1"])
    Peaks_2_phase = pd.DataFrame(Peaks_2_phase, columns=["Peak_2"])
    Peaks_3_phase = pd.DataFrame(Peaks_3_phase, columns=["Peak_3"])
    Peaks_4_phase = pd.DataFrame(Peaks_4_phase, columns=["Peak_4"])
    Peaks_5_phase = pd.DataFrame(Peaks_5_phase, columns=["Peak_5"])
    Surface_volume_phase_1 = pd.DataFrame(
        Surface_volume_phase_1_append, columns=["Surface_volume_phase_1"]
    )
    Surface_volume_phase_1.index = Index_5_phase["Label"]
    Surface_volume_phase_2 = pd.DataFrame(
        Surface_volume_phase_2_append, columns=["Surface_volume_phase_2"]
    )
    Surface_volume_phase_2.index = Index_5_phase["Label"]
    Surface_volume_phase_3 = pd.DataFrame(
        Surface_volume_phase_3_append, columns=["Surface_volume_phase_3"]
    )
    Surface_volume_phase_3.index = Index_5_phase["Label"]
    Surface_volume_phase_4 = pd.DataFrame(
        Surface_volume_phase_4_append, columns=["Surface_volume_phase_4"]
    )
    Surface_volume_phase_4.index = Index_5_phase["Label"]
    Surface_volume_phase_5 = pd.DataFrame(
        Surface_volume_phase_5_append, columns=["Surface_volume_phase_5"]
    )
    Surface_volume_phase_5.index = Index_5_phase["Label"]
    Quantification_5_phases = pd.concat(
        [
            Index_5_phase,
            Quantification_all_5_phases_1,
            Quantification_all_5_phases_2,
            Quantification_all_5_phases_3,
            Quantification_all_5_phases_4,
            Quantification_all_5_phases_5,
            Peaks_1_phase,
            Peaks_2_phase,
            Peaks_3_phase,
            Peaks_4_phase,
            Peaks_5_phase,
        ],
        axis=1,
    )
    cols = ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
    Phase_5_threshold = 100000
    thresholds = [
        background_peak,
        phase_1_threshold,
        phase_2_threshold,
        phase_3_threshold,
        phase_4_threshold,
        Phase_5_threshold,
    ]
    Quantification_5_phase_sorted = pd.DataFrame(
        columns=cols + [f"Phase_{i}_quantification" for i in range(1, 6)]
    )
    Quantification_5_phase_sorted_1 = Quantification_5_phase_sorted.copy()
    Quantification_5_phase_sorted_2 = Quantification_5_phase_sorted.copy()
    Quantification_5_phase_sorted_3 = Quantification_5_phase_sorted.copy()
    Quantification_5_phase_sorted_4 = Quantification_5_phase_sorted.copy()
    for i in range(1, 6):
        mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
            Peaks_1_phase["Peak_1"] <= thresholds[i]
        )
        Quantification_5_phase_sorted[f"Peak_{i}"] = np.where(
            mask, Peaks_1_phase["Peak_1"], 0
        )
        Quantification_5_phase_sorted[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_5_phases["total_quantification_phase_1"], 0
        )
        Quantification_5_phase_sorted[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_1["Surface_volume_phase_1"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_2_phase["Peak_2"] > thresholds[i - 1]) & (
            Peaks_2_phase["Peak_2"] <= thresholds[i]
        )
        Quantification_5_phase_sorted_1[f"Peak_{i}"] = np.where(
            mask, Peaks_2_phase["Peak_2"], 0
        )
        Quantification_5_phase_sorted_1[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_5_phases["total_quantification_phase_2"], 0
        )
        Quantification_5_phase_sorted_1[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_2["Surface_volume_phase_2"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_3_phase["Peak_3"] > thresholds[i - 1]) & (
            Peaks_3_phase["Peak_3"] <= thresholds[i]
        )
        Quantification_5_phase_sorted_2[f"Peak_{i}"] = np.where(
            mask, Peaks_3_phase["Peak_3"], 0
        )
        Quantification_5_phase_sorted_2[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_5_phases["total_quantification_phase_3"], 0
        )
        Quantification_5_phase_sorted_2[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_3["Surface_volume_phase_3"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_4_phase["Peak_4"] > thresholds[i - 1]) & (
            Peaks_4_phase["Peak_4"] <= thresholds[i]
        )
        Quantification_5_phase_sorted_3[f"Peak_{i}"] = np.where(
            mask, Peaks_4_phase["Peak_4"], 0
        )
        Quantification_5_phase_sorted_3[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_5_phases["total_quantification_phase_4"], 0
        )
        Quantification_5_phase_sorted_3[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_4["Surface_volume_phase_4"], 0
        )
    for i in range(1, 6):
        mask = (Peaks_5_phase["Peak_5"] > thresholds[i - 1]) & (
            Peaks_5_phase["Peak_5"] <= thresholds[i]
        )
        Quantification_5_phase_sorted_4[f"Peak_{i}"] = np.where(
            mask, Peaks_5_phase["Peak_5"], 0
        )
        Quantification_5_phase_sorted_4[f"Phase_{i}_quantification"] = np.where(
            mask, Quantification_5_phases["total_quantification_phase_5"], 0
        )
        Quantification_5_phase_sorted_4[f"Phase_{i}_surface_quantification"] = np.where(
            mask, Surface_volume_phase_5["Surface_volume_phase_5"], 0
        )
    Quantification_5_phase_sorted = Quantification_5_phase_sorted.mask(
        Quantification_5_phase_sorted == 0, Quantification_5_phase_sorted_1
    )
    Quantification_5_phase_sorted = Quantification_5_phase_sorted.mask(
        Quantification_5_phase_sorted == 0, Quantification_5_phase_sorted_2
    )
    Quantification_5_phase_sorted = Quantification_5_phase_sorted.mask(
        Quantification_5_phase_sorted == 0, Quantification_5_phase_sorted_3
    )
    Quantification_5_phase_sorted = Quantification_5_phase_sorted.mask(
        Quantification_5_phase_sorted == 0, Quantification_5_phase_sorted_4
    )
    Quantification_5_phase_sorted.index = Quantification_5_phases["Label"]
    return (
        Quantification_5_phase_sorted,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    )


def arrange_columns(df):
    df["Label"] = df.index
    column_order = [
        "Label",
        "Peak_1",
        "Peak_2",
        "Peak_3",
        "Peak_4",
        "Peak_5",
        "Phase_1_quantification",
        "Phase_2_quantification",
        "Phase_3_quantification",
        "Phase_4_quantification",
        "Phase_5_quantification",
        "Phase_1_surface_quantification",
        "Phase_2_surface_quantification",
        "Phase_3_surface_quantification",
        "Phase_4_surface_quantification",
        "Phase_5_surface_quantification",
    ]
    # Check if all columns in column_order exist in the DataFrame
    missing_columns = [col for col in column_order if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Columns {missing_columns} not found in DataFrame.")
    # Arrange columns
    arranged_df = df[column_order]
    arranged_df = arranged_df.fillna(0)
    return arranged_df


def quantify_mineralogy(
    properties_data_w_peaks,
    background_peak,
    peak_height,
    histograms_data,
    inputDensityA,
    inputDensityB,
    inputDensityC,
    inputDensityD,
    inputDensityE,
):
    properties_data_w_peaks = pd.DataFrame(properties_data_w_peaks)
    partList = properties_data_w_peaks.index.to_list()

    # filter the histogram data to contain only the particles for which a valid peak was found
    OutHistogram_Subdata = outer_volume_histograms.loc[partList]
    SurfaceMesh_Subdata = surface_mesh_histogram.loc[partList]
    InHistogram_Subdata = inner_volume_histograms.loc[partList]
    Histograms_Subdata = histograms_data.loc[partList]
    Gradient_Subdata = gradient.loc[partList]

    # subdata_properties is a subdataset from properties that contains only the peaks
    subdata_properties = _update_peak_positions(
        properties_data_w_peaks, background_peak, peak_height
    )

    # counter variables
    regions3Phases = 0
    regionsAnalysed = 0
    volumeAnalysed = 0

    phaseA = 0
    phaseB = 0
    phaseC = 0
    phaseD = 0
    phaseE = 0

    (
        q_liberated,
        regionsLiberated,
        regionsAnalysed,
        volumeAnalysed,
    ) = quantify_liberated_regions(
        SurfaceMesh_Subdata,
        subdata_properties,
        background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        regionsAnalysed,
        volumeAnalysed,
    )
    (
        q_binary,
        regions2Phases,
        regionsAnalysed,
        volumeAnalysed,
    ) = quantify_two_phases_particle(
        InHistogram_Subdata,
        OutHistogram_Subdata,
        Gradient_Subdata,
        SurfaceMesh_Subdata,
        subdata_properties,
        background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        regionsAnalysed,
        volumeAnalysed,
        background_peak,
    )
    (
        q_ternary,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    ) = quantify3_phases_particle(
        Histograms_Subdata,
        Gradient_Subdata,
        SurfaceMesh_Subdata,
        subdata_properties,
        background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    )
    q_quarternary, regionsAnalysed, volumeAnalysed, regions3Phases = quaternary_regions(
        Histograms_Subdata,
        Gradient_Subdata,
        SurfaceMesh_Subdata,
        subdata_properties,
        background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    )
    q_quintary, regionsAnalysed, volumeAnalysed, regions3Phases = quinary_regions(
        Histograms_Subdata,
        Gradient_Subdata,
        SurfaceMesh_Subdata,
        subdata_properties,
        background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    )
    q_liberated = arrange_columns(q_liberated)
    q_binary = arrange_columns(q_binary)
    q_ternary = arrange_columns(q_ternary)
    q_quarternary = arrange_columns(q_quarternary)
    q_quintary = arrange_columns(q_quintary)

    non_empty_quantification_ds = [
        df.dropna(how="all")
        for df in [q_liberated, q_binary, q_ternary, q_quarternary, q_quintary]
        if not df.dropna(how="all").empty
    ]
    quantification = pd.concat(non_empty_quantification_ds, axis=0)
    quantification["Total_quantification"] = (
        quantification["Phase_1_quantification"]
        + quantification["Phase_2_quantification"]
        + quantification["Phase_3_quantification"]
        + quantification["Phase_4_quantification"]
        + quantification["Phase_5_quantification"]
    )
    quantification = quantification.sort_index(ascending=True)
    surfaceA = quantification["Phase_1_surface_quantification"].sum()
    surfaceB = quantification["Phase_2_surface_quantification"].sum()
    surfaceC = quantification["Phase_3_surface_quantification"].sum()
    surfaceD = quantification["Phase_4_surface_quantification"].sum()
    surfaceE = quantification["Phase_5_surface_quantification"].sum()

    phaseA_mass = quantification["Phase_1_quantification"].sum() * inputDensityA
    phaseB_mass = quantification["Phase_2_quantification"].sum() * inputDensityB
    phaseC_mass = quantification["Phase_3_quantification"].sum() * inputDensityC
    phaseD_mass = quantification["Phase_4_quantification"].sum() * inputDensityD
    phaseE_mass = quantification["Phase_5_quantification"].sum() * inputDensityE

    volumeAnalysed2 = (
        quantification["Phase_1_quantification"].sum()
        + quantification["Phase_2_quantification"].sum()
        + quantification["Phase_3_quantification"].sum()
        + quantification["Phase_4_quantification"].sum()
        + quantification["Phase_5_quantification"].sum()
    )
    surfaceAnalysed = surfaceA + surfaceB + surfaceC + surfaceD + surfaceE

    totalMass = phaseA_mass + phaseB_mass + phaseC_mass + phaseD_mass + phaseE_mass
    if totalMass > 0:
        phaseA = round(phaseA_mass * 100 / totalMass, 1)
        phaseB = round(phaseB_mass * 100 / totalMass, 1)
        phaseC = round(phaseC_mass * 100 / totalMass, 1)
        phaseD = round(phaseD_mass * 100 / totalMass, 1)
        phaseE = round(phaseE_mass * 100 / totalMass, 1)
        surfaceA = round(surfaceA * 100 / surfaceAnalysed, 1)
        surfaceB = round(surfaceB * 100 / surfaceAnalysed, 1)
        surfaceC = round(surfaceC * 100 / surfaceAnalysed, 1)
        surfaceD = round(surfaceD * 100 / surfaceAnalysed, 1)
        surfaceE = round(surfaceE * 100 / surfaceAnalysed, 1)

    properties_data_w_peaks.index = properties_data_w_peaks["label"]
    columns_to_keep = [
        col
        for col in properties_data_w_peaks.columns
        if col not in quantification.columns or col == "Label"
    ]
    properties_data_w_peaks = properties_data_w_peaks[columns_to_keep]
    quantification = pd.merge(
        quantification, properties_data_w_peaks, left_index=True, right_index=True
    )
    # Path_save_Quantification = os.path.join(dataDirectory, 'Quantification.csv')
    # Quantification.to_csv(Path_save_Quantification, index=False)  ################################################# This should be in the report

    report = {
        "regions2Phases": regions2Phases,
        "regions3Phases": regions3Phases,
        "regionsAnalysed": regionsAnalysed,
        "volumeAnalysed2": volumeAnalysed2,
        "regionsLiberated": regionsLiberated,
        "volumeAnalysed": volumeAnalysed,
        "surfaceAnalysed": surfaceAnalysed,
        "totalMass": totalMass,
        "phaseA": phaseA,
        "phaseB": phaseB,
        "phaseC": phaseC,
        "phaseD": phaseD,
        "phaseE": phaseE,
        "phaseA_mass": phaseA_mass,
        "phaseB_mass": phaseB_mass,
        "phaseC_mass": phaseC_mass,
        "phaseD_mass": phaseD_mass,
        "phaseE_mass": phaseE_mass,
        "surfaceA": surfaceA,
        "surfaceB": surfaceB,
        "surfaceC": surfaceC,
        "surfaceD": surfaceD,
        "surfaceE": surfaceE,
    }

    return report, quantification


def file_name(path):
    """Select the type of histograms using a dropdown menu, must be h5ad."""
    import streamlit as st

    # initialize streamlit
    st.set_page_config(layout="wide", page_title="All streamlit steps in 1 app")

    histogram_files = [f for f in os.listdir(path) if f.endswith(".h5ad")]
    histogram_type = st.sidebar.selectbox(
        "Histogram type",
        histogram_files,
        index=0,
        help="TIP: Bulk histograms should be used for a general assessment of the parameters. Must click randomize button to refresh the histograms if changed.",
    )  # it resets if new files are created in folder 'Data'
    return histogram_type


############################### Streamlit #################################
import sys

################## CMD Arguments ##################
dataDirectory = sys.argv[1]
report_directory = sys.argv[2]
parameters_json = sys.argv[3]
run_online = sys.argv[4]  # option to run this script without streamlit offline

print("Data Directory:", dataDirectory)
print("Report Directory:", report_directory)
print("Parameters JSON:", parameters_json)
print("Run Online:", run_online)

parameters_dict = get_dict_from_yml(parameters_json)

################## Data ##################
if run_online == "True":
    print("Running in online mode")
    file = file_name(dataDirectory)
else:
    print("Running in offline mode")
    file = "Bulk_histograms.h5ad"  # default file name for offline mode
# load bulk histograms (= Inner + Outer)
path_load_bulk_histogram = os.path.join(dataDirectory, file)
# load inner histograms (inside the region without the eroded voxels)
path_load_inner_histograms = os.path.join(dataDirectory, "Inner_histograms.h5ad")
# load outer (surface layers consisting of all voxels eroded) volume histograms
path_load_outer_histograms = os.path.join(dataDirectory, "Outer_histograms.h5ad")
# load mesh histograms
path_load_surface_mesh_histograms = os.path.join(
    dataDirectory, "Surface_histogram.h5ad"
)
# load gradient
path_load_gradient = os.path.join(dataDirectory, "Gradient.csv")

histogramsData, initialBins = load_histograms(path_load_bulk_histogram)
histogramsData = histogramsData.rename_axis("label")
histogramsData = histogramsData.astype("float64")
histogramsData = histogramsData.iloc[:, 1:]

propertiesData = load_properties(dataDirectory)
propertiesData.index = propertiesData["label"]

inner_volume_histograms = load_in_volume(path_load_inner_histograms)
outer_volume_histograms = load_out_volume(path_load_outer_histograms)
surface_mesh_histogram = load_mesh(path_load_surface_mesh_histograms)
gradient = load_gradient(path_load_gradient)

################## load Arguments ##################
input4Quantification = {
    "BackgroundT": parameters_dict["background_q"],
    "DensityA": parameters_dict["DensityA"],
    "Max greyvalue A": parameters_dict["MaxGreyValueA"],
    "DensityB": parameters_dict["DensityB"],
    "Max greyvalue B": parameters_dict["MaxGreyValueB"],
    "DensityC": parameters_dict["DensityC"],
    "Max greyvalue C": parameters_dict["MaxGreyValueC"],
    "DensityD": parameters_dict["DensityD"],
    "Max greyvalue D": parameters_dict["MaxGreyValueD"],
    "DensityE": parameters_dict["DensityE"],
    "Max greyvalue E": parameters_dict["MaxGreyValueE"],
}

################## offline Arguments ##################
if run_online == "False":
    Peak_Width = parameters_dict["gray_value_width"]
    Peak_Height = parameters_dict["min_frequency"]
    Peak_Prominence = parameters_dict["prominence"]
    Peak_Horizontal_Distance = parameters_dict["horizDistance"]
    Peak_Vertical_Distance = parameters_dict["vertDistance"]

    binInput = parameters_dict["binInput"]
    number_bins = int(initialBins / binInput)
    savgolInput = parameters_dict["savgolInput"]
    enable_savgol = parameters_dict["enableSavgol"]

    inputDensityA = input4Quantification["DensityA"]
    inputDensityB = input4Quantification["DensityB"]
    inputDensityC = input4Quantification["DensityC"]
    inputDensityD = input4Quantification["DensityD"]
    inputDensityE = input4Quantification["DensityE"]
    background_peak = input4Quantification["BackgroundT"]
    Phase_1_threshold = input4Quantification["Max greyvalue A"]
    Phase_2_threshold = input4Quantification["Max greyvalue B"]
    Phase_3_threshold = input4Quantification["Max greyvalue C"]
    Phase_4_threshold = input4Quantification["Max greyvalue D"]
    Phase_5_threshold = input4Quantification["Max greyvalue E"]

    ################## offline process ##################

    histograms_binned = binning(binInput, histogramsData, n_jobs=-1)
    if enable_savgol:
        savgolSmooth = smooth_histograms_savgol(
            histograms_binned, savgolInput, n_jobs=-1
        )
        NormalizedData = normalize_volume(savgolSmooth)
    else:
        NormalizedData = normalize_volume(histograms_binned)

    PeaksSubData = process_peaks(
        NormalizedData,
        histogramsData,
        propertiesData,
        number_bins,
        Peak_Width,
        Peak_Height,
        Peak_Prominence,
        Peak_Vertical_Distance,
        Peak_Horizontal_Distance,
        binInput,
    )
    propertiesAndPeaks = arrange_peaks(
        PeaksSubData,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        Phase_5_threshold,
        background_peak,
        propertiesData,
    )

    report, quantification = quantify_mineralogy(
        propertiesAndPeaks,
        background_peak,
        Peak_Height,
        histogramsData,
        inputDensityA,
        inputDensityB,
        inputDensityC,
        inputDensityD,
        inputDensityE,
    )
    # add particle volume to report
    report["totalParticleVolume"] = str(propertiesData["Volume"].sum())

    # save report
    report_path = os.path.join(report_directory, "report.yml")
    write_dict_to_yml(report_path, report)

    # save quantification
    path_save_Quantification = os.path.join(report_directory, "Quantification.csv")
    quantification.to_csv(path_save_Quantification, index=False)

################## online Arguments ##################
else:
    from tkinter.filedialog import askdirectory

    import streamlit as st

    ############################### Streamlit #################################
    tabHistOverview, tabFindPeaks, tabHistogramProperty, tabQuantify = st.tabs(
        ["Histogram Overview", "Peak Finder", "Properties", "Quantification"]
    )

    @st.cache_data
    def directory():
        path = askdirectory(title="select folder with data")  ## folder 'data'
        return path

    @st.cache_data
    def load_histograms(path_bulk_histogram):
        """Load the bulk histograms from the h5ad file and convert it to a DataFrame."""
        print("path histograms:", path_bulk_histogram)
        histogram_ds = _load_ann_data(
            path_bulk_histogram, "h5ad bulk converted to DataFrame successfully."
        )
        initial_bins = len(histogram_ds.columns)

        return histogram_ds, initial_bins

    @st.cache_data
    def load_properties(path):
        """Load the properties from the csv file and convert it to a DataFrame."""
        path_and_name = os.path.join(path, "Properties.csv")
        properties_data = pd.read_csv(path_and_name, encoding="unicode_escape")
        return properties_data

    @st.cache_data
    def load_in_volume(_path_load_inner_histograms):
        """Load the Inner histograms from the h5ad file and convert it to a DataFrame."""
        return _load_ann_data(
            _path_load_inner_histograms,
            "h5ad inner histogram converted to DataFrame successfully.",
        )

    @st.cache_data
    def load_out_volume(_path_load_outer_histograms):
        """Load the Outer histograms from the h5ad file and convert it to a DataFrame."""
        return _load_ann_data(
            _path_load_outer_histograms,
            "h5ad outer histogram converted to DataFrame successfully.",
        )

    @st.cache_data
    def load_mesh(_path_load_surface_mesh_histograms):
        """Load the Mesh data from the h5ad file and convert it to a DataFrame."""
        return _load_ann_data(
            _path_load_surface_mesh_histograms,
            "h5ad Surface mesh converted to DataFrame successfully.",
        )

    @st.cache_data
    def load_gradient(path_load_gradient):
        """Load the gradient from the csv file and convert it to a DataFrame."""
        gradient = pd.read_csv(path_load_gradient)
        gradient.index = gradient["label"]
        return gradient

    ############################### Online Plot #################################

    @st.cache_data
    def plot_histogram_overview(plot_data):
        colorStd = alt.Color(
            "frequency:Q",
            scale=alt.Scale(scheme="viridis", domainMax=0.06),
            legend=alt.Legend(orient="bottom"),
            title="Frequency",
        )
        particleNumber = alt.X("X:N", title="Region")
        greyBin = alt.Y("Y:O", title="Binned Greyscale").bin(maxbins=52)
        heatMapPartSelect = alt.selection_point(
            encodings=["x"], fields=["X"]
        )  # to select points on a trigger defined in "encodings", e.g. XY position
        opacitySelection = alt.condition(
            heatMapPartSelect, alt.value(1.0), alt.value(0.2)
        )
        plotAllHistograms = (
            alt.Chart(plot_data, width=1500, height=1000)
            .mark_area(opacity=0.3)
            .encode(
                x=alt.X("Y", title="Greyscale"),
                y=alt.Y("frequency", title="Frequency").stack(None),
                color=(particleNumber),
                tooltip=("X"),
            )
            .transform_filter(heatMapPartSelect)
            .interactive(bind_x=False, bind_y=True)
        )
        heatMapHistograms = (
            alt.Chart(plot_data, width=900, height=900)
            .mark_rect()
            .encode(
                x=particleNumber,
                y=greyBin,
                color=colorStd,
                opacity=opacitySelection,
                tooltip=("X", "Y"),
            )
            .add_params(heatMapPartSelect)
            .interactive()
        )
        plot = plotAllHistograms | heatMapHistograms
        st.altair_chart(plot, use_container_width=True)

    @st.cache_data
    def plot_peaks(plot_data, peaks_df):
        particleNumber = alt.X("X:N", title="Region")
        plotAllHistograms = (
            alt.Chart(plot_data, width=1000, height=500)
            .mark_line()
            .encode(
                x=alt.X("Y", title="Greyscale"),
                y=alt.Y("frequency", title="Frequency"),
                color=(particleNumber),
                tooltip=("X"),
            )
            .interactive(bind_x=True, bind_y=True)
        )
        peak1Marks = (
            alt.Chart(peaks_df, width=1000, height=500)
            .mark_circle(color="#7fc97f", size=200, opacity=0.85)
            .encode(
                x=alt.X("Peak_1", title="Greyscale"),
                y=alt.Y("Peaks_Height_1", title="Frequency"),
            )
        )
        peak2Marks = (
            alt.Chart(peaks_df, width=1000, height=500)
            .mark_circle(color="#beaed4", size=200, opacity=0.85)
            .encode(
                x=alt.X("Peak_2", title="Greyscale"),
                y=alt.Y("Peaks_Height_2", title="Frequency"),
            )
        )
        peak3Marks = (
            alt.Chart(peaks_df, width=1000, height=500)
            .mark_circle(color="#fdc086", size=200, opacity=0.85)
            .encode(
                x=alt.X("Peak_3", title="Greyscale"),
                y=alt.Y("Peaks_Height_3", title="Frequency"),
            )
        )
        peak4Marks = (
            alt.Chart(peaks_df, width=1000, height=500)
            .mark_circle(color="yellow", size=200, opacity=0.85)
            .encode(
                x=alt.X("Peak_4", title="Greyscale"),
                y=alt.Y("Peaks_Height_4", title="Frequency"),
            )
        )
        peak5Marks = (
            alt.Chart(peaks_df, width=1000, height=500)
            .mark_circle(color="#386cb0", size=200, opacity=0.85)
            .encode(
                x=alt.X("Peak_5", title="Greyscale"),
                y=alt.Y("Peaks_Height_5", title="Frequency"),
            )
        )
        plot = (
            plotAllHistograms
            + peak1Marks
            + peak2Marks
            + peak3Marks
            + peak4Marks
            + peak5Marks
        )
        with st.container():
            st.altair_chart(plot, use_container_width=True)

    def plot_properties():  # Plot in the properties tab
        colorStd2 = alt.Color(
            "X:N",
            scale=alt.Scale(scheme="accent"),
            legend=alt.Legend(title="Region Label", orient="bottom"),
        )
        colorStd3 = alt.Color(
            propertiesColor,
            scale=alt.Scale(scheme="spectral"),
            legend=alt.Legend(title="Color Property", orient="bottom"),
        )
        colorStd4 = alt.Color("label:N", scale=alt.Scale(scheme="accent"), legend=None)
        sizeStd1 = alt.Size(
            propertiesSize, legend=alt.Legend(title="Size Property", orient="bottom")
        )
        listOfregions = [
            st.session_state["Particle_X"],
            st.session_state["Particle_A"],
            st.session_state["Particle_B"],
            st.session_state["Particle_C"],
            st.session_state["Particle_D"],
            st.session_state["Particle_E"],
            st.session_state["Particle_F"],
        ]
        plotHist2 = (
            alt.Chart(st.session_state["plotSubData1"], height=1000)
            .mark_line()
            .encode(
                x=alt.X("Y", title="Greyscale"),
                y=alt.Y("frequency", title="Frequency"),
                color=colorStd2,
            )
            .transform_filter(alt.FieldOneOfPredicate(field="X", oneOf=listOfregions))
            .interactive()
        )
        plotPropSelect = (
            alt.Chart(st.session_state["propAndPeaksAll"], height=1000)
            .mark_point(filled=True, opacity=1)
            .encode(x=propertiesX, y=propertiesY, size=propertiesSize, color=colorStd4)
            .transform_filter(
                alt.FieldOneOfPredicate(field="label", oneOf=listOfregions)
            )
        )
        plotPropAll = (
            alt.Chart(st.session_state["propAndPeaksAll"])
            .mark_point(shape="triangle", opacity=0.3)
            .encode(x=propertiesX, y=propertiesY, color=colorStd3, size=sizeStd1)
            .interactive()
        )
        plotProp = plotPropAll + plotPropSelect
        with tabHistogramProperty:
            colHist, colProp = st.columns(2)
            with colHist:
                st.altair_chart(plotHist2, use_container_width=True)
            with colProp:
                st.altair_chart(plotProp, use_container_width=True)

    def plot_mineralogy(report):
        """Plots the mineralogy from the report"""
        # convert report to DataFrame
        mineral_mass = pd.DataFrame(
            {
                "mineral": ["A", "B", "C", "D", "E"],
                "value": [
                    report["phaseA"],
                    report["phaseB"],
                    report["phaseC"],
                    report["phaseD"],
                    report["phaseE"],
                ],
            }
        )
        mineral_surface = pd.DataFrame(
            {
                "Surface": ["A", "B", "C", "D", "E"],
                "value": [
                    report["surfaceA"],
                    report["surfaceB"],
                    report["surfaceC"],
                    report["surfaceD"],
                    report["surfaceE"],
                ],
            }
        )

        # define color schema
        color_std_mass = alt.Color(
            "mineral:N",
            scale=alt.Scale(scheme="accent"),
            legend=alt.Legend(title="Mass", orient="right"),
        )
        color_std_surface = alt.Color(
            "Surface:N",
            scale=alt.Scale(scheme="accent"),
            legend=alt.Legend(title="Surface", orient="right"),
        )

        # define plots
        mineral_plot_mass = (
            alt.Chart(mineral_mass, title="Mass %")
            .mark_arc()
            .encode(theta="value", color=color_std_mass)
        )
        mineral_plot_surface = (
            alt.Chart(mineral_surface, title="Surface %")
            .mark_arc()
            .encode(theta="value", color=color_std_surface)
        )

        # combine plots
        combined_plot = mineral_plot_mass & mineral_plot_surface

        # plot
        st.altair_chart(combined_plot, use_container_width=True)

    def plot_peaks_balls(properties_and_peaks):
        PaP = pd.DataFrame(properties_and_peaks)
        allPeaks = pd.concat(
            [
                PaP["Peak_1"],
                PaP["Peak_2"],
                PaP["Peak_3"],
                PaP["Peak_4"],
                PaP["Peak_5"],
                PaP["Peak_6"],
            ],
            ignore_index=True,
        )
        countsTotal = pd.DataFrame({"counts": (allPeaks.value_counts())})
        countsTotal = countsTotal.reset_index()
        countsTotal = countsTotal.drop(0)
        greyBin = alt.X("index:Q", title="Greyscale")
        testPeakBalls = (
            alt.Chart(countsTotal, height=300)
            .mark_circle(opacity=0.8, stroke="black", strokeWidth=2, strokeOpacity=0.4)
            .encode(
                x=greyBin,
                size="counts:N",
                color=alt.Color(
                    "counts:N",
                    scale=alt.Scale(scheme="viridis"),
                    legend=alt.Legend(title="count", orient="bottom"),
                ),
            )
            .properties(width=450, height=180)
            .configure_axisX(grid=True)
            .configure_view(stroke=None)
            .interactive()
        )
        st.altair_chart(testPeakBalls, use_container_width=True)

    def save_label_list(data_directory):
        """Save the label List csv to disk."""
        labels_array = np.array(
            [
                st.session_state["Particle_A"],
                st.session_state["Particle_B"],
                st.session_state["Particle_C"],
                st.session_state["Particle_D"],
                st.session_state["Particle_E"],
                st.session_state["Particle_F"],
            ]
        )

        if (
            st.session_state["Particle_X"] > 0
        ):  # add a specific particle to the random dataset. Be sure the label exists
            labels_array = np.append(labels_array, st.session_state["Particle_X"])

        labels_array = np.sort(labels_array)
        filtered_ROI_properties = propertiesData.loc[labels_array]
        filtered_ROI_properties = filtered_ROI_properties.filter(
            [
                "bbox-0",
                "bbox-1",
                "bbox-2",
                "bbox-3",
                "bbox-5",
                "centroid-0",
                "centroid-1",
                "centroid-2",
            ],
            axis=1,
        )
        filtered_ROI_properties["Label Index"] = labels_array
        path_label_list = os.path.join(data_directory, "labelList.csv")
        filtered_ROI_properties.to_csv(path_label_list, index=False)

    # additional buttons
    buttRandomize = st.sidebar.button("Randomize")

    # initialize session state variables
    if "list6regions" not in st.session_state:
        st.session_state["list6regions"] = []
    if "subData_binned" not in st.session_state:
        st.session_state["subData_binned"] = []
    if "Particle_X" not in st.session_state:
        st.session_state["Particle_X"] = 0
    if "PropertiesAndPeaks" not in st.session_state:
        st.session_state["PropertiesAndPeaks"] = []
    if "regionsAnalysed" not in st.session_state:
        st.session_state["regionsAnalysed"] = 0

    number_regions = len(histogramsData)
    st.sidebar.metric(
        label="Number of regions",
        value=number_regions,
        help="Total number of regions loaded from the histogram file",
    )

    num_bins_input = st.sidebar.number_input(
        "Bins",
        value=256,
        max_value=initialBins,
        step=16,
        help="Number to be divided by the initial number of bins. The higher the input the less number of bins plotted",
    )

    number_bins = int(initialBins / num_bins_input)

    savgol_window_length = st.sidebar.slider(
        "Savgol smoothing intensity",
        min_value=3,
        value=parameters_dict["savgolInput"],
        max_value=26,
        help="This slider is not interactive! The new input is only visible in the plot after pressing randomize. Tip: higher values increase the smoothness",
    )

    numbPartSubData = st.sidebar.number_input(
        "Number of regions in subset",
        value=3,
        min_value=3,
        max_value=number_regions,
        step=2,
    )

    Peak_Width = st.sidebar.slider(
        label="Grey-value width",
        max_value=int(number_bins / 10),
        min_value=0,
        step=1,
        value=int(parameters_dict["gray_value_width"]),
        help="Distance between two valleys on either side of a peak",
    )

    Peak_Height = st.sidebar.slider(
        label="Min. Frequency",
        max_value=0.1,
        min_value=0.0,
        value=float(parameters_dict["min_frequency"]),
        step=0.001,
        format="%f",
        help="Minimum height of peaks from bottom",
    )

    Peak_Prominence = st.sidebar.slider(
        label="Frequency prominence",
        max_value=0.05,
        min_value=0.00,
        value=float(parameters_dict["prominence"]),
        step=0.002,
        format="%f",
        help="Minimum height of climb from a valley left or right from the peak",
    )

    Peak_Horizontal_Distance = st.sidebar.slider(
        label="Grey-value variation",
        max_value=int(number_bins - (number_bins * 0.3)),
        min_value=1,
        value=int(parameters_dict["horizDistance"]),
        step=1,
        help="Minimum horizontal distance between neighbour peaks",
    )

    Peak_Vertical_Distance = st.sidebar.slider(
        label="Frequency variation",
        max_value=0.005,
        min_value=0.000,
        value=float(parameters_dict["vertDistance"]),
        step=0.0002,
        format="%f",
        help="Minimum vertical distance between neighbour peaks",
    )
    buttRunAll = st.sidebar.button(
        label="Quantify all",
        help="Applies the peak parameters to all regions and appends the grey-values of the peaks to the properties file. Must be pressed for the new thresholds to take effect",
    )
    plotDataButton = st.sidebar.radio(
        "How many regions",
        ["All regions", "Random regions", "Regions of interest"],
        index=2,
    )

    ################## online functionality ##################
    with tabHistOverview:
        (
            colLoad,
            colSave,
            colSavgol,
            colA,
            colB,
            colC,
            colD,
            colE,
            colF,
            colX,
        ) = st.columns(10)

        # histogram smoothing checkbox
        with colSavgol:
            savgolBox = st.checkbox(
                "Activate Savgol",
                value=parameters_dict["enableSavgol"],
                help="Smoothens the histograms. Use together with slider in the sidebar",
            )

        # Load label regions
        with colLoad:
            buttLoadListLabels = st.button(
                "Load regions",
                help="Loads a list of labels as csv created in the 3D viewer",
            )
        # save label regions
        with colSave:
            buttSaveListLabels = st.button(
                "Save regions",
                help="Saves a list of labels as csv that are loaded automatically in the 3D viewer",
            )

    # initiation condition creates 3 random regions
    if (
        "particleLabels" not in st.session_state
        or "plotSubData1" not in st.session_state
    ):
        (
            histogramsSubData,
            st.session_state["particleLabels"],
        ) = create_histogram_subdata(
            numbPartSubData, histogramsData, st.session_state["Particle_X"]
        )
        startTime = time.time()

        histograms_binned = binning(num_bins_input, histogramsSubData, n_jobs=-1)
        if savgolBox:
            savgol_smoothed_ds = smooth_histograms_savgol(
                histograms_binned, savgol_window_length, n_jobs=-1
            )
            normalized_histograms_ds = normalize_volume(savgol_smoothed_ds)
        else:
            normalized_histograms_ds = normalize_volume(histograms_binned)

        # update session states
        st.session_state["plotSubData1"] = transform_columns_xy(
            normalized_histograms_ds
        )
        st.session_state["NormalizedSubData"] = normalized_histograms_ds

        finishTime = time.time()
        print("plot selected data in s:", finishTime - startTime)

    with tabFindPeaks:  # table with threshold inputs
        col1, col2 = st.columns(spec=[0.8, 0.2])
        with col2:
            loadInputFiles = st.file_uploader(
                label="Load input densities and thresholds",
                help="Thresholds and densities can be loaded from a csv pre-saved from the table. IMPORTANT: if file is loaded, changes on the table will not take effect. Delete file to interactively see changes in the plot",
            )
        with col1:
            st.subheader("Greyvalue phase thresholds and densities")
            if loadInputFiles:
                inputsLoaded = pd.read_csv(loadInputFiles)
                inputsLoaded = inputsLoaded.drop(inputsLoaded.columns[0], axis=1)
                print("input table", inputsLoaded)
                inputstable = st.data_editor(inputsLoaded)
                print(inputstable)
                inputDensityA = int(inputsLoaded.iloc[0]["DensityA"])
                inputDensityB = int(inputsLoaded.iloc[0]["DensityB"])
                inputDensityC = int(inputsLoaded.iloc[0]["DensityC"])
                inputDensityD = int(inputsLoaded.iloc[0]["DensityD"])
                inputDensityE = int(inputsLoaded.iloc[0]["DensityE"])
                background_peak = int(inputsLoaded.iloc[0]["BackgroundT"])
                Phase_1_threshold = int(inputsLoaded.iloc[0]["Max greyvalue A"])
                Phase_2_threshold = int(inputsLoaded.iloc[0]["Max greyvalue B"])
                Phase_3_threshold = int(inputsLoaded.iloc[0]["Max greyvalue C"])
                Phase_4_threshold = int(inputsLoaded.iloc[0]["Max greyvalue D"])
                Phase_5_threshold = int(inputsLoaded.iloc[0]["Max greyvalue E"])
                print("greyC", int(inputsLoaded.iloc[0]["Max greyvalue C"]))
                print("threshold3", Phase_3_threshold)
            else:
                input4Quantification = pd.DataFrame([input4Quantification])
                inputs = st.data_editor(input4Quantification)
                input4Quantification = inputs.to_dict(orient="records")[0]
                inputDensityA = input4Quantification["DensityA"]
                inputDensityB = input4Quantification["DensityB"]
                inputDensityC = input4Quantification["DensityC"]
                inputDensityD = input4Quantification["DensityD"]
                inputDensityE = input4Quantification["DensityE"]
                background_peak = input4Quantification["BackgroundT"]
                Phase_1_threshold = input4Quantification["Max greyvalue A"]
                Phase_2_threshold = input4Quantification["Max greyvalue B"]
                Phase_3_threshold = input4Quantification["Max greyvalue C"]
                Phase_4_threshold = input4Quantification["Max greyvalue D"]
                Phase_5_threshold = input4Quantification["Max greyvalue E"]

    if "plotAllData" not in st.session_state:
        startTime = time.time()
        histograms_binned = binning(num_bins_input, histogramsData, n_jobs=-1)
        if savgolBox:
            savgol_smoothed_ds = smooth_histograms_savgol(
                histograms_binned, savgol_window_length, n_jobs=-1
            )  ############# Savgol filter applied if the slider input is >1
            st.session_state["NormalizedData"] = normalize_volume(savgol_smoothed_ds)
        else:
            st.session_state["NormalizedData"] = normalize_volume(histograms_binned)
        st.session_state["plotAllData"] = transform_columns_xy(
            st.session_state["NormalizedData"]
        )
        # normalized_data, histograms_data, properties, number_bins, peak_width, peak_height, peak_prominence,
        #                   peak_vertical_distance, peak_horizontal_distance

        PeaksSubData = process_peaks(
            st.session_state["NormalizedData"],
            histogramsData,
            propertiesData,
            number_bins,
            Peak_Width,
            Peak_Height,
            Peak_Prominence,
            Peak_Vertical_Distance,
            Peak_Horizontal_Distance,
            num_bins_input,
        )
        st.session_state["propAndPeaksAll"] = arrange_peaks(
            PeaksSubData,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
            Phase_5_threshold,
            background_peak,
            propertiesData,
        )
        finishTime = time.time()
        print("plotAllData:", finishTime - startTime)

    propertiesAndPeaks = st.session_state["propAndPeaksAll"]
    if buttRandomize:  # creates a random list of regions st.['regionsLabels']
        (
            histogramsSubData,
            st.session_state["particleLabels"],
        ) = create_histogram_subdata(
            numbPartSubData, histogramsData, st.session_state["Particle_X"]
        )
        startTime = time.time()
        histograms_binned = binning(num_bins_input, histogramsSubData, n_jobs=-1)
        if savgolBox:
            savgol_smoothed_ds = smooth_histograms_savgol(
                histograms_binned, savgol_window_length, n_jobs=-1
            )  ############# Savgol filter applied if the slider input is >1
            st.session_state["NormalizedSubData"] = normalize_volume(savgol_smoothed_ds)
        else:
            st.session_state["NormalizedSubData"] = normalize_volume(histograms_binned)
        st.session_state["plotSubData1"] = transform_columns_xy(
            st.session_state["NormalizedSubData"]
        )
        finishTime = time.time()
        print("plotSubData1:", finishTime - startTime)

    if (
        buttLoadListLabels
    ):  # Loads list of region labelsfrom CSV, regions A to F created either from 'Histograms Overview' tab or from Napari
        sub_data_from_list, st.session_state["particleLabels"] = load_label_list(
            dataDirectory
        )
        startTime = time.time()
        histograms_binned = binning(num_bins_input, sub_data_from_list, n_jobs=-1)
        if savgolBox:
            savgol_smoothed_ds = smooth_histograms_savgol(
                histograms_binned, savgol_window_length, n_jobs=-1
            )
            st.session_state["Normalized6regions"] = normalize_volume(
                savgol_smoothed_ds
            )

        else:
            st.session_state["Normalized6regions"] = normalize_volume(histograms_binned)
        st.session_state["plotDataFromList"] = transform_columns_xy(
            st.session_state["Normalized6regions"]
        )
        finishTime = time.time()
        print("plotted selected data in s: ", finishTime - startTime)

        # update session variables
        st.session_state["list6regions"] = st.session_state["particleLabels"]

    with tabHistOverview:
        lenghtOfList = len(st.session_state["particleLabels"])
        with colX:
            particleNumberBox = st.number_input(
                "Label particle X",
                step=1,
                help="specific region label. Does not need to be in the random dataset, but the label must exist in the full dataset",
            )
            st.session_state["Particle_X"] = particleNumberBox
        with colA:
            st.session_state["Particle_A"] = st.selectbox(
                label="Label Region A",
                options=st.session_state["particleLabels"],
                index=0,
            )
        with colB:
            st.session_state["Particle_B"] = st.selectbox(
                label="Label Region B",
                options=st.session_state["particleLabels"],
                index=1,
            )
        with colC:
            st.session_state["Particle_C"] = st.selectbox(
                label="Label Region C",
                options=st.session_state["particleLabels"],
                index=2,
            )
        with colD:
            if lenghtOfList > 3:
                dropdown4 = st.selectbox(
                    label="Label Region D",
                    options=st.session_state["particleLabels"],
                    index=3,
                )
            else:
                dropdown4 = st.selectbox(
                    label="Label Region D",
                    options=st.session_state["particleLabels"],
                    index=0,
                )
            st.session_state["Particle_D"] = dropdown4
        with colE:
            if lenghtOfList > 4:
                dropdown5 = st.selectbox(
                    label="Label Region E",
                    options=st.session_state["particleLabels"],
                    index=4,
                )
            else:
                dropdown5 = st.selectbox(
                    label="Label Region E",
                    options=st.session_state["particleLabels"],
                    index=0,
                )
            st.session_state["Particle_E"] = dropdown5
        with colF:
            if lenghtOfList > 5:
                dropdown6 = st.selectbox(
                    label="Label Region F",
                    options=st.session_state["particleLabels"],
                    index=5,
                )
            else:
                dropdown6 = st.selectbox(
                    label="Label Region F",
                    options=st.session_state["particleLabels"],
                    index=0,
                )
            st.session_state["Particle_F"] = dropdown6
        list6regions = {
            "Label Index": [
                st.session_state["Particle_A"],
                st.session_state["Particle_B"],
                st.session_state["Particle_C"],
                st.session_state["Particle_D"],
                st.session_state["Particle_E"],
                st.session_state["Particle_F"],
            ]
        }
        st.session_state["list6regions"] = pd.DataFrame(list6regions)
        histograms6regions = histogramsData[
            histogramsData.index.isin(list6regions["Label Index"])
        ]

        if (
            plotDataButton == "Regions of interest"
            or "plotDataFromList" not in st.session_state
        ):
            startTime = time.time()
            histograms_binned = binning(num_bins_input, histograms6regions, n_jobs=-1)
            if savgolBox:
                savgol_smoothed_ds = smooth_histograms_savgol(
                    histograms_binned, savgol_window_length, n_jobs=-1
                )  ############# Savgol filter applied if the slider input is >1
                normalized_histograms_ds = normalize_volume(savgol_smoothed_ds)
            else:
                normalized_histograms_ds = normalize_volume(histograms_binned)
            st.session_state["plotDataFromList"] = transform_columns_xy(
                normalized_histograms_ds
            )
            st.session_state["Normalized6regions"] = normalized_histograms_ds
            finishTime = time.time()
            print("plot selected data in s:", finishTime - startTime)
            plot_histogram_overview(st.session_state["plotDataFromList"])
            with st.expander("Histograms regions of interest"):
                st.dataframe(st.session_state["Normalized6regions"], hide_index=True)

        if plotDataButton == "Random regions":
            plot_histogram_overview(st.session_state["plotSubData1"])
            with st.expander("Histograms of random regions"):
                st.dataframe(st.session_state["NormalizedSubData"], hide_index=True)

        if plotDataButton == "All regions":
            plot_histogram_overview(st.session_state["plotAllData"])
            with st.expander("Histograms all regions"):
                st.dataframe(st.session_state["NormalizedData"], hide_index=True)

    if buttSaveListLabels:
        save_label_list(dataDirectory)

    with tabFindPeaks:  # table with threshold inputs
        with col1:
            if plotDataButton == "Regions of interest":
                PeaksSubData = process_peaks(
                    st.session_state["Normalized6regions"],
                    histogramsData,
                    propertiesData,
                    number_bins,
                    Peak_Width,
                    Peak_Height,
                    Peak_Prominence,
                    Peak_Vertical_Distance,
                    Peak_Horizontal_Distance,
                    num_bins_input,
                )
                st.session_state["propAndPeaksROI"] = arrange_peaks(
                    PeaksSubData,
                    Phase_1_threshold,
                    Phase_2_threshold,
                    Phase_3_threshold,
                    Phase_4_threshold,
                    Phase_5_threshold,
                    background_peak,
                    propertiesData,
                )
                plot_peaks(
                    st.session_state["plotDataFromList"],
                    st.session_state["propAndPeaksROI"],
                )
            if plotDataButton == "Random regions":
                PeaksSubData = process_peaks(
                    st.session_state["NormalizedSubData"],
                    histogramsData,
                    propertiesData,
                    number_bins,
                    Peak_Width,
                    Peak_Height,
                    Peak_Prominence,
                    Peak_Vertical_Distance,
                    Peak_Horizontal_Distance,
                    num_bins_input,
                )
                st.session_state["propAndPeaksRandom"] = arrange_peaks(
                    PeaksSubData,
                    Phase_1_threshold,
                    Phase_2_threshold,
                    Phase_3_threshold,
                    Phase_4_threshold,
                    Phase_5_threshold,
                    background_peak,
                    propertiesData,
                )
                plot_peaks(
                    st.session_state["plotSubData1"],
                    st.session_state["propAndPeaksRandom"],
                )
            if plotDataButton == "All regions":
                PeaksSubData = process_peaks(
                    st.session_state["NormalizedData"],
                    histogramsData,
                    propertiesData,
                    number_bins,
                    Peak_Width,
                    Peak_Height,
                    Peak_Prominence,
                    Peak_Vertical_Distance,
                    Peak_Horizontal_Distance,
                    num_bins_input,
                )
                st.session_state["propAndPeaksAll"] = arrange_peaks(
                    PeaksSubData,
                    Phase_1_threshold,
                    Phase_2_threshold,
                    Phase_3_threshold,
                    Phase_4_threshold,
                    Phase_5_threshold,
                    background_peak,
                    propertiesData,
                )
                plot_peaks(
                    st.session_state["plotAllData"], st.session_state["propAndPeaksAll"]
                )
        with col2:
            if plotDataButton == "Random regions":
                with st.expander("List of Peaks"):
                    st.dataframe(st.session_state["propAndPeaksRandom"])
            if plotDataButton == "All regions":
                with st.expander("List of Peaks"):
                    st.dataframe(st.session_state["propAndPeaksAll"])
            if plotDataButton == "Regions of interest":
                with st.expander("List of Peaks"):
                    st.dataframe(st.session_state["propAndPeaksROI"])

    if buttRunAll:
        with tabFindPeaks:
            with col1:
                plot_peaks_balls(st.session_state["propAndPeaksAll"])
            with col2:
                st.write(
                    "Number of peaks class A:",
                    propertiesAndPeaks["Peaks_Height_1"].astype(bool).sum(axis=0),
                )
                st.write(
                    "Number of peaks class B:",
                    propertiesAndPeaks["Peaks_Height_2"].astype(bool).sum(axis=0),
                )
                st.write(
                    "Number of peaks class C:",
                    propertiesAndPeaks["Peaks_Height_3"].astype(bool).sum(axis=0),
                )
                st.write(
                    "Number of peaks class D:",
                    propertiesAndPeaks["Peaks_Height_4"].astype(bool).sum(axis=0),
                )
                st.write(
                    "Number of peaks class E:",
                    propertiesAndPeaks["Peaks_Height_5"].astype(bool).sum(axis=0),
                )
        with tabQuantify:
            report, quantification = quantify_mineralogy(
                st.session_state["propAndPeaksAll"],
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            st.subheader("Statistics for all regions")
            col1Stats, col2PiePlot = st.columns(2)

            with col1Stats:
                # statistics for the mineral quantification
                totalParticleVolume = propertiesData["Volume"].sum()
                st.metric(
                    label="regions analysed",
                    value=report["regionsAnalysed"],
                    delta=number_regions,
                    delta_color="inverse",
                    help="If number of regions analysed is very different from the number of regions segmented means something is wrong with the classification. Check the peaks and thresholds",
                )
                st.metric(
                    label="Volume analysed",
                    value=round(report["volumeAnalysed2"], 0),
                    delta=round(
                        report["volumeAnalysed"] / report["volumeAnalysed2"], 2
                    ),
                    delta_color="inverse",
                    help=" compare volume fraction analysed = volume analysed / total volume",
                )
                st.metric(
                    label="Number regions liberated",
                    value=report["regionsLiberated"],
                    help="regions with only one phase",
                )
                st.metric(
                    label="Number regions with 2 phases", value=report["regions2Phases"]
                )
                st.metric(
                    label="Number regions with more than 2 phases",
                    value=report["regions3Phases"],
                    help="partial volume not corrected",
                )
                print(report["volumeAnalysed"])
                print(report["volumeAnalysed2"])
                print(totalParticleVolume)

            with col2PiePlot:
                # plot area of the mineralogy
                plot_mineralogy(report)

            # save report
            report_path = os.path.join(report_directory, "report.yml")
            write_dict_to_yml(report_path, report)

            # save quantification
            path_save_Quantification = os.path.join(
                report_directory, "Quantification.csv"
            )
            quantification.to_csv(path_save_Quantification, index=False)

    with tabHistogramProperty:
        colActivate, column1, column2, column3, column4 = st.columns(5)

        with colActivate:
            # activate property plot checkbox
            plotPropActive = st.checkbox("Plot properties", value=False)

        if plotPropActive:
            with column4:
                propertiesSize = st.selectbox(
                    "Size property", propertiesAndPeaks.columns[:].unique(), index=19
                )
            with column3:
                propertiesColor = st.selectbox(
                    "Color property", propertiesAndPeaks.columns[:].unique(), index=14
                )
            with column2:
                propertiesY = st.selectbox(
                    "Y-property", propertiesAndPeaks.columns[:].unique(), index=16
                )
            with column1:
                propertiesX = st.selectbox(
                    "X-property", propertiesAndPeaks.columns[:].unique(), index=12
                )
            plot_properties()

        with st.expander("Properties And Peaks"):
            # option to look at hte properties and peaks dataset
            st.dataframe(st.session_state["propAndPeaksAll"])

    with tabFindPeaks:
        colPartA, colPartB, colPartC, colPartD, colPartE, colPartF = st.columns(6)
        with colPartA:
            PropWPeak_A = propertiesAndPeaks.loc[[st.session_state["Particle_A"]]]
            st.subheader(st.session_state["Particle_A"])
            report, _ = quantify_mineralogy(
                PropWPeak_A,
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            plot_mineralogy(report)
        with colPartB:
            PropWPeak_B = propertiesAndPeaks.loc[[st.session_state["Particle_B"]]]
            st.subheader(st.session_state["Particle_B"])
            report, _ = quantify_mineralogy(
                PropWPeak_B,
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            plot_mineralogy(report)
        with colPartC:
            PropWPeak_C = propertiesAndPeaks.loc[[st.session_state["Particle_C"]]]
            st.subheader(st.session_state["Particle_C"])
            report, _ = quantify_mineralogy(
                PropWPeak_C,
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            plot_mineralogy(report)
        with colPartD:
            PropWPeak_D = propertiesAndPeaks.loc[[st.session_state["Particle_D"]]]
            st.subheader(st.session_state["Particle_D"])
            report, _ = quantify_mineralogy(
                PropWPeak_D,
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            plot_mineralogy(report)
        with colPartE:
            PropWPeak_E = propertiesAndPeaks.loc[[st.session_state["Particle_E"]]]
            st.subheader(st.session_state["Particle_E"])
            report, _ = quantify_mineralogy(
                PropWPeak_E,
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            plot_mineralogy(report)
        with colPartF:
            PropWPeak_F = propertiesAndPeaks.loc[[st.session_state["Particle_F"]]]
            st.subheader(st.session_state["Particle_F"])
            report, _ = quantify_mineralogy(
                PropWPeak_F,
                background_peak,
                Peak_Height,
                histogramsData,
                inputDensityA,
                inputDensityB,
                inputDensityC,
                inputDensityD,
                inputDensityE,
            )
            plot_mineralogy(report)
