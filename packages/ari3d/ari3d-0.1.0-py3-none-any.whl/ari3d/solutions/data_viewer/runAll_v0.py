import os
from pathlib import Path

import anndata
import numpy as np
import pandas as pd
import yaml
from joblib import Parallel, delayed
from scipy.signal import find_peaks, savgol_filter
from tqdm import tqdm

############################### load data


def load_histograms(path_load_bulk_histogram):
    """Load the bulk histograms from the h5ad file and convert it to a DataFrame."""
    print("path histograms:", path_load_bulk_histogram)
    try:
        adata = anndata.read_h5ad(path_load_bulk_histogram, backed="r")
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
        print("h5ad bulk converted to DataFrame successfully.")
        initial_bins = len(df.columns)
        return df, initial_bins
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")


def load_properties(path):
    path_and_name = os.path.join(path, "Properties.csv")
    properties_data = pd.read_csv(path_and_name, encoding="unicode_escape")
    return properties_data


def load_properties_with_peaks(path):
    path_and_name = os.path.join(path, "PropertyAndPeaks.csv")
    properties_data = pd.read_csv(path_and_name, encoding="unicode_escape")
    return properties_data


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


def load_in_volume(_path_load_inner_histograms):
    return _load_ann_data(
        _path_load_inner_histograms,
        "h5ad inner histogram converted to DataFrame successfully.",
    )


def load_out_volume(_path_load_outer_histograms):
    return _load_ann_data(
        _path_load_outer_histograms,
        "h5ad outer histogram converted to DataFrame successfully.",
    )


def load_mesh(_path_load_surface_mesh_histograms):
    return _load_ann_data(
        _path_load_surface_mesh_histograms,
        "h5ad Surface mesh converted to DataFrame successfully.",
    )


def load_gradient(path_load_gradient):
    gradient = pd.read_csv(path_load_gradient)
    gradient.index = gradient["label"]
    return gradient


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
    file1 = Parallel(n_jobs=n_jobs)(
        delayed(process_histogram_row)(row, histograms_data_int, bin_input)
        for _, row in tqdm(
            histograms_data.iterrows(),
            total=histograms_data.shape[0],
            desc="Processing Rows",
        )
    )
    # Convert lists to DataFrames
    rang = int(round(len(histograms_data.columns) / bin_input))
    x = np.linspace(0, len(histograms_data.columns) - 1, rang - 1).astype(int)
    file1 = np.array(file1).reshape(len(file1), -1)
    file1 = pd.DataFrame(file1, columns=x)
    file1.index = histograms_data.index
    file1[file1 < 0] = 0
    return file1


def normalize_volume(un_normalized):
    un_normalized = pd.DataFrame(un_normalized)
    df_new = un_normalized.loc[:, :].div(un_normalized.sum(axis=1), axis=0)
    df_new = df_new.fillna(0)
    return df_new


def smooth_histograms_savgol(binned_histograms, savgol_input, n_jobs=-1):
    smoothed_file1 = Parallel(n_jobs=n_jobs)(
        delayed(
            lambda row: savgol_filter(row, window_length=savgol_input, polyorder=3)
        )(row)
        for _, row in tqdm(
            binned_histograms.iterrows(),
            total=binned_histograms.shape[0],
            desc="Smoothing Rows",
        )
    )
    file1 = pd.DataFrame(
        smoothed_file1, columns=binned_histograms.columns, index=binned_histograms.index
    )
    # Clip negative values to 0
    file1[file1 < 0] = 0
    # Ensure integer values if required
    file1 = file1.astype(int)
    return file1


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
        peak_pos = peak_pos * binInput

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


def quantify_liberatedregions(
    surface_mesh_subdata,
    subdata_properties,
    background_peak,
    phase_1_threshold,
    phase_2_threshold,
    phase_3_threshold,
    phase_4_threshold,
    regionsAnalysed,
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
            # linear equation from peak position to background. creates a list (then array) with each entry is the result of the equation
            multiples_towards_background_phase_1 = np.linspace(
                0, 1, Partical_peak - background_peak
            )
            No_of_voxels_towards_background_phase_1 = row.iloc[
                background_peak:Partical_peak
            ]
            if len(No_of_voxels_towards_background_phase_1) != len(
                multiples_towards_background_phase_1
            ):
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
    return Quantification_1_phase_sorted, regionsLiberated, regionsAnalysed


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

            if len(multiples_towards_Partical_peak_1) > len(No_of_voxels):
                multiples_towards_Partical_peak_1 = np.delete(
                    multiples_towards_Partical_peak_1, 0
                )
            elif len(multiples_towards_Partical_peak_1) < len(No_of_voxels):
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


def quantify_mineralogy(properties_data_w_peaks, background_peak, Peak_Height):
    properties_data_w_peaks = pd.DataFrame(properties_data_w_peaks)
    partList = properties_data_w_peaks.index.to_list()

    # filter the histogram data to contain only the particles for which a valid peak was found
    OutHistogram_Subdata = outer_volume_histograms.loc[partList]
    SurfaceMesh_Subdata = surface_mesh_histogram.loc[partList]
    InHistogram_Subdata = inner_volume_histograms.loc[partList]
    Histograms_Subdata = histogramsData.loc[partList]
    Gradient_Subdata = gradient.loc[partList]

    # subdata_properties is a subdataset from properties that contains only the peaks
    subdata_properties = _update_peak_positions(
        properties_data_w_peaks, background_peak, Peak_Height
    )

    # counter variables
    regions3Phases = 0
    regionsAnalysed = 0
    volumeAnalysed = 0

    regionsLiberated = 0
    surfaceAnalysed = 0
    surfaceA = 0
    surfaceB = 0
    surfaceC = 0
    surfaceD = 0
    surfaceE = 0
    phaseA = 0
    phaseB = 0
    phaseC = 0
    phaseD = 0
    phaseE = 0
    phaseA_mass = 0
    phaseB_mass = 0
    phaseC_mass = 0
    phaseD_mass = 0
    phaseE_mass = 0
    (
        Liberated_quantification,
        regionsLiberated,
        regionsAnalysed,
    ) = quantify_liberatedregions(
        SurfaceMesh_Subdata,
        subdata_properties,
        background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        regionsAnalysed,
    )
    (
        Binary_quantification,
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
        Ternary_quantification,
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
    (
        Quaternary_quantification,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    ) = quaternary_regions(
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
    (
        Quinary_quantification,
        regionsAnalysed,
        volumeAnalysed,
        regions3Phases,
    ) = quinary_regions(
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
    Liberated_quantification = arrange_columns(Liberated_quantification)
    Binary_quantification = arrange_columns(Binary_quantification)
    Ternary_quantification = arrange_columns(Ternary_quantification)
    Quaternary_quantification = arrange_columns(Quaternary_quantification)
    Quinary_quantification = arrange_columns(Quinary_quantification)

    Quantification = pd.concat(
        [
            Liberated_quantification,
            Binary_quantification,
            Ternary_quantification,
            Quaternary_quantification,
            Quinary_quantification,
        ],
        axis=0,
    )
    Quantification["Total_quantification"] = (
        Quantification["Phase_1_quantification"]
        + Quantification["Phase_2_quantification"]
        + Quantification["Phase_3_quantification"]
        + Quantification["Phase_4_quantification"]
        + Quantification["Phase_5_quantification"]
    )
    Quantification = Quantification.sort_index(ascending=True)
    surfaceA = Quantification["Phase_1_surface_quantification"].sum()
    surfaceB = Quantification["Phase_2_surface_quantification"].sum()
    surfaceC = Quantification["Phase_3_surface_quantification"].sum()
    surfaceD = Quantification["Phase_4_surface_quantification"].sum()
    surfaceE = Quantification["Phase_5_surface_quantification"].sum()

    phaseA_mass = Quantification["Phase_1_quantification"].sum() * inputDensityA
    phaseB_mass = Quantification["Phase_2_quantification"].sum() * inputDensityB
    phaseC_mass = Quantification["Phase_3_quantification"].sum() * inputDensityC
    phaseD_mass = Quantification["Phase_4_quantification"].sum() * inputDensityD
    phaseE_mass = Quantification["Phase_5_quantification"].sum() * inputDensityE

    volumeAnalysed2 = (
        Quantification["Phase_1_quantification"].sum()
        + Quantification["Phase_2_quantification"].sum()
        + Quantification["Phase_3_quantification"].sum()
        + Quantification["Phase_4_quantification"].sum()
        + Quantification["Phase_5_quantification"].sum()
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
        if col not in Quantification.columns or col == "Label"
    ]
    properties_data_w_peaks = properties_data_w_peaks[columns_to_keep]
    Quantification = pd.merge(
        Quantification, properties_data_w_peaks, left_index=True, right_index=True
    )
    # Path_save_Quantification = os.path.join(dataDirectory, 'Quantification.csv')
    # Quantification.to_csv(Path_save_Quantification, index=False)  ################################################# This should be in the report

    report = {
        "regions2Phases": str(regions2Phases),
        "regions3Phases": str(regions3Phases),
        "regionsAnalysed": str(regionsAnalysed),
        "volumeAnalysed2": str(volumeAnalysed2),
        "regionsLiberated": str(regionsLiberated),
        "volumeAnalysed": str(volumeAnalysed),
        "surfaceAnalysed": str(surfaceAnalysed),
        "totalMass": str(totalMass),
        "phaseA": str(phaseA),
        "phaseB": str(phaseB),
        "phaseC": str(phaseC),
        "phaseD": str(phaseD),
        "phaseE": str(phaseE),
        "phaseA_mass": str(phaseA_mass),
        "phaseB_mass": str(phaseB_mass),
        "phaseC_mass": str(phaseC_mass),
        "phaseD_mass": str(phaseD_mass),
        "phaseE_mass": str(phaseE_mass),
        "surfaceA": str(surfaceA),
        "surfaceB": str(surfaceB),
        "surfaceC": str(surfaceC),
        "surfaceD": str(surfaceD),
        "surfaceE": str(surfaceE),
    }

    return report, Quantification


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


############################### Load-Save Paths #################################

### histograms as h5ad
import sys

dataDirectory = sys.argv[1]
reportDirectory = sys.argv[1]
# load bulk histograms (= Inner + Outer)
path_load_bulk_histogram = os.path.join(dataDirectory, "Bulk_histograms.h5ad")
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

############################### Load data #################################

histogramsData, initialBins = load_histograms(path_load_bulk_histogram)
histogramsData = histogramsData.rename_axis("label")
histogramsData = histogramsData.astype("float64")
histogramsData = histogramsData.iloc[:, 1:]

propertiesData = load_properties(dataDirectory)
propertiesData.index = propertiesData["label"]

number_regions = len(
    histogramsData
)  ################################################################ OUTPUT 2nd report

inner_volume_histograms = load_in_volume(path_load_inner_histograms)
outer_volume_histograms = load_out_volume(path_load_outer_histograms)
surface_mesh_histogram = load_mesh(path_load_surface_mesh_histograms)
gradient = load_gradient(path_load_gradient)

################################## Define Inputs #################################

# peak finder function
sliderWidth = 0  ###################################################### Load value
Peak_Width = sliderWidth
sliderHeight = 0  ###################################################### Load value
Peak_Height = sliderHeight
Prominence = 0  ###################################################### Load value
Peak_Prominence = Prominence
horizDistance = 1  ###################################################### Load value
Peak_Horizontal_Distance = horizDistance
vertDistance = 0  ###################################################### Load value
Peak_Vertical_Distance = vertDistance
# peak_variables= {'Peak_Width'=sliderWidth,'Peak_Height'=sliderHeight,'Peak_Prominence'=Prominence,'Peak_Horizontal_Distance'=horizDistance,'Peak_Vertical_Distance'=vertDistance}

# table with threshold inputs
input4Quantification = {
    "BackgroundT": 600,
    "DensityA": 1,
    "Max greyvalue A": 6000,
    "DensityB": 1,
    "Max greyvalue B": 11111,
    "DensityC": 1,
    "Max greyvalue C": 22222,
    "DensityD": 1,
    "Max greyvalue D": 25555,
    "DensityE": 0,
    "Max greyvalue E": 65555,
}
inputDensityA = input4Quantification[
    "DensityA"
]  ###################################################### Load value
inputDensityB = input4Quantification[
    "DensityB"
]  ###################################################### Load value
inputDensityC = input4Quantification[
    "DensityC"
]  ###################################################### Load value
inputDensityD = input4Quantification[
    "DensityD"
]  ###################################################### Load value
inputDensityE = input4Quantification[
    "DensityE"
]  ###################################################### Load value
background_peak = input4Quantification[
    "BackgroundT"
]  ###################################################### Load value
Phase_1_threshold = input4Quantification[
    "Max greyvalue A"
]  ###################################################### Load value
Phase_2_threshold = input4Quantification[
    "Max greyvalue B"
]  ###################################################### Load value
Phase_3_threshold = input4Quantification[
    "Max greyvalue C"
]  ###################################################### Load value
Phase_4_threshold = input4Quantification[
    "Max greyvalue D"
]  ###################################################### Load value
Phase_5_threshold = input4Quantification[
    "Max greyvalue E"
]  ###################################################### Load value

binInput = 256  ###################################################### Load value
numberBins = int(initialBins / binInput)
savgolInput = 4  ###################################################### Load value
enable_savgol = False  ###################################################### Load value

################################## Process #################################

histograms_binned = binning(binInput, histogramsData, n_jobs=-1)

if (
    enable_savgol
):  ###################################################################### CHANGE condition
    savgolSmooth = smooth_histograms_savgol(histograms_binned, savgolInput, n_jobs=-1)
    NormalizedData = normalize_volume(savgolSmooth)
else:
    NormalizedData = normalize_volume(histograms_binned)

PeaksSubData = process_peaks(
    NormalizedData,
    histogramsData,
    propertiesData,
    numberBins,
    Peak_Width,
    Peak_Height,
    Peak_Prominence,
    Peak_Vertical_Distance,
    Peak_Horizontal_Distance,
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
    propertiesAndPeaks, background_peak, Peak_Height
)
# add particle volume to report
report["totalParticleVolume"] = str(propertiesData["Volume"].sum())

# save report
report_path = os.path.join(reportDirectory, "report.yml")
write_dict_to_yml(report_path, report)

# save quantification
Path_save_Quantification = os.path.join(reportDirectory, "Quantification.csv")
quantification.to_csv(Path_save_Quantification, index=False)
