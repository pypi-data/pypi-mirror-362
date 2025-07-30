import os
import time
from tkinter.filedialog import askdirectory

import altair as alt
import anndata
import numpy as np
import pandas as pd
import streamlit as st
from joblib import Parallel, delayed
from scipy.signal import find_peaks, savgol_filter
from tqdm import tqdm

st.set_page_config(layout="wide", page_title="All streamlit steps in 1 app")
tabHistOverview, tabFindPeaks, tabHistogramProperty, tabQuantify, tabAll = st.tabs(
    [
        "Histogram Overview",
        "Peak Finder",
        "Histograms + Properties",
        "Quantification",
        'All in One "experimental"',
    ]
)


############################### Load-Save Paths #################################
@st.cache_data
def directory():
    path = askdirectory(title="select folder with data")  ## folder 'data'
    return path


def fileName(path):  # select the type of histograms using a dropdown menu, must be h5ad
    filenames = [
        f for f in os.listdir(path) if f.endswith(".h5ad")
    ]  # get a list of h5ad files in the directory

    file = st.sidebar.selectbox(
        "Select a file",
        filenames,
        index=0,
        help="TIP: Bulk histograms should be used for a general assessmento of the parameters. Must click randomize button to refresh the histograms if changed",
    )  # it resets if new files are created in folder 'Data'
    return file


### histograms as h5ad
import sys

dataDirectory = sys.argv[1]
file = fileName(dataDirectory)
# load bulk histograms (= Inner + Outer)
Path_load_bulk_histogram = os.path.join(dataDirectory, file)
# load inner histograms (inside the particle without the eroded voxels)
Path_load_inner_histograms = os.path.join(dataDirectory, "Inner_histograms.h5ad")
# load outer (surface layers consisting of all voxels eroded) volume histograms
Path_load_outer_histograms = os.path.join(dataDirectory, "Outer_histograms.h5ad")
# load mesh histograms
Path_load_surface_mesh_histograms = os.path.join(
    dataDirectory, "Surface_histogram.h5ad"
)
# load gradient
Path_load_gradient = os.path.join(dataDirectory, "Gradient.csv")


############################### load data
@st.cache_data
def loadHistograms(Path_load_bulk_histogram):
    print("path histograms:", Path_load_bulk_histogram)
    try:
        adata = anndata.read_h5ad(Path_load_bulk_histogram, backed="r")
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
        initialBins = len(df.columns)
        return df, initialBins
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")


@st.cache_data
def loadProperties(path):
    pathAndName = os.path.join(
        path, "Properties.csv"
    )  ##works only for that file name of 'properties.csv'
    propertiesData = pd.read_csv(pathAndName, encoding="unicode_escape")
    return propertiesData


def loadPropertiesWPeaks(path):
    pathAndName = os.path.join(
        path, "PropertyAndPeaks.csv"
    )  ##works only for that file name of 'properties.csv'
    propertiesData = pd.read_csv(pathAndName, encoding="unicode_escape")
    return propertiesData


@st.cache_data
def loadInVolume(Path_load_inner_histograms):
    try:
        adata = anndata.read_h5ad(Path_load_inner_histograms, backed="r")
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
        print("h5ad Inner converted to DataFrame successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")
    return df


@st.cache_data
def loadOutVolume(Path_load_outer_histograms):
    try:
        adata = anndata.read_h5ad(Path_load_outer_histograms, backed="r")
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
        print("h5ad Outter converted to DataFrame successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")
    return df


@st.cache_data
def loadMesh(Path_load_surface_mesh_histograms):
    try:
        adata = anndata.read_h5ad(Path_load_surface_mesh_histograms, backed="r")
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
        print("h5ad Surface mesh converted to DataFrame successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")
    return df


@st.cache_data
def loadGradient(Path_load_gradient):
    Gradient = pd.read_csv(Path_load_gradient)
    Gradient.index = Gradient["label"]
    print("Gradient loaded")
    return Gradient


histogramsData, initialBins = loadHistograms(Path_load_bulk_histogram)
histogramsData = histogramsData.rename_axis("label")
histogramsData = histogramsData.astype("float64")
histogramsData = histogramsData.iloc[:, 1:]
propertiesData = loadProperties(dataDirectory)
propertiesData.index = propertiesData["label"]
numberregions = len(histogramsData)
st.sidebar.metric(
    label="Number of regions",
    value=numberregions,
    help="Total number of regions loaded in the histogram",
)
Inner_volume_histograms = loadInVolume(Path_load_inner_histograms)
Outer_volume_histograms = loadOutVolume(Path_load_outer_histograms)
Surface_mesh_histogram = loadMesh(Path_load_surface_mesh_histograms)
Gradient = loadGradient(Path_load_gradient)

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


@st.cache_data
def plotHistogramOverview(plotData):
    colorStd = alt.Color(
        "frequency:Q",
        scale=alt.Scale(scheme="viridis", domainMax=0.06),
        legend=alt.Legend(orient="bottom"),
        title="Frequency",
    )
    particleNumber = alt.X("X:N", title="Particle")
    greyBin = alt.Y("Y:O", title="Binned Greyscale").bin(maxbins=52)
    heatMapPartSelect = alt.selection_point(
        encodings=["x"], fields=["X"]
    )  # to select points on a trigger defined in "encodings", e.g. XY position
    opacitySelection = alt.condition(heatMapPartSelect, alt.value(1.0), alt.value(0.2))
    plotAllHistograms = (
        alt.Chart(plotData, width=1500, height=1000)
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
        alt.Chart(plotData, width=900, height=900)
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
def plotPeaks(plotData, PeaksDF):
    particleNumber = alt.X("X:N", title="Particle")
    plotAllHistograms = (
        alt.Chart(plotData, width=1000, height=500)
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
        alt.Chart(PeaksDF, width=1000, height=500)
        .mark_circle(color="#7fc97f", size=200, opacity=0.85)
        .encode(
            x=alt.X("Peak_1", title="Greyscale"),
            y=alt.Y("Peaks_Height_1", title="Frequency"),
        )
    )
    peak2Marks = (
        alt.Chart(PeaksDF, width=1000, height=500)
        .mark_circle(color="#beaed4", size=200, opacity=0.85)
        .encode(
            x=alt.X("Peak_2", title="Greyscale"),
            y=alt.Y("Peaks_Height_2", title="Frequency"),
        )
    )
    peak3Marks = (
        alt.Chart(PeaksDF, width=1000, height=500)
        .mark_circle(color="#fdc086", size=200, opacity=0.85)
        .encode(
            x=alt.X("Peak_3", title="Greyscale"),
            y=alt.Y("Peaks_Height_3", title="Frequency"),
        )
    )
    peak4Marks = (
        alt.Chart(PeaksDF, width=1000, height=500)
        .mark_circle(color="yellow", size=200, opacity=0.85)
        .encode(
            x=alt.X("Peak_4", title="Greyscale"),
            y=alt.Y("Peaks_Height_4", title="Frequency"),
        )
    )
    peak5Marks = (
        alt.Chart(PeaksDF, width=1000, height=500)
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


def plotMineralogy():
    # creates pie chart
    mineralMass = pd.DataFrame(
        {
            "mineral": ["A", "B", "C", "D", "E"],
            "value": [
                st.session_state["Phase A"],
                st.session_state["Phase B"],
                st.session_state["Phase C"],
                st.session_state["Phase D"],
                st.session_state["Phase E"],
            ],
        }
    )
    mineralSurface = pd.DataFrame(
        {
            "Surface": ["A", "B", "C", "D", "E"],
            "value": [
                st.session_state["SurfaceA"],
                st.session_state["SurfaceB"],
                st.session_state["SurfaceC"],
                st.session_state["SurfaceD"],
                st.session_state["SurfaceE"],
            ],
        }
    )
    colorStd2 = alt.Color(
        "mineral:N",
        scale=alt.Scale(scheme="accent"),
        legend=alt.Legend(title="Mass", orient="right"),
    )
    colorStd3 = alt.Color(
        "Surface:N",
        scale=alt.Scale(scheme="accent"),
        legend=alt.Legend(title="Surface", orient="right"),
    )
    mineralPlotM = (
        alt.Chart(mineralMass, title="Mass %")
        .mark_arc()
        .encode(theta="value", color=colorStd2)
    )
    mineralPlotS = (
        alt.Chart(mineralSurface, title="Surface %")
        .mark_arc()
        .encode(theta="value", color=colorStd3)
    )
    plot2 = mineralPlotM & mineralPlotS
    st.altair_chart(plot2, use_container_width=True)


def createSubdata1(n):
    labels_array = np.array(histogramsData.index)
    labels_array = labels_array[labels_array > 0]
    random_labels = np.random.choice(labels_array, n, replace=False)
    if (
        st.session_state["Particle_X"] > 0
    ):  # add a specific particle to the random dataset. Be sure the label exists
        random_labels = np.append(random_labels, st.session_state["Particle_X"])
    random_labels = np.sort(random_labels)
    random_labels = pd.DataFrame(random_labels, columns=["Label Index"])
    subData1 = histogramsData[histogramsData.index.isin(random_labels["Label Index"])]
    st.session_state["particleLabels"] = random_labels
    return subData1


def loadLabelList(dataDirectory):
    Path_labelList = os.path.join(dataDirectory, "labelList.csv")
    labelList = pd.read_csv(Path_labelList)
    subDataFromList = histogramsData[
        histogramsData.index.isin(labelList["Label Index"])
    ]
    st.session_state["list6regions"] = labelList["Label Index"]
    print(labelList)
    return subDataFromList


def saveLabelList(dataDirectory):
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
    PropWPeak_list = propertiesData.loc[labels_array]
    PropWPeak_list = PropWPeak_list.filter(
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
    PropWPeak_list["Label Index"] = labels_array
    Path_labelList = os.path.join(dataDirectory, "labelList.csv")
    PropWPeak_list.to_csv(Path_labelList, index=False)


def process_histogram_row(
    row, array, binning
):  # allows to input images with any binnig. This function is parallelized and used in the binning.
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


def binning(binInput, subData1, n_jobs=-1):
    array = np.array(subData1.columns).astype(int)
    binning = binInput
    # Parallel processing
    file1 = Parallel(n_jobs=n_jobs)(
        delayed(process_histogram_row)(row, array, binning)
        for _, row in tqdm(
            subData1.iterrows(), total=subData1.shape[0], desc="Processing Rows"
        )
    )
    # Convert lists to DataFrames
    rang = int(round(len(subData1.columns) / binning))
    x = np.linspace(0, len(subData1.columns) - 1, rang - 1).astype(int)
    file1 = np.array(file1).reshape(len(file1), -1)
    file1 = pd.DataFrame(file1, columns=x)
    file1.index = subData1.index
    file1[file1 < 0] = 0
    st.session_state["subData_binned"] = file1
    return file1


def normalizeVolume(unNormalized):
    unNormalized = pd.DataFrame(unNormalized)
    df_new = unNormalized.loc[:, :].div(unNormalized.sum(axis=1), axis=0)
    df_new = df_new.fillna(0)
    return df_new


def transformColumnsXY(subData_ready):
    row_append = []
    index_append = []
    Cols_append = []
    i = 0
    for i in range(len(subData_ready)):
        if i > -1:
            row = subData_ready.iloc[i]
            row_append.append([row])
            cols = (subData_ready.columns).astype(int)
            Index_array = np.zeros(len(row))
            Index_array[Index_array == 0] = row.name
            index_append.append([Index_array])
            Cols_append.append([cols])
        i = i + 1
    row_append = np.array(row_append)
    row_append = row_append.ravel()
    index_append = np.array(index_append)
    index_append = index_append.ravel()
    Cols_append = np.array(Cols_append)
    Cols_append = Cols_append.ravel()
    DataFrame1 = pd.DataFrame(index_append, columns=["X"])
    DataFrame2 = pd.DataFrame(Cols_append, columns=["Y"])
    DataFrame3 = pd.DataFrame(row_append, columns=["frequency"])
    Dataframe = pd.concat([DataFrame1, DataFrame2, DataFrame3], axis=1)
    return Dataframe


def smooth_histograms_Savgol(Binned_histograms, savgolInput, n_jobs=-1):
    smoothed_file1 = Parallel(n_jobs=n_jobs)(
        delayed(lambda row: savgol_filter(row, window_length=savgolInput, polyorder=3))(
            row
        )
        for _, row in tqdm(
            Binned_histograms.iterrows(),
            total=Binned_histograms.shape[0],
            desc="Smoothing Rows",
        )
    )
    file1 = pd.DataFrame(
        smoothed_file1, columns=Binned_histograms.columns, index=Binned_histograms.index
    )
    # Clip negative values to 0
    file1[file1 < 0] = 0
    # Ensure integer values if required
    file1 = file1.astype(int)
    return file1


def plotProperties():  # Plot in the histograms and properties tab
    colorStd2 = alt.Color(
        "X:N",
        scale=alt.Scale(scheme="accent"),
        legend=alt.Legend(title="Particle Number", orient="bottom"),
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
        .transform_filter(alt.FieldOneOfPredicate(field="label", oneOf=listOfregions))
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


def peaks(subDataFromList, labelList):
    PeaksDF = pd.DataFrame()
    with tabFindPeaks:
        with st.expander("Peak Properties"):
            for particle in labelList["Label Index"]:
                findParticleInSubdata = np.any(subDataFromList == particle, axis=1)
                regionsubdata = subDataFromList[findParticleInSubdata]
                frequency = regionsubdata["frequency"]
                peaksScipy = find_peaks(
                    frequency,
                    rel_height=0.5,
                    width=st.session_state["Peak_Width"],
                    height=st.session_state["Peak_Height"],
                    prominence=st.session_state["Peak_Prominence"],
                    threshold=st.session_state["Peak_Vertical_Distance"],
                    distance=st.session_state["Peak_Horizontal_Distance"],
                )
                st.write("Particle", particle, peaksScipy)
                xPeaks = np.array(peaksScipy[0])
                for p in xPeaks:
                    p = p * binInput
                    findPeakInParticle = regionsubdata[
                        np.any(regionsubdata == p, axis=1)
                    ]
                    PeaksDF = pd.concat([PeaksDF, findPeakInParticle], axis=0)
    return PeaksDF


def process_peaks(normalizedData, histogramsData, Properties, numberBins):
    normalizedData = pd.DataFrame(
        normalizedData
    )  # binned but maintaining the range, e.g.16bit to 8bit: 256 bins between 0-65535 (0, 256,512,768...)
    Peaks_Position = []
    Peaks_Height = []
    for index, row in tqdm(
        normalizedData.iterrows(),
        total=normalizedData.shape[0],
        desc="Processing Peaks",
    ):
        file_row_1 = np.array(row).ravel()
        file_row_1 = file_row_1.astype(float)
        file_row_1 = np.pad(file_row_1, (0, 1), constant_values=0)
        Grey_scale = np.array(histogramsData.columns, dtype=float)
        Grey_scale = np.pad(Grey_scale, (0, 1), constant_values=0)
        Grey_scale = Grey_scale.astype(int)
        file_row_1[np.isnan(file_row_1)] = 0
        file_row_1[file_row_1 < 0] = 0
        peaksScipy = find_peaks(
            file_row_1,
            rel_height=0.5,
            width=st.session_state["Peak_Width"],
            height=st.session_state["Peak_Height"],
            prominence=st.session_state["Peak_Prominence"],
            threshold=st.session_state["Peak_Vertical_Distance"],
            distance=st.session_state["Peak_Horizontal_Distance"],
        )

        height = peaksScipy[1]["peak_heights"]  # List of the heights of the peaks
        peak_pos = Grey_scale[peaksScipy[0]]
        peak_pos = peak_pos * binInput
        Peaks_Position.append([peak_pos])
        Peaks_Height.append([height])
    Peaks_Positions = pd.DataFrame(Peaks_Position)
    Peaks_Height = pd.DataFrame(Peaks_Height)
    # Flatten and rename columns
    Peaks_Positions = pd.concat([Peaks_Positions[0].str[i] for i in range(22)], axis=1)
    Peaks_Height = pd.concat([Peaks_Height[0].str[i] for i in range(22)], axis=1)
    Peaks_Positions.columns = [f"Peak_{i + 1}" for i in range(22)]
    Peaks_Height.columns = [f"Peaks_Height_{i + 1}" for i in range(22)]
    Peaks_Positions = Peaks_Positions.fillna(0)
    Peaks_Height = Peaks_Height.fillna(0)
    Peaks = pd.concat([Peaks_Positions, Peaks_Height], axis=1)
    Peaks.index = normalizedData.index
    Properties = Properties.loc[normalizedData.index]
    Peaks = pd.concat([Peaks, Properties], axis=1)
    Peaks["Binning"] = numberBins
    Peaks = Peaks.astype(float)
    Peaks.replace([np.inf, -np.inf], 0, inplace=True)
    Peaks.replace([np.inf, -np.inf], 0, inplace=True)
    Peaks.replace([np.nan], 0, inplace=True)
    return Peaks


def Arrange_peaks(
    Peaks1,
    Phase_1_threshold,
    Phase_2_threshold,
    Phase_3_threshold,
    Phase_4_threshold,
    Phase_5_threshold,
    Background_peak,
    Properties,
):
    # Define column names
    cols = [f"Peak_{i}" for i in range(1, 23)]
    peaks_height_cols = [f"Peaks_Height_{i}" for i in range(1, 23)]

    def process_phase(Peaks, phase_start, phase_end, phase_label):
        if Peaks.empty:
            return pd.DataFrame(
                0,
                index=Peaks.index,
                columns=[f"Peak_{phase_label}", f"Peaks_Height_{phase_label}"],
            )
        # Apply thresholds
        Peaks_filtered = Peaks.where(
            (Peaks >= phase_start) & (Peaks < phase_end), np.nan
        )
        Peaks_height = Peaks1[peaks_height_cols]
        Peaks_filtered = Peaks_filtered.loc[Peaks_filtered.any(axis=1), :].fillna(0)
        Peaks_filtered = Peaks_filtered.merge(
            Peaks_height, left_index=True, right_index=True
        )
        # Adjust peak positions and heights
        for i in range(1, 23):
            Peaks_filtered[f"Peak_{i}"] = Peaks_filtered[f"Peak_{i}"].clip(lower=0)
            Peaks_filtered[f"Peaks_Height_{i}"] = (
                Peaks_filtered[f"Peaks_Height_{i}"]
                .where(
                    (Peaks_filtered[f"Peak_{i}"] >= phase_start)
                    & (Peaks_filtered[f"Peak_{i}"] < phase_end),
                    0,
                )
                .where(Peaks_filtered[f"Peak_{i}"] >= Background_peak, 0)
            )
        # Check if there's valid data to process
        if Peaks_filtered[peaks_height_cols].notna().any().any():
            # Find the index of the maximum height
            max_peak_idx = Peaks_filtered[peaks_height_cols].idxmax(axis=1)
            # Initialize a new DataFrame with zeros
            peaks_data = pd.DataFrame(
                0,
                index=Peaks_filtered.index,
                columns=[f"Peak_{phase_label}", f"Peaks_Height_{phase_label}"],
            )
            for i, col_name in enumerate(peaks_height_cols):
                mask = max_peak_idx == col_name
                peaks_data[f"Peak_{phase_label}"] = np.where(
                    mask,
                    Peaks_filtered[f"Peak_{i + 1}"],
                    peaks_data[f"Peak_{phase_label}"],
                )
                peaks_data[f"Peaks_Height_{phase_label}"] = np.where(
                    mask,
                    Peaks_filtered[col_name],
                    peaks_data[f"Peaks_Height_{phase_label}"],
                )
        else:
            # Return an empty DataFrame if no valid peaks were found
            peaks_data = pd.DataFrame(
                0,
                index=Peaks.index,
                columns=[f"Peak_{phase_label}", f"Peaks_Height_{phase_label}"],
            )
        return peaks_data

    # Process each phase
    peaks_data_T1 = process_phase(Peaks1[cols], Background_peak, Phase_1_threshold, 1)
    peaks_data_T2 = process_phase(Peaks1[cols], Phase_1_threshold, Phase_2_threshold, 2)
    peaks_data_T3 = process_phase(Peaks1[cols], Phase_2_threshold, Phase_3_threshold, 3)
    peaks_data_T4 = process_phase(Peaks1[cols], Phase_3_threshold, Phase_4_threshold, 4)
    peaks_data_T5 = process_phase(Peaks1[cols], Phase_4_threshold, Phase_5_threshold, 5)
    peaks_data_T6 = process_phase(Peaks1[cols], Phase_5_threshold, np.inf, 6)
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
        Peaks = pd.concat(non_empty_peaks_data, axis=1, join="outer")
        Peaks = Peaks.loc[
            :, ~Peaks.columns.duplicated()
        ]  # Remove duplicated columns from concatenation
    else:
        Peaks = pd.DataFrame(
            index=Peaks1.index,
            columns=[f"Peak_{i}" for i in range(1, 7)]
            + [f"Peaks_Height_{i}" for i in range(1, 7)],
        )
        Peaks = Peaks.fillna(0)
    Peaks = Peaks.fillna(0)
    # Peaks = Peaks.astype(int)
    Peaks[["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5", "Peak_6"]] = Peaks[
        ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5", "Peak_6"]
    ].replace(0, Background_peak)
    Peaks["Max_peak"] = Peaks[
        ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5", "Peak_6"]
    ].max(axis=1)
    Peaks = Peaks.sort_values(by=["label"])
    # Combine with Properties_real
    propertiesAndPeaks = pd.concat([Peaks, Properties], axis=1)
    propertiesAndPeaks = propertiesAndPeaks.dropna()
    propertiesAndPeaks.replace([np.inf, -np.inf], 0, inplace=True)
    propertiesAndPeaks = propertiesAndPeaks.drop(
        propertiesAndPeaks[propertiesAndPeaks.Max_peak <= Background_peak].index
    )
    # propertiesAndPeaks = propertiesAndPeaks[["label","Volume",......to rearange the dataset]]
    # pathAndName=os.path.join(dataDirectory,'PropertyAndPeaks.csv')
    # propertiesAndPeaks.to_csv(pathAndName,index=False) ########################add save path input
    return propertiesAndPeaks


def plotPeaksBalls(propertiesAndPeaks):
    PaP = pd.DataFrame(propertiesAndPeaks)
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


def quntifyMineralogy(propertiesDataWPeaks, Background_peak):
    propertiesDataWPeaks = pd.DataFrame(propertiesDataWPeaks)
    partList = propertiesDataWPeaks.index.to_list()
    OutHistogram_Subdata = Outer_volume_histograms.loc[partList]
    SurfaceMesh_Subdata = Surface_mesh_histogram.loc[partList]
    InHistogram_Subdata = Inner_volume_histograms.loc[partList]
    Histograms_Subdata = histogramsData.loc[partList]
    Gradient_Subdata = Gradient.loc[partList]

    def update_peak_positions(
        properties, Background_peak, height_threshold, max_value=65535
    ):
        array = properties[["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]]
        # Fill NaN values with 0
        array = array.fillna(0)
        # Cap values at max_value
        array[array > max_value] = max_value
        for i in range(1, 5):  # Assuming there are 6 peaks (1 to 7)
            peak_position_col = f"Peak_{i}"
            peak_height_col = f"Peaks_Height_{i}"
            # Update peak positions based on the background peak position
            array[peak_position_col] = np.where(
                array[peak_position_col] < Background_peak,
                Background_peak,
                array[peak_position_col],
            )
            # Update peak positions based on the peak height
            array[peak_position_col] = np.where(
                properties[peak_height_col] < float(height_threshold),
                Background_peak,
                array[peak_position_col],
            )
        return array

    array = update_peak_positions(
        propertiesDataWPeaks, Background_peak, st.session_state["Peak_Height"]
    )

    # array is a subdataset from properties that contains only the peaks

    #### only liberated regions
    def quantifyLiberatedregions(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    ):
        Quantification_1_phases_append = []
        Index_1_phase = []
        Peaks_1_phase = []
        Quantification_Outer_phase_1_append = []
        Surface_quantification_append = []
        for i, (index, row) in enumerate(SurfaceMesh_Subdata.iterrows()):
            # Getting the peaks values
            Peaks = array.iloc[[i]].values
            # Condition that only 1 peak has value greater than background
            if np.count_nonzero(Peaks > Background_peak) == 1:
                Partical_peak = Peaks[Peaks > Background_peak].astype(int)[0]
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
                    0, 1, Partical_peak - Background_peak
                )
                No_of_voxels_towards_background_phase_1 = row.iloc[
                    Background_peak:Partical_peak
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
                Surface_quantification_liberated = SurfaceMesh_Subdata.iloc[
                    i, Background_peak:65535
                ].sum()
                Surface_quantification_append.append([Surface_quantification_liberated])
                st.session_state["regionsLiberated"] = (
                    st.session_state["regionsLiberated"] + 1
                )
                st.session_state["regionsAnalysed"] = (
                    st.session_state["regionsAnalysed"] + 1
                )
        # Outher referes to bins lower grey value than the peak (affected by partial volume)
        Quantification_Outer_phase_1 = pd.DataFrame(
            Quantification_Outer_phase_1_append,
            columns=["Quantification_Outer_phase_1"],
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
        Phase_0_threshold = Background_peak
        thresholds = [
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
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
            Quantification_1_phase_sorted[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_quantification["Surface_quantification"], 0)
        return Quantification_1_phase_sorted

    #### 2 Phases per particle
    def quantifyTwoPhasesParticle(
        SurfaceMesh_Subdata,
        array,
        Background_peak_pos,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        Gradient_threshold=0.75,
    ):
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
        for index, row in InHistogram_Subdata.iterrows():
            Peaks = array.iloc[[i]].values
            if (np.count_nonzero(Peaks > Background_peak_pos) == 2) and i > -1:
                Partical_peak = Peaks[Peaks > Background_peak_pos]
                Partical_peak_1 = int((Partical_peak).flat[0])
                Partical_peak_1 = int(float(Partical_peak_1))
                Gradient_ratio = Gradient_Subdata["Gradient_3"].iloc[i]
                if Gradient_ratio < Gradient_threshold:
                    Gradient_ratio = Gradient_threshold
                Sum_phase_1 = (
                    InHistogram_Subdata.iloc[i, Background_peak_pos:Partical_peak_1]
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
                No_of_voxels = InHistogram_Subdata.iloc[
                    i, Partical_peak_1:Partical_peak_2
                ]
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

                multiples_towards_Partical_peak_2 = multiples_towards_Partical_peak_1[
                    ::-1
                ]
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
                    0, 1, 1 / ((Partical_peak_1 - 1) - Background_peak_pos)
                )
                multiples_towards_background_phase_1 = np.array(
                    multiples_towards_background_phase_1
                )

                if len(
                    OutHistogram_Subdata.iloc[i, Background_peak_pos:Partical_peak_1]
                ) == len(multiples_towards_background_phase_1):
                    No_of_voxels_towards_background_phase_1 = OutHistogram_Subdata.iloc[
                        i, Background_peak_pos:Partical_peak_1
                    ]
                elif len(
                    OutHistogram_Subdata.iloc[i, Background_peak_pos:Partical_peak_1]
                ) > len(multiples_towards_background_phase_1):
                    No_of_voxels_towards_background_phase_1 = OutHistogram_Subdata.iloc[
                        i, Background_peak_pos : Partical_peak_1 - 1
                    ]
                else:
                    No_of_voxels_towards_background_phase_1 = OutHistogram_Subdata.iloc[
                        i, Background_peak_pos : Partical_peak_1 + 1
                    ]
                Quantification_Outer_phase_1_array = (
                    No_of_voxels_towards_background_phase_1
                    * multiples_towards_background_phase_1
                )
                multiples_towards_background_phase_2 = np.arange(
                    0, 1, 1 / ((Partical_peak_2 - 1) - Background_peak_pos)
                )
                multiples_towards_background_phase_2 = np.array(
                    multiples_towards_background_phase_2
                )

                if len(
                    OutHistogram_Subdata.iloc[i, Background_peak_pos:Partical_peak_2]
                ) == len(multiples_towards_background_phase_2):
                    No_of_voxels_towards_background_phase_2 = OutHistogram_Subdata.iloc[
                        i, Background_peak_pos:Partical_peak_2
                    ]
                elif len(
                    OutHistogram_Subdata.iloc[i, Background_peak_pos:Partical_peak_2]
                ) > len(multiples_towards_background_phase_2):
                    No_of_voxels_towards_background_phase_2 = OutHistogram_Subdata.iloc[
                        i, Background_peak_pos : Partical_peak_2 - 1
                    ]
                else:
                    No_of_voxels_towards_background_phase_2 = OutHistogram_Subdata.iloc[
                        i, Background_peak_pos : Partical_peak_2 + 1
                    ]
                Quantification_Outer_phase_2_array = (
                    No_of_voxels_towards_background_phase_2
                    * multiples_towards_background_phase_2
                )
                Vol_to_subtract_from_phase_1 = Quantification_Outer_phase_2_array[
                    Background_peak_pos:Partical_peak_1
                ]
                Vol_to_subtract_from_phase_1 = Vol_to_subtract_from_phase_1.sum()
                Quantification_Outer_phase_2_array = (
                    Quantification_Outer_phase_2_array.sum()
                    - Vol_to_subtract_from_phase_1
                )
                Quantification_Outer_phase_1_array = (
                    Quantification_Outer_phase_1_array.sum()
                )
                PVE_adjusted_volume = (
                    Outer_volume_full_phase_2
                    + Quantification_Outer_phase_1_array
                    + Quantification_Outer_phase_2_array
                )

                if Partical_peak_1 < Phase_1_threshold:
                    Phase_limit = Phase_1_threshold
                elif Phase_1_threshold <= Partical_peak_1 < Phase_2_threshold:
                    Phase_limit = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_1 < Phase_3_threshold:
                    Phase_limit = Phase_3_threshold
                elif Phase_3_threshold <= Partical_peak_1 < Phase_4_threshold:
                    Phase_limit = Phase_4_threshold

                Surface_ratio = (
                    SurfaceMesh_Subdata.iloc[
                        i, Background_peak_pos : int(Gradient_ratio * Phase_limit)
                    ].sum()
                ) / (SurfaceMesh_Subdata.iloc[i, Background_peak_pos:].sum())
                Phase_1_surface_volume = (
                    SurfaceMesh_Subdata.iloc[i, Background_peak_pos:65535].sum()
                    * Surface_ratio
                )
                Phase_2_surface_volume = (
                    SurfaceMesh_Subdata.iloc[i, Background_peak_pos:65535].sum()
                    - Phase_1_surface_volume
                )
                Surface_volume_phase_1_append.append([Phase_1_surface_volume])
                Surface_volume_phase_2_append.append([Phase_2_surface_volume])
                Quantification_Outer_phase_1_volume = (
                    Surface_ratio * PVE_adjusted_volume
                )
                Quantification_Outer_phase_2_volume = (
                    PVE_adjusted_volume - Quantification_Outer_phase_1_volume
                )
                Quantification_Outer_phase_1.append(
                    [Quantification_Outer_phase_1_volume]
                )
                Quantification_Outer_phase_2.append(
                    [Quantification_Outer_phase_2_volume]
                )
                Index_2_phase.append([index])
                st.session_state["regions2Phases"] = (
                    st.session_state["regions2Phases"] + 1
                )
                st.session_state["regionsAnalysed"] = (
                    st.session_state["regionsAnalysed"] + 1
                )
                st.session_state["VolumeAnalysed"] = (
                    st.session_state["VolumeAnalysed"]
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
        Quantification_2_phases[
            "Phase_1_surface_quantification"
        ] = Surface_volume_phase_1["Surface_volume_phase_1"]
        Quantification_2_phases[
            "Phase_2_surface_quantification"
        ] = Surface_volume_phase_2["Surface_volume_phase_2"]

        Phase_0_threshold = Background_peak
        cols = ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
        Phase_5_threshold = 100000
        thresholds = [
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
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
            Quantification_2_phase_sorted[
                f"Phase_{i}_surface_quantification"
            ] = np.where(
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
            Quantification_2_phase_sorted_1[
                f"Phase_{i}_surface_quantification"
            ] = np.where(
                mask, Quantification_2_phases["Phase_2_surface_quantification"], 0
            )

        Quantification_2_phase_sorted = Quantification_2_phase_sorted.mask(
            Quantification_2_phase_sorted == 0, Quantification_2_phase_sorted_1
        )
        Quantification_2_phase_sorted.index = Quantification_2_phases.index

        return Quantification_2_phase_sorted

    #### 3 Phases per particle
    def quantify3Phases_particle(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    ):
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
        for index, row in SurfaceMesh_Subdata.iterrows():
            Peaks = array.iloc[[i]].values
            if (np.count_nonzero(Peaks > Background_peak) == 3) and i > -1:
                Partical_peak = Peaks[Peaks > Background_peak]
                Partical_peak_1 = Partical_peak.flat[0]
                Partical_peak_1 = int(float(Partical_peak_1))
                Partical_peak_2 = Partical_peak.flat[1]
                Partical_peak_2 = int(float(Partical_peak_2))
                Partical_peak_3 = Partical_peak.flat[2]
                Partical_peak_3 = int(float(Partical_peak_3))
                # Taking the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
                Sum_phase_1 = Histograms_Subdata.iloc[
                    i, Background_peak : int((Partical_peak_1 + Partical_peak_2) / 2)
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

                if Partical_peak_1 < Phase_1_threshold:
                    Phase_limit_1 = Phase_1_threshold
                elif Phase_1_threshold <= Partical_peak_1 < Phase_2_threshold:
                    Phase_limit_1 = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_1 < Phase_3_threshold:
                    Phase_limit_1 = Phase_3_threshold
                else:
                    Phase_limit_1 = Phase_4_threshold

                if Phase_1_threshold <= Partical_peak_2 < Phase_2_threshold:
                    Phase_limit_2 = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_2 < Phase_3_threshold:
                    Phase_limit_2 = Phase_3_threshold
                else:
                    Phase_limit_2 = Phase_4_threshold
                Phase_1_surface_volume = SurfaceMesh_Subdata.iloc[
                    i, Background_peak : int(Phase_limit_1 * Gradient_ratio)
                ].sum()
                Phase_2_surface_volume = SurfaceMesh_Subdata.iloc[
                    i,
                    int(Phase_limit_1 * Gradient_ratio) : int(
                        Phase_limit_2 * Gradient_ratio
                    ),
                ].sum()
                Phase_3_surface_volume = SurfaceMesh_Subdata.iloc[
                    i, int(Phase_limit_2 * Gradient_ratio) :
                ].sum()
                Surface_volume_phase_1_append.append([Phase_1_surface_volume])
                Surface_volume_phase_2_append.append([Phase_2_surface_volume])
                Surface_volume_phase_3_append.append([Phase_3_surface_volume])
                st.session_state["regions3Phases"] = (
                    st.session_state["regions3Phases"] + 1
                )
                st.session_state["regionsAnalysed"] = (
                    st.session_state["regionsAnalysed"] + 1
                )
                st.session_state["VolumeAnalysed"] = (
                    st.session_state["VolumeAnalysed"]
                    + Sum_phase_1
                    + Sum_phase_2
                    + Sum_phase_3
                )
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
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
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
            Quantification_3_phase_sorted[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_1["Surface_volume_phase_1"], 0)
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
            Quantification_3_phase_sorted_1[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_2["Surface_volume_phase_2"], 0)
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
            Quantification_3_phase_sorted_2[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_3["Surface_volume_phase_3"], 0)
        Quantification_3_phase_sorted = Quantification_3_phase_sorted.mask(
            Quantification_3_phase_sorted == 0, Quantification_3_phase_sorted_1
        )
        Quantification_3_phase_sorted = Quantification_3_phase_sorted.mask(
            Quantification_3_phase_sorted == 0, Quantification_3_phase_sorted_2
        )
        Quantification_3_phase_sorted.index = Quantification_3_phases["Label"]

        return Quantification_3_phase_sorted

    #### 4 Phases per particle
    def Quaternary_regions(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    ):
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
        for index, row in SurfaceMesh_Subdata.iterrows():
            Peaks = array.iloc[[i]].values
            if (np.count_nonzero(Peaks > Background_peak) == 4) and i > -1:
                Partical_peak = Peaks[Peaks > Background_peak]
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
                    i, Background_peak : int((Partical_peak_1 + Partical_peak_2) / 2)
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
                if Partical_peak_1 < Phase_1_threshold:
                    Phase_limit_1 = Phase_1_threshold
                elif Phase_1_threshold <= Partical_peak_1 < Phase_2_threshold:
                    Phase_limit_1 = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_1 < Phase_3_threshold:
                    Phase_limit_1 = Phase_3_threshold
                else:
                    Phase_limit_1 = Phase_4_threshold

                if Phase_1_threshold <= Partical_peak_2 < Phase_2_threshold:
                    Phase_limit_2 = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_2 < Phase_3_threshold:
                    Phase_limit_2 = Phase_3_threshold
                else:
                    Phase_limit_2 = Phase_4_threshold

                if Phase_2_threshold <= Partical_peak_3 < Phase_3_threshold:
                    Phase_limit_3 = Phase_3_threshold
                else:
                    Phase_limit_3 = Phase_4_threshold

                Phase_1_surface_volume = SurfaceMesh_Subdata.iloc[
                    i, Background_peak : int(Phase_limit_1 * Gradient_ratio)
                ].sum()
                Phase_2_surface_volume = SurfaceMesh_Subdata.iloc[
                    i,
                    int(Phase_limit_1 * Gradient_ratio) : int(
                        Phase_limit_2 * Gradient_ratio
                    ),
                ].sum()
                Phase_3_surface_volume = SurfaceMesh_Subdata.iloc[
                    i,
                    int(Phase_limit_2 * Gradient_ratio) : int(
                        Phase_limit_3 * Gradient_ratio
                    ),
                ].sum()
                Phase_4_surface_volume = SurfaceMesh_Subdata.iloc[
                    i, int(Phase_limit_3 * Gradient_ratio) :
                ].sum()
                Surface_volume_phase_1_append.append([Phase_1_surface_volume])
                Surface_volume_phase_2_append.append([Phase_2_surface_volume])
                Surface_volume_phase_3_append.append([Phase_3_surface_volume])
                Surface_volume_phase_4_append.append([Phase_4_surface_volume])
                st.session_state["regions3Phases"] = (
                    st.session_state["regions3Phases"] + 1
                )
                st.session_state["regionsAnalysed"] = (
                    st.session_state["regionsAnalysed"] + 1
                )
                st.session_state["VolumeAnalysed"] = (
                    st.session_state["VolumeAnalysed"]
                    + Sum_phase_1
                    + Sum_phase_2
                    + Sum_phase_3
                    + Sum_phase_4
                )
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
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
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
            Quantification_4_phase_sorted[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_1["Surface_volume_phase_1"], 0)
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
            Quantification_4_phase_sorted_1[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_2["Surface_volume_phase_2"], 0)
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
            Quantification_4_phase_sorted_2[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_3["Surface_volume_phase_3"], 0)
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
            Quantification_4_phase_sorted_3[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_4["Surface_volume_phase_4"], 0)
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

        return Quantification_4_phase_sorted

    #### 5 Phases per particle
    def Quinary_regions(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    ):
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
        for index, row in SurfaceMesh_Subdata.iterrows():
            Peaks = array.iloc[[i]].values
            if (np.count_nonzero(Peaks > Background_peak) == 5) and i > -1:
                Partical_peak = Peaks[Peaks > Background_peak]
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
                    i, Background_peak : int((Partical_peak_1 + Partical_peak_2) / 2)
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
                Phase_limit_1 = Phase_1_threshold
                Phase_limit_2 = Phase_2_threshold
                Phase_limit_3 = Phase_3_threshold
                Phase_limit_4 = Phase_4_threshold
                Phase_1_surface_volume = SurfaceMesh_Subdata.iloc[
                    i, Background_peak : int(Phase_limit_1 * Gradient_ratio)
                ].sum()
                Phase_2_surface_volume = SurfaceMesh_Subdata.iloc[
                    i,
                    int(Phase_limit_1 * Gradient_ratio) : int(
                        Phase_limit_2 * Gradient_ratio
                    ),
                ].sum()
                Phase_3_surface_volume = SurfaceMesh_Subdata.iloc[
                    i,
                    int(Phase_limit_2 * Gradient_ratio) : int(
                        Phase_limit_3 * Gradient_ratio
                    ),
                ].sum()
                Phase_4_surface_volume = SurfaceMesh_Subdata.iloc[
                    i,
                    int(Phase_limit_3 * Gradient_ratio) : int(
                        Phase_limit_4 * Gradient_ratio
                    ),
                ].sum()
                Phase_5_surface_volume = SurfaceMesh_Subdata.iloc[
                    i, int(Phase_limit_4 * Gradient_ratio) :
                ].sum()
                Surface_volume_phase_1_append.append([Phase_1_surface_volume])
                Surface_volume_phase_2_append.append([Phase_2_surface_volume])
                Surface_volume_phase_3_append.append([Phase_3_surface_volume])
                Surface_volume_phase_4_append.append([Phase_4_surface_volume])
                Surface_volume_phase_5_append.append([Phase_5_surface_volume])
                st.session_state["regions3Phases"] = (
                    st.session_state["regions3Phases"] + 1
                )
                st.session_state["regionsAnalysed"] = (
                    st.session_state["regionsAnalysed"] + 1
                )
                st.session_state["VolumeAnalysed"] = (
                    st.session_state["VolumeAnalysed"]
                    + Sum_phase_1
                    + Sum_phase_2
                    + Sum_phase_3
                    + Sum_phase_4
                    + Sum_phase_5
                )
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
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
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
            Quantification_5_phase_sorted[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_1["Surface_volume_phase_1"], 0)
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
            Quantification_5_phase_sorted_1[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_2["Surface_volume_phase_2"], 0)
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
            Quantification_5_phase_sorted_2[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_3["Surface_volume_phase_3"], 0)
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
            Quantification_5_phase_sorted_3[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_4["Surface_volume_phase_4"], 0)
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
            Quantification_5_phase_sorted_4[
                f"Phase_{i}_surface_quantification"
            ] = np.where(mask, Surface_volume_phase_5["Surface_volume_phase_5"], 0)
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
        return Quantification_5_phase_sorted

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

    st.session_state["regions2Phases"] = 0
    st.session_state["regions3Phases"] = 0
    st.session_state["regionsAnalysed"] = 0
    st.session_state["VolumeAnalysed2"] = 0
    st.session_state["regionsLiberated"] = 0
    st.session_state["VolumeAnalysed"] = 0
    st.session_state["SurfaceAnalysed"] = 0
    st.session_state["SurfaceA"] = 0
    st.session_state["SurfaceB"] = 0
    st.session_state["SurfaceC"] = 0
    st.session_state["SurfaceD"] = 0
    st.session_state["SurfaceE"] = 0
    st.session_state["Phase A"] = 0
    st.session_state["Phase B"] = 0
    st.session_state["Phase C"] = 0
    st.session_state["Phase D"] = 0
    st.session_state["Phase E"] = 0
    st.session_state["PhaseA_mass"] = 0
    st.session_state["PhaseB_mass"] = 0
    st.session_state["PhaseC_mass"] = 0
    st.session_state["PhaseD_mass"] = 0
    st.session_state["PhaseE_mass"] = 0
    Liberated_quantification = quantifyLiberatedregions(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    )
    Binary_quantification = quantifyTwoPhasesParticle(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    )
    Ternary_quantification = quantify3Phases_particle(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    )
    Quaternary_quantification = Quaternary_regions(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
    )
    Quinary_quantification = Quinary_regions(
        SurfaceMesh_Subdata,
        array,
        Background_peak,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
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
    st.session_state["SurfaceA"] = Quantification[
        "Phase_1_surface_quantification"
    ].sum()
    st.session_state["SurfaceB"] = Quantification[
        "Phase_2_surface_quantification"
    ].sum()
    st.session_state["SurfaceC"] = Quantification[
        "Phase_3_surface_quantification"
    ].sum()
    st.session_state["SurfaceD"] = Quantification[
        "Phase_4_surface_quantification"
    ].sum()
    st.session_state["SurfaceE"] = Quantification[
        "Phase_5_surface_quantification"
    ].sum()

    st.session_state["PhaseA_mass"] = (
        Quantification["Phase_1_quantification"].sum() * inputDensityA
    )
    st.session_state["PhaseB_mass"] = (
        Quantification["Phase_2_quantification"].sum() * inputDensityB
    )
    st.session_state["PhaseC_mass"] = (
        Quantification["Phase_3_quantification"].sum() * inputDensityC
    )
    st.session_state["PhaseD_mass"] = (
        Quantification["Phase_4_quantification"].sum() * inputDensityD
    )
    st.session_state["PhaseE_mass"] = (
        Quantification["Phase_5_quantification"].sum() * inputDensityE
    )

    st.session_state["VolumeAnalysed2"] = (
        Quantification["Phase_1_quantification"].sum()
        + Quantification["Phase_2_quantification"].sum()
        + Quantification["Phase_3_quantification"].sum()
        + Quantification["Phase_4_quantification"].sum()
        + Quantification["Phase_5_quantification"].sum()
    )
    st.session_state["SurfaceAnalysed"] = (
        st.session_state["SurfaceA"]
        + st.session_state["SurfaceB"]
        + st.session_state["SurfaceC"]
        + st.session_state["SurfaceD"]
        + st.session_state["SurfaceE"]
    )

    totalMass = (
        st.session_state["PhaseA_mass"]
        + st.session_state["PhaseB_mass"]
        + st.session_state["PhaseC_mass"]
        + st.session_state["PhaseD_mass"]
        + st.session_state["PhaseE_mass"]
    )
    if totalMass > 0:
        st.session_state["Phase A"] = round(
            st.session_state["PhaseA_mass"] * 100 / totalMass, 1
        )
        st.session_state["Phase B"] = round(
            st.session_state["PhaseB_mass"] * 100 / totalMass, 1
        )
        st.session_state["Phase C"] = round(
            st.session_state["PhaseC_mass"] * 100 / totalMass, 1
        )
        st.session_state["Phase D"] = round(
            st.session_state["PhaseD_mass"] * 100 / totalMass, 1
        )
        st.session_state["Phase E"] = round(
            st.session_state["PhaseE_mass"] * 100 / totalMass, 1
        )
        st.session_state["SurfaceA"] = round(
            st.session_state["SurfaceA"] * 100 / st.session_state["SurfaceAnalysed"], 1
        )
        st.session_state["SurfaceB"] = round(
            st.session_state["SurfaceB"] * 100 / st.session_state["SurfaceAnalysed"], 1
        )
        st.session_state["SurfaceC"] = round(
            st.session_state["SurfaceC"] * 100 / st.session_state["SurfaceAnalysed"], 1
        )
        st.session_state["SurfaceD"] = round(
            st.session_state["SurfaceD"] * 100 / st.session_state["SurfaceAnalysed"], 1
        )
        st.session_state["SurfaceE"] = round(
            st.session_state["SurfaceE"] * 100 / st.session_state["SurfaceAnalysed"], 1
        )

    propertiesDataWPeaks.index = propertiesDataWPeaks["label"]
    columns_to_keep = [
        col
        for col in propertiesDataWPeaks.columns
        if col not in Quantification.columns or col == "Label"
    ]
    propertiesDataWPeaks = propertiesDataWPeaks[columns_to_keep]
    Quantification = pd.merge(
        Quantification, propertiesDataWPeaks, left_index=True, right_index=True
    )
    Path_save_Quantification = os.path.join(dataDirectory, "Quantification.csv")
    Quantification.to_csv(Path_save_Quantification, index=False)


binInput = st.sidebar.number_input(
    "bins",
    value=256,
    max_value=initialBins,
    step=16,
    help="number to be divided by the initial number of bins. The higher the input the less number of bins plotted",
)
numberBins = int(initialBins / binInput)
savgolInput = st.sidebar.slider(
    "Savgol plot smothening input",
    min_value=3,
    value=4,
    max_value=26,
    help="This slider is not interactive! The new input is only visible in the plot after pressing randomize",
)
numbPartSubData = st.sidebar.number_input(
    "number regions in subset", value=3, min_value=3, max_value=numberregions, step=2
)
buttRandomize = st.sidebar.button("Randomize")
sliderWidth = st.sidebar.slider(
    label="Grey-value width",
    max_value=int(numberBins / 5),
    min_value=0,
    step=1,
    help="Unclear definition, possibly the distance between the two valeys on either side of a peak",
)
sliderHeight = st.sidebar.slider(
    label="Min. Frequency",
    max_value=0.20,
    min_value=0.001,
    step=0.001,
    help="Minimum height of peaks from bottom",
)
Prominence = st.sidebar.slider(
    label="Frequency prominence",
    max_value=0.050,
    min_value=0.000,
    step=0.002,
    help="Minimum height of climb from a valey left or right from the peak",
)
horizDistance = st.sidebar.slider(
    label="Grey-value variation",
    max_value=int(numberBins - (numberBins * 0.15)),
    min_value=1,
    step=1,
    help="Minimum horizontal distance between neighbour peaks",
)
vertDistance = st.sidebar.slider(
    label="Frequency variation",
    max_value=0.100,
    min_value=0.000,
    step=0.001,
    help="Minimum vertical distance between neighbour peaks",
)
buttRunAll = st.sidebar.button(
    label="Quantify all",
    help="Applies the peak parameters to all regions and apends the grey-values of the peaks to the properties file. Must be pressed for the new thresholds to take effect",
)
plotDataButton = st.sidebar.radio(
    "How many regions",
    ["All regions", "Random regions", "regions of interest"],
    index=2,
)
st.session_state["Peak_Width"] = sliderWidth
st.session_state["Peak_Height"] = sliderHeight
st.session_state["Peak_Prominence"] = Prominence
st.session_state["Peak_Horizontal_Distance"] = horizDistance
st.session_state["Peak_Vertical_Distance"] = vertDistance
inclusionsBox = st.sidebar.checkbox("inclusions")

with tabHistOverview:
    colLoad, colSave, colSavgol, colA, colB, colC, colD, colE, colF, colX = st.columns(
        10
    )
    with colSavgol:
        savgolBox = st.checkbox("Activate Savgol Smoothening")
    with colLoad:
        buttLoadListLabels = st.button(
            "Load regions",
            help="Loads a list of labels as csv created from Napari image viewer",
        )
    with colSave:
        buttSaveListLabels = st.button(
            "Save regions",
            help="Saves a list of particle label as csv that can be visualized in Napari",
        )
# initiation condition creates 3 random regions
if "particleLabels" not in st.session_state or "plotSubData1" not in st.session_state:
    histogramsSubData = createSubdata1(3)
    startTime = time.time()
    histograms_binned = binning(binInput, histogramsSubData, n_jobs=-1)
    if savgolBox:
        savgolSmooth = smooth_histograms_Savgol(
            histograms_binned, savgolInput, n_jobs=-1
        )  ############# Savgol filter applied if the slider input is >1
        normalizedHistograms = normalizeVolume(savgolSmooth)
    else:
        normalizedHistograms = normalizeVolume(histograms_binned)
    st.session_state["plotSubData1"] = transformColumnsXY(normalizedHistograms)
    st.session_state["NormalizedSubData"] = normalizedHistograms
    finishTime = time.time()
    print("plotSubData1:", finishTime - startTime)
with tabFindPeaks:  # table with threshold inputs
    col1, col2 = st.columns(spec=[0.8, 0.2])
    with col2:
        loadInputFiles = st.file_uploader(
            label="Load input densities and thresholds",
            help="Thresholds and densities can be loaded from a csv pre-saved from the table. IMPORTANT: if file is loaded changes on the table will not make effect. Delete file to interactively see changes in the plot",
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
            Background_peak = int(inputsLoaded.iloc[0]["BackgroundT"])
            Phase_1_threshold = int(inputsLoaded.iloc[0]["Max greyvalue A"])
            Phase_2_threshold = int(inputsLoaded.iloc[0]["Max greyvalue B"])
            Phase_3_threshold = int(inputsLoaded.iloc[0]["Max greyvalue C"])
            Phase_4_threshold = int(inputsLoaded.iloc[0]["Max greyvalue D"])
            Phase_5_threshold = int(inputsLoaded.iloc[0]["Max greyvalue E"])
            print("greyC", int(inputsLoaded.iloc[0]["Max greyvalue C"]))
            print("threshold3", Phase_3_threshold)
        else:
            input4Quantification = {
                "BackgroundT": [600],
                "DensityA": [1],
                "Max greyvalue A": [6000],
                "DensityB": [1],
                "Max greyvalue B": [11111],
                "DensityC": [1],
                "Max greyvalue C": [22222],
                "DensityD": [1],
                "Max greyvalue D": [25555],
                "DensityE": [0],
                "Max greyvalue E": [65555],
            }
            input4Quantification = pd.DataFrame(input4Quantification)
            inputs = st.data_editor(input4Quantification)
            inputDensityA = int(inputs.iloc[0]["DensityA"])
            inputDensityB = int(inputs.iloc[0]["DensityB"])
            inputDensityC = int(inputs.iloc[0]["DensityC"])
            inputDensityD = int(inputs.iloc[0]["DensityD"])
            inputDensityE = int(inputs.iloc[0]["DensityE"])
            Background_peak = int(inputs.iloc[0]["BackgroundT"])
            Phase_1_threshold = int(inputs.iloc[0]["Max greyvalue A"])
            Phase_2_threshold = int(inputs.iloc[0]["Max greyvalue B"])
            Phase_3_threshold = int(inputs.iloc[0]["Max greyvalue C"])
            Phase_4_threshold = int(inputs.iloc[0]["Max greyvalue D"])
            Phase_5_threshold = int(inputs.iloc[0]["Max greyvalue E"])

        Phase_0_threshold = Background_peak

if "plotAllData" not in st.session_state:
    startTime = time.time()
    histograms_binned = binning(binInput, histogramsData, n_jobs=-1)
    if savgolBox:
        savgolSmooth = smooth_histograms_Savgol(
            histograms_binned, savgolInput, n_jobs=-1
        )  ############# Savgol filter applied if the slider input is >1
        st.session_state["NormalizedData"] = normalizeVolume(savgolSmooth)
    else:
        st.session_state["NormalizedData"] = normalizeVolume(histograms_binned)
    st.session_state["plotAllData"] = transformColumnsXY(
        st.session_state["NormalizedData"]
    )
    PeaksSubData = process_peaks(
        st.session_state["NormalizedData"], histogramsData, propertiesData, numberBins
    )
    st.session_state["propAndPeaksAll"] = Arrange_peaks(
        PeaksSubData,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        Phase_5_threshold,
        Phase_0_threshold,
        propertiesData,
    )
    finishTime = time.time()
    print("plotAllData:", finishTime - startTime)

propertiesAndPeaks = st.session_state["propAndPeaksAll"]
if buttRandomize:  # creates a random list of regions st.['particleLabels']
    histogramsSubData = createSubdata1(numbPartSubData)
    startTime = time.time()
    histograms_binned = binning(binInput, histogramsSubData, n_jobs=-1)
    if savgolBox:
        savgolSmooth = smooth_histograms_Savgol(
            histograms_binned, savgolInput, n_jobs=-1
        )  ############# Savgol filter applied if the slider input is >1
        st.session_state["NormalizedSubData"] = normalizeVolume(savgolSmooth)
    else:
        st.session_state["NormalizedSubData"] = normalizeVolume(histograms_binned)
    st.session_state["plotSubData1"] = transformColumnsXY(
        st.session_state["NormalizedSubData"]
    )
    finishTime = time.time()
    print("plotSubData1:", finishTime - startTime)

if (
    buttLoadListLabels
):  # Loads list of particle labelsfrom CSV, regions A to F created either from 'Histograms Overview' tab or from Napari
    subDataFromList = loadLabelList(dataDirectory)  # updates st.list6regions
    startTime = time.time()
    histograms_binned = binning(binInput, subDataFromList, n_jobs=-1)
    if savgolBox:
        savgolSmooth = smooth_histograms_Savgol(
            histograms_binned, savgolInput, n_jobs=-1
        )  ############# Savgol filter applied if the slider input is >1
        st.session_state["Normalized6regions"] = normalizeVolume(savgolSmooth)
    else:
        st.session_state["Normalized6regions"] = normalizeVolume(histograms_binned)
    st.session_state["plotDataFromList"] = transformColumnsXY(
        st.session_state["Normalized6regions"]
    )
    finishTime = time.time()
    print("plotDataFromList:", finishTime - startTime)
    st.session_state["particleLabels"] = st.session_state["list6regions"]

with tabHistOverview:
    lenghtOfList = len(st.session_state["particleLabels"])
    with colX:
        particleNumberBox = st.number_input(
            "Label particle X",
            step=1,
            help="specific particle. Does not need to be in the random dataset, but the label must exist in the full dataset",
        )
        st.session_state["Particle_X"] = particleNumberBox
    with colA:
        dropdown1 = st.selectbox(
            label="Label Particle A",
            options=st.session_state["particleLabels"],
            index=0,
        )
        st.session_state["Particle_A"] = dropdown1
    with colB:
        dropdown2 = st.selectbox(
            label="Label Particle B",
            options=st.session_state["particleLabels"],
            index=1,
        )
        st.session_state["Particle_B"] = dropdown2
    with colC:
        dropdown3 = st.selectbox(
            label="Label Particle C",
            options=st.session_state["particleLabels"],
            index=2,
        )
        st.session_state["Particle_C"] = dropdown3
    with colD:
        if lenghtOfList > 3:
            dropdown4 = st.selectbox(
                label="Label Particle D",
                options=st.session_state["particleLabels"],
                index=3,
            )
        else:
            dropdown4 = st.selectbox(
                label="Label Particle D",
                options=st.session_state["particleLabels"],
                index=0,
            )
        st.session_state["Particle_D"] = dropdown4
    with colE:
        if lenghtOfList > 4:
            dropdown5 = st.selectbox(
                label="Label Particle E",
                options=st.session_state["particleLabels"],
                index=4,
            )
        else:
            dropdown5 = st.selectbox(
                label="Label Particle E",
                options=st.session_state["particleLabels"],
                index=0,
            )
        st.session_state["Particle_E"] = dropdown5
    with colF:
        if lenghtOfList > 5:
            dropdown6 = st.selectbox(
                label="Label Particle F",
                options=st.session_state["particleLabels"],
                index=5,
            )
        else:
            dropdown6 = st.selectbox(
                label="Label Particle F",
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
        plotDataButton == "regions of interest"
        or "plotDataFromList" not in st.session_state
    ):
        startTime = time.time()
        histograms_binned = binning(binInput, histograms6regions, n_jobs=-1)
        if savgolBox:
            savgolSmooth = smooth_histograms_Savgol(
                histograms_binned, savgolInput, n_jobs=-1
            )  ############# Savgol filter applied if the slider input is >1
            normalizedHistograms = normalizeVolume(savgolSmooth)
        else:
            normalizedHistograms = normalizeVolume(histograms_binned)
        st.session_state["plotDataFromList"] = transformColumnsXY(normalizedHistograms)
        st.session_state["Normalized6regions"] = normalizedHistograms
        finishTime = time.time()
        print("plotDataFromList:", finishTime - startTime)
        plotHistogramOverview(st.session_state["plotDataFromList"])
        with st.expander("Histograms regions of interest"):
            st.dataframe(st.session_state["Normalized6regions"], hide_index=True)
    if plotDataButton == "Random regions":
        plotHistogramOverview(st.session_state["plotSubData1"])
        with st.expander("Histograms of random regions"):
            st.dataframe(st.session_state["NormalizedSubData"], hide_index=True)
    if plotDataButton == "All regions":
        plotHistogramOverview(st.session_state["plotAllData"])
        with st.expander("Histograms all regions"):
            st.dataframe(st.session_state["NormalizedData"], hide_index=True)
if buttSaveListLabels:
    saveLabelList(dataDirectory)

with tabFindPeaks:  # table with threshold inputs
    with col1:
        if plotDataButton == "regions of interest":
            PeaksSubData = process_peaks(
                st.session_state["Normalized6regions"],
                histogramsData,
                propertiesData,
                numberBins,
            )
            st.session_state["propAndPeaksROI"] = Arrange_peaks(
                PeaksSubData,
                Phase_1_threshold,
                Phase_2_threshold,
                Phase_3_threshold,
                Phase_4_threshold,
                Phase_5_threshold,
                Phase_0_threshold,
                propertiesData,
            )
            plotPeaks(
                st.session_state["plotDataFromList"],
                st.session_state["propAndPeaksROI"],
            )
        if plotDataButton == "Random regions":
            PeaksSubData = process_peaks(
                st.session_state["NormalizedSubData"],
                histogramsData,
                propertiesData,
                numberBins,
            )
            st.session_state["propAndPeaksRandom"] = Arrange_peaks(
                PeaksSubData,
                Phase_1_threshold,
                Phase_2_threshold,
                Phase_3_threshold,
                Phase_4_threshold,
                Phase_5_threshold,
                Phase_0_threshold,
                propertiesData,
            )
            plotPeaks(
                st.session_state["plotSubData1"], st.session_state["propAndPeaksRandom"]
            )
        if plotDataButton == "All regions":
            PeaksSubData = process_peaks(
                st.session_state["NormalizedData"],
                histogramsData,
                propertiesData,
                numberBins,
            )
            st.session_state["propAndPeaksAll"] = Arrange_peaks(
                PeaksSubData,
                Phase_1_threshold,
                Phase_2_threshold,
                Phase_3_threshold,
                Phase_4_threshold,
                Phase_5_threshold,
                Phase_0_threshold,
                propertiesData,
            )
            plotPeaks(
                st.session_state["plotAllData"], st.session_state["propAndPeaksAll"]
            )
    with col2:
        if plotDataButton == "Random regions":
            with st.expander("List of Peaks"):
                st.dataframe(st.session_state["propAndPeaksRandom"])
        if plotDataButton == "All regions":
            with st.expander("List of Peaks"):
                st.dataframe(st.session_state["propAndPeaksAll"])
        if plotDataButton == "regions of interest":
            with st.expander("List of Peaks"):
                st.dataframe(st.session_state["propAndPeaksROI"])
if buttRunAll:
    with tabFindPeaks:
        with col1:
            plotPeaksBalls(st.session_state["propAndPeaksAll"])
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
        quntifyMineralogy(st.session_state["propAndPeaksAll"], Background_peak)
        st.subheader("Statistics for all regions")
        col1Stats, col2PiePlot = st.columns(2)
        with col1Stats:
            totalParticleVolume = propertiesData["Volume"].sum()
            st.metric(
                label="regions analysed",
                value=st.session_state["regionsAnalysed"],
                delta=numberregions,
                delta_color="inverse",
                help="If number of regions analysed is very different from the number of regions segmented means something is wrong with the classification. Check the peaks and thresholds",
            )
            st.metric(
                label="Volume analysed",
                value=round(st.session_state["VolumeAnalysed2"], 0),
                delta=round(
                    st.session_state["VolumeAnalysed"]
                    / st.session_state["VolumeAnalysed2"],
                    2,
                ),
                delta_color="inverse",
                help=" compare volume fraction analysed = volume analysed / total volume",
            )
            st.metric(
                label="Number regions liberated",
                value=st.session_state["regionsLiberated"],
                help="regions with only one phase",
            )
            st.metric(
                label="Number regions with 2 phases",
                value=st.session_state["regions2Phases"],
            )
            st.metric(
                label="Number regions with more than 2 phases",
                value=st.session_state["regions3Phases"],
                help="partial volume not corrected",
            )
            print(st.session_state["VolumeAnalysed"])
            print(st.session_state["VolumeAnalysed2"])
            print(totalParticleVolume)
        with col2PiePlot:
            plotMineralogy()

with tabHistogramProperty:
    colActivate, column1, column2, column3, column4 = st.columns(5)
    with colActivate:
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
        plotProperties()
    with st.expander("Properties And Peaks"):
        st.dataframe(st.session_state["propAndPeaksAll"])

with tabFindPeaks:
    colPartA, colPartB, colPartC, colPartD, colPartE, colPartF = st.columns(6)
    with colPartA:
        PropWPeak_A = propertiesAndPeaks.loc[[st.session_state["Particle_A"]]]
        st.subheader(st.session_state["Particle_A"])
        quntifyMineralogy(PropWPeak_A, Background_peak)
        plotMineralogy()
    with colPartB:
        PropWPeak_B = propertiesAndPeaks.loc[[st.session_state["Particle_B"]]]
        st.subheader(st.session_state["Particle_B"])
        quntifyMineralogy(PropWPeak_B, Background_peak)
        plotMineralogy()
    with colPartC:
        PropWPeak_C = propertiesAndPeaks.loc[[st.session_state["Particle_C"]]]
        st.subheader(st.session_state["Particle_C"])
        quntifyMineralogy(PropWPeak_C, Background_peak)
        plotMineralogy()
    with colPartD:
        PropWPeak_D = propertiesAndPeaks.loc[[st.session_state["Particle_D"]]]
        st.subheader(st.session_state["Particle_D"])
        quntifyMineralogy(PropWPeak_D, Background_peak)
        plotMineralogy()
    with colPartE:
        PropWPeak_E = propertiesAndPeaks.loc[[st.session_state["Particle_E"]]]
        st.subheader(st.session_state["Particle_E"])
        quntifyMineralogy(PropWPeak_E, Background_peak)
        plotMineralogy()
    with colPartF:
        PropWPeak_F = propertiesAndPeaks.loc[[st.session_state["Particle_F"]]]
        st.subheader(st.session_state["Particle_F"])
        quntifyMineralogy(PropWPeak_F, Background_peak)
        plotMineralogy()

with tabAll:  # EXPERIMENTAL
    allInOne = st.checkbox("All in One")
    colleft, colRight = st.columns(2)
    if allInOne:
        with colleft:
            plotHistogramOverview(st.session_state["plotSubData1"])
        with colRight:
            plotPeaks(st.session_state["plotSubData1"], PeaksSubData)
            plotMineralogy()

            # with tabInstructions:
    #     st.write('- change the directory with the CSVs')
    #     st.write('- input the densities')
    #     st.write('- input thresholds for peaks')
    #     st.write('- press "run" button')
    #     st.write('Note: the plots are comulative from 1 to 3 phases per particle')

# def plotSphericity():          #not implemented yet
#     #creates violin plot: https://altair-viz.github.io/gallery/violin_plot.html
#     violins=alt.Chart(st.session_state['PropertiesAndPeaks'], width=100).transform_density('Sphericity',as_=['Sphericity', 'density'],extent=[5, 50],
#     groupby=['Peak_3']).mark_area(orient='horizontal').encode(alt.X('density:Q').stack('center').impute(None).title(None).axis(labels=False, values=[0], grid=False, ticks=True),
#     alt.Y('Sphericity:Q'),alt.Color('Peak_3:N'),alt.Column('Peak_3:N').spacing(0).header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)).configure_view(stroke=None)
#     st.altair_chart(violins,use_container_width=True)
# def plotEqDiameter():          #not implemented yet
# creates a comulative mass percentage for each bin of particle size for each phase: https://altair-viz.github.io/gallery/scatter_with_loess.html
# eqDiameter = alt.Chart(st.session_state['PropertiesAndPeaks']).mark_circle(opacity=0.5).transform_fold(fold=['A', 'B', 'C'],as_=['Peak_3', 'ComulativePercent']).encode(
# alt.X('equivalent_diameter:Q'),alt.Y('comulativePercent:Q'),alt.Color('Peak_3:N'))
# plot=eqDiameter + eqDiameter.transform_loess('x', 'y', groupby=['Peak_3']).mark_line(size=4)
# st.altair_chart(plot,use_container_width=True)


############################################################### Enable inclusions later
# # @st.cache_data
# def loadInclusionsHistogram():
#     Inclusions_histograms = pd.read_csv(r"C:\Users\daass73\Desktop\PlayGUI\Data\Apr24_Vivi4Quantification\Inclusions_histograms.csv")
#     Inclusions_histograms.index = Inclusions_histograms.iloc[:, 0]
#     Inclusions_histograms = Inclusions_histograms.iloc[: , 2:]
#     Properties_inclusions = pd.read_csv(r"C:\Users\daass73\Desktop\PlayGUI\Data\Apr24_Vivi4Quantification\Properties_inclusions.csv",nrows=inputNumbPart)
#     #condition for being an inclusion, >17000 because its above the iron oxide (its or condition)
#     condition = (((Properties_inclusions['vol_ratio'] <0.2) & (Properties_inclusions['inclusion_counts'] >2))|(Properties_inclusions['max_intensity'] >17000))    #What is 'vol_ratio'?????????
#     filtered_inclusions = Properties_inclusions[condition]
#     filtered_inclusions.index = filtered_inclusions['label']
#     filtered_df = Inclusions_histograms[Inclusions_histograms.index.isin(filtered_inclusions['label'])]
#     df = (filtered_df.sum(axis = 1) - filtered_inclusions['Volume'])
#     df[df>0]
#     return df, filtered_df
# #     if inclusionsBox:
#         df, filtered_df=loadInclusionsHistogram()
