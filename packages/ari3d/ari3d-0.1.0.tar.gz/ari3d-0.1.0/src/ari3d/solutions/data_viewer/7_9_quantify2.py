#  Reads h5ad data
import os
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
(
    tabHistOverview,
    tabHistogramProperty,
    tabFindPeaks,
    tabAnalysePeaks,
    tabQuantify,
) = st.tabs(
    [
        "Histogram Overview",
        "Histograms + Properties",
        "Peak Finder",
        "Analyse Peaks",
        "Quantification",
    ]
)


@st.cache_data
def directory():
    path = askdirectory(title="select folder with data")  ## folder 'data'
    return path


def fileName(path):  # select the type of histograms, must be h5ad
    filenames = os.listdir(path)  # get a list of files in the directory
    file = st.sidebar.selectbox(
        "Select a file",
        filenames,
        index=3,
        help="must click randomize button to refresh the histograms",
    )  # index3 should be bulk histograms
    return file


############################### Load-Save Paths #################################
### histograms as h5ad
import sys

dataDirectory = sys.argv[1]
file = sys.argv[2]
# load bulk histograms (= Inner + Outer)
Path_load_bulk_histogram = os.path.join(dataDirectory, file)
# load inner histograms (inside the particle without the eroded voxels)
Path_load_inner_histograms = os.path.join(dataDirectory, "Inner_volume_histograms.h5ad")
# load outer (surface layers consisting of all voxels eroded) volume histograms
Path_load_outer_histograms = os.path.join(dataDirectory, "Outer_volume_histograms.h5ad")
# load mesh histograms
Path_load_surface_mesh_histograms = os.path.join(
    dataDirectory, "Surface_mesh_histogram_0_50.h5ad"
)
# load gradient
Path_load_gradient = os.path.join(dataDirectory, "Gradient_smoothened_0_50.csv")


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
        path, "properties.csv"
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
    # Inner_volume_histograms.index = Inner_volume_histograms.iloc[:, 0]
    # Inner_volume_histograms = Inner_volume_histograms.iloc[: , 2:]
    # Inner_volume_histograms = Inner_volume_histograms.rename_axis('label')
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
    # Outer_volume_histograms.index = Outer_volume_histograms.iloc[:, 0]
    # Outer_volume_histograms = Outer_volume_histograms.iloc[: , 2:]
    # Outer_volume_histograms = Outer_volume_histograms.rename_axis('label')
    return df


@st.cache_data
def loadMesh(Path_load_surface_mesh_histograms):
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
        print("h5ad Surface mesh converted to DataFrame successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while uploading and converting the h5ad file: {e}")
    # Surface_mesh_histogram.index = Surface_mesh_histogram.iloc[:, 0]
    # Surface_mesh_histogram = Surface_mesh_histogram.iloc[: , 2:]
    # Surface_mesh_histogram = Surface_mesh_histogram.rename_axis('label')
    return df


@st.cache_data
def loadGradient(Path_load_gradient):
    Gradient = pd.read_csv(Path_load_gradient)
    # Gradient.index = Gradient['label']
    # Gradient['Max'] = Gradient[['mean_intensity1', 'mean_intensity2', 'mean_intensity3', 'mean_intensity4', 'mean_intensity5', 'mean_intensity6']].max(axis=1)
    # Gradient['Ratio'] = Gradient['mean_intensity2']/Gradient['Max']
    print("Gradient loaded")
    return Gradient


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

histogramsData, initialBins = loadHistograms(Path_load_bulk_histogram)
histogramsData = histogramsData.rename_axis("label")
histogramsData = histogramsData.astype("float64")
histogramsData = histogramsData.iloc[:, 1:]
maxParticleNumber = len(histogramsData)
propertiesData = loadProperties(dataDirectory)
propertiesData.index = propertiesData["label"]
numberParticles = len(histogramsData)

if "particleLabels" not in st.session_state:
    st.session_state["particleLabels"] = []
if "list6Particles" not in st.session_state:
    st.session_state["list6Particles"] = []
if "data_8bit" not in st.session_state:
    st.session_state["data_8bit"] = []
if "plotSubData1" not in st.session_state:
    st.session_state["plotSubData1"] = []
if "plotDataFromList" not in st.session_state:
    st.session_state["plotDataFromList"] = []
if "Particle_X" not in st.session_state:
    st.session_state["Particle_X"] = 0
if "Particle_A" not in st.session_state:
    st.session_state["Particle_A"] = 0
if "Particle_B" not in st.session_state:
    st.session_state["Particle_B"] = 0
if "Particle_C" not in st.session_state:
    st.session_state["Particle_C"] = 0
if "Particle_D" not in st.session_state:
    st.session_state["Particle_D"] = 0
if "Particle_E" not in st.session_state:
    st.session_state["Particle_E"] = 0
if "Particle_F" not in st.session_state:
    st.session_state["Particle_F"] = 0
if "Peak_Width" not in st.session_state:
    st.session_state["Peak_Width"] = 1
if "Peak_Height" not in st.session_state:
    st.session_state["Peak_Height"] = 0.000
if "Peak_Prominence" not in st.session_state:
    st.session_state["Peak_Prominence"] = 0.000
if "Peak_Horizontal_Distance" not in st.session_state:
    st.session_state["Peak_Horizontal_Distance"] = 1
if "Peak_Vertical_Distance" not in st.session_state:
    st.session_state["Peak_Vertical_Distance"] = 0.000
if "PropertiesAndPeaks" not in st.session_state:
    st.session_state["PropertiesAndPeaks"] = []
if "Phase A" not in st.session_state:
    st.session_state["Phase A"] = 0  ###########Volumes
if "Phase B" not in st.session_state:
    st.session_state["Phase B"] = 0
if "Phase C" not in st.session_state:
    st.session_state["Phase C"] = 0
if "Phase D" not in st.session_state:
    st.session_state["Phase D"] = 0
if "Phase E" not in st.session_state:
    st.session_state["Phase E"] = 0
if "ParticlesAnalysed" not in st.session_state:
    st.session_state["ParticlesAnalysed"] = 0
if "PhaseA mass" not in st.session_state:  ################## Mass
    st.session_state["PhaseA_mass"] = 0
if "PhaseB mass" not in st.session_state:
    st.session_state["PhaseB_mass"] = 0
if "PhaseC mass" not in st.session_state:
    st.session_state["PhaseC_mass"] = 0
if "PhaseD mass" not in st.session_state:
    st.session_state["PhaseD_mass"] = 0
if "VolumeAnalysed" not in st.session_state:
    st.session_state["VolumeAnalysed"] = 0


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
        alt.Chart(plotData, width=1600, height=600)
        .mark_area(opacity=0.2)
        .encode(
            x=alt.X("Y", title="Greyscale"),
            y=alt.Y("frequency", title="Frequency"),
            color=(particleNumber),
            tooltip=("X"),
        )
        .transform_filter(heatMapPartSelect)
        .interactive(bind_x=False, bind_y=True)
    )
    heatMapHistograms = (
        alt.Chart(plotData, width=1900, height=400)
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
    plot = heatMapHistograms & plotAllHistograms
    st.altair_chart(plot, use_container_width=True)


@st.cache_data
def plotPeaks(plotData, PeaksDF):
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
        alt.Chart(plotData, width=1000, height=500)
        .mark_line()
        .encode(
            x=alt.X("Y", title="Greyscale"),
            y=alt.Y("frequency", title="Frequency"),
            color=(particleNumber),
            tooltip=("X"),
        )
        .transform_filter(heatMapPartSelect)
        .interactive(bind_x=True, bind_y=True)
    )
    heatMapHistograms = (
        alt.Chart(plotData, width=700, height=400)
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
    peakMarks = (
        alt.Chart(PeaksDF, width=1000, height=500)
        .mark_circle(color="white", size=200, opacity=0.85)
        .encode(
            x=alt.X("Y", title="Greyscale"), y=alt.Y("frequency", title="Frequency")
        )
        .transform_filter(heatMapPartSelect)
    )

    plot = plotAllHistograms + peakMarks | heatMapHistograms
    with st.container():
        st.altair_chart(plot, use_container_width=True)


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
    print(Path_labelList)
    labelList = pd.read_csv(Path_labelList)
    subDataFromList = histogramsData[
        histogramsData.index.isin(labelList["Label Index"])
    ]
    st.session_state["list6Particles"] = labelList
    return subDataFromList


def saveLabelList():
    dataDirectory = sys.argv[1]
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
    # todo: remove me
    labels_array = np.array([2, 7, 4])

    if (
        st.session_state["Particle_X"] > 0
    ):  # add a specific particle to the random dataset. Be sure the label exists
        labels_array = np.append(labels_array, st.session_state["Particle_X"])
    labels_array = np.sort(labels_array)
    labels_array = pd.DataFrame(labels_array, columns=["Label Index"])
    Path_labelList = os.path.join(dataDirectory, "labelList.csv")
    labels_array.to_csv(Path_labelList, index=False)


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
    # print ('file1',file1)
    # result2 = savgol_filter(file1[1], savgolInput, 3) # 1-25
    # print ('result2',result2)
    file1 = pd.DataFrame(file1, columns=x)
    file1.index = subData1.index
    file1[file1 < 0] = 0
    st.session_state["data_8bit"] = file1
    return file1


def normalizeVolume(unNormalized):
    unNormalized = pd.DataFrame(unNormalized)
    df_new = unNormalized.loc[:, :].div(unNormalized.sum(axis=1), axis=0)
    df_new = df_new.fillna(0)
    return df_new


def transformColumnsXY(subData_ready):
    array = np.array(subData_ready)
    number_of_rows = len(array)
    number_of_columns = len(array[0])
    row = []
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            index_array = (subData_ready.index)[i]
            element = array[i][j]
            row.append([index_array, j, element])
    DataFrame = pd.DataFrame(row, dtype="float32")
    DataFrame.columns = ["X", "Y", "frequency"]
    pd.set_option("display.float_format", "{:.10f}".format)
    DataFrame["X"] = DataFrame["X"].astype(int)
    DataFrame["Y"] = DataFrame["Y"].astype(int)
    return DataFrame


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
    listOfParticles = [
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
        .transform_filter(alt.FieldOneOfPredicate(field="X", oneOf=listOfParticles))
        .interactive()
    )
    plotPropSelect = (
        alt.Chart(propertiesData, height=1000)
        .mark_point(filled=True, opacity=1)
        .encode(x=propertiesX, y=propertiesY, size=propertiesSize, color=colorStd4)
        .transform_filter(alt.FieldOneOfPredicate(field="label", oneOf=listOfParticles))
    )
    plotPropAll = (
        alt.Chart(propertiesData)
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
                particleSubdata = subDataFromList[findParticleInSubdata]
                frequency = particleSubdata["frequency"]
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
                    findPeakInParticle = particleSubdata[
                        np.any(particleSubdata == p, axis=1)
                    ]
                    PeaksDF = pd.concat([PeaksDF, findPeakInParticle], axis=0)
        plotPeaks(st.session_state["plotDataFromList"], PeaksDF)
    return PeaksDF


def applyPeaks(normalizedData):
    applyPeaksDF = pd.DataFrame(
        normalizedData
    )  # binned but maintaining the range, e.g.16bit to 8bit: 256 bins between 0-65535 (0, 256,512,768...)
    Peaks_Positions = []
    for index, row in applyPeaksDF.iterrows():
        file_row_1 = np.array(row)
        file_row_1 = file_row_1.ravel()
        file_row_1 = file_row_1.astype(float)
        file_row_1 = np.pad(file_row_1, (0, 1))
        Grey_scale = np.array(applyPeaksDF.columns, dtype=float)
        Grey_scale = np.pad(Grey_scale, (0, 1))
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
        peak_pos = Grey_scale[peaksScipy[0]]
        Peaks_Positions.append([peak_pos])
    Peaks_Positions = pd.DataFrame(Peaks_Positions)
    Peaks_Positions = pd.concat(
        [
            Peaks_Positions[0].str[0],
            Peaks_Positions[0].str[1],
            Peaks_Positions[0].str[2],
            Peaks_Positions[0].str[3],
            Peaks_Positions[0].str[4],
        ],
        axis=1,
    )
    cols = []
    count = 1
    for column in Peaks_Positions.columns:
        if column == 0:
            cols.append(f"Peak_{count}")
            count += 1
            continue
        cols.append(column)
    Peaks_Positions.columns = cols
    Peaks_Positions = Peaks_Positions.fillna(0)
    Peaks_Positions.index = applyPeaksDF.index
    with tabAnalysePeaks:
        allPeaksDF = pd.DataFrame(Peaks_Positions)
        propertiesAndPeaks = pd.concat([propertiesData, allPeaksDF], axis=1)
        propertiesAndPeaks = propertiesAndPeaks.fillna(0)
        pathAndName = os.path.join(dataDirectory, "PropertyAndPeaks.csv")
        propertiesAndPeaks.to_csv(
            pathAndName, index=False
        )  ########################add save path input
        st.session_state["PropertiesAndPeaks"] = propertiesAndPeaks


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
        peak_pos = peak_pos * numberBins
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

    with tabAnalysePeaks:
        pathAndName = os.path.join(dataDirectory, "PropertyAndPeaks.csv")
        propertiesAndPeaks.to_csv(
            pathAndName, index=False
        )  ########################add save path input
        st.session_state["PropertiesAndPeaks"] = propertiesAndPeaks
    return propertiesAndPeaks


def plotPeaksAndProperty():  # Plot in the peak analysis tab
    sizeStd1 = alt.Size(
        propertiesSize, legend=alt.Legend(title="Size Property", orient="bottom")
    )
    peak1 = alt.X("Peak_1:N", title="Peak Grey Values")
    plotProperty = alt.Y(properties, title="Property")
    colorStd4 = alt.Color("label:N", scale=alt.Scale(scheme="tableau20"), legend=None)
    plotPeak1 = (
        alt.Chart(st.session_state["PropertiesAndPeaks"], height=800)
        .mark_point(filled=True, opacity=0.9, shape="circle")
        .encode(
            x=peak1,
            y=plotProperty,
            size=sizeStd1,
            tooltip=(peak1, plotProperty),
            color=colorStd4,
        )
        .transform_filter(alt.FieldGTPredicate(field="Peak_1", gt=1))
        .interactive()
    )
    plotPeak2 = (
        alt.Chart(st.session_state["PropertiesAndPeaks"], height=800)
        .mark_point(filled=True, opacity=0.9, shape="triangle")
        .encode(
            x="Peak_2:N",
            y=plotProperty,
            size=sizeStd1,
            tooltip=("Peak_2:N", plotProperty),
            color=colorStd4,
        )
        .transform_filter(alt.FieldGTPredicate(field="Peak_2", gt=1))
        .interactive()
    )
    plotPeak3 = (
        alt.Chart(st.session_state["PropertiesAndPeaks"], height=800)
        .mark_point(filled=True, opacity=0.9, shape="square")
        .encode(
            x="Peak_3:N",
            y=plotProperty,
            size=sizeStd1,
            tooltip=("Peak_3:N", plotProperty),
            color=colorStd4,
        )
        .transform_filter(alt.FieldGTPredicate(field="Peak_3", gt=1))
        .interactive()
    )
    plotAllPeaks = plotPeak1 + plotPeak2 + plotPeak3
    with tabAnalysePeaks:
        st.altair_chart(plotAllPeaks, use_container_width=True)


def plotPeaksBalls():
    PaP = pd.DataFrame(st.session_state["PropertiesAndPeaks"])
    allPeaks = pd.concat(
        [PaP["Peak_1"], PaP["Peak_2"], PaP["Peak_3"], PaP["Peak_4"]], ignore_index=True
    )
    countsTotal = pd.DataFrame(allPeaks.value_counts())
    countsTotal = countsTotal.reset_index()
    countsTotal = countsTotal.drop(0)
    testPeakBalls = (
        alt.Chart(countsTotal, height=300)
        .mark_circle(opacity=0.8, stroke="black", strokeWidth=2, strokeOpacity=0.4)
        .encode(
            x=alt.X("index:Q", title="Peak grey-value"),
            size="count:N",
            color=alt.Color(
                "count:N",
                scale=alt.Scale(scheme="darkred"),
                legend=alt.Legend(title="count", orient="bottom"),
            ),
        )
        .properties(width=450, height=180)
        .configure_axisX(grid=True)
        .configure_view(stroke=None)
        .interactive()
    )
    st.altair_chart(testPeakBalls, use_container_width=True)
    # testViolinPeaks=alt.Chart(countsDF).mark_bar(orient='horizontal').transform_density('Peak_1',as_=['Peak_1', 'density'],bandwidth=binInput, steps=binInput*2).encode(y='Peak_1:Q',x=alt.X(
    #     'density:Q',stack='center',impute=None,axis=alt.Axis(ticks=True))).interactive()
    # st.altair_chart(testViolinPeaks)


def quntifyMineralogy(dataDirectory):
    def plotMineralogy():
        # creates pie chart
        mineralogy = pd.DataFrame(
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
        colorStd2 = alt.Color(
            "mineral:N",
            scale=alt.Scale(scheme="accent"),
            legend=alt.Legend(title="Mineral", orient="bottom"),
        )
        mineralPlot = (
            alt.Chart(mineralogy).mark_arc().encode(theta="value", color=colorStd2)
        )
        st.altair_chart(mineralPlot, use_container_width=True)

    def plotSphericity():  # not implemented yet
        # creates violin plot: https://altair-viz.github.io/gallery/violin_plot.html
        violins = (
            alt.Chart(st.session_state["PropertiesAndPeaks"], width=100)
            .transform_density(
                "Sphericity",
                as_=["Sphericity", "density"],
                extent=[5, 50],
                groupby=["Peak_3"],
            )
            .mark_area(orient="horizontal")
            .encode(
                alt.X("density:Q")
                .stack("center")
                .impute(None)
                .title(None)
                .axis(labels=False, values=[0], grid=False, ticks=True),
                alt.Y("Sphericity:Q"),
                alt.Color("Peak_3:N"),
                alt.Column("Peak_3:N")
                .spacing(0)
                .header(titleOrient="bottom", labelOrient="bottom", labelPadding=0),
            )
            .configure_view(stroke=None)
        )
        st.altair_chart(violins, use_container_width=True)

    def plotEqDiameter():  # not implemented yet
        # creates a comulative mass percentage for each bin of particle size for each phase: https://altair-viz.github.io/gallery/scatter_with_loess.html
        eqDiameter = (
            alt.Chart(st.session_state["PropertiesAndPeaks"])
            .mark_circle(opacity=0.5)
            .transform_fold(fold=["A", "B", "C"], as_=["Peak_3", "ComulativePercent"])
            .encode(
                alt.X("equivalent_diameter:Q"),
                alt.Y("comulativePercent:Q"),
                alt.Color("Peak_3:N"),
            )
        )
        plot = eqDiameter + eqDiameter.transform_loess(
            "x", "y", groupby=["Peak_3"]
        ).mark_line(size=4)
        st.altair_chart(plot, use_container_width=True)

    ########################## Quantifies phase mass % from peak properties and histograms ################
    #### only liberated particles
    def quantifyLiberatedParticles():
        propertiesDataWPeaks = st.session_state["PropertiesAndPeaks"]
        array = propertiesDataWPeaks[
            ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
        ]  # list of peaks
        array = array.fillna(0)
        array[array > 65535] = 65535
        Quantify_LiberatedParticle = []
        Index_LiberatedParticle = []
        AllPeaks = []
        nVoxels_Outer_LiberatedParticle_append = []
        # Iterating rows
        i = 0
        for index, row in histogramsData.iterrows():
            Peaks = array.iloc[
                [i]
            ].values  # list of peaks per particle (grey values 16bit)
            # if only one peak in the particle
            if (
                np.count_nonzero(Peaks > background_peak_pos) == 1
            ) and i > -1:  # condition of only 1 peak
                Partical_peak = Peaks[Peaks > background_peak_pos]
                Partical_peak = int((Partical_peak).flat[0])
                # Takes the sum of ith row from phase 1 minimum threshold greyscale value till Phase1_max_limit
                Sum_phase = histogramsData.iloc[i, Partical_peak:65535].sum()
                index = int((array.iloc[[i]].index.values).flat[0])
                Quantify_LiberatedParticle.append([Sum_phase])
                Index_LiberatedParticle.append(
                    [index]
                )  ##########creates 2 lists, one with index and one with peak greyvalue
                AllPeaks.append([Partical_peak])
                # linear equation from peak position to background. creates a list (then array) with each entry is the result of the equation
                multiple_to_background_LiberatedParticle = np.arange(
                    0, 1, 1 / ((Partical_peak - 1) - background_peak_pos)
                )
                multiple_to_background_LiberatedParticle = np.array(
                    multiple_to_background_LiberatedParticle
                )
                if len(
                    histogramsData.iloc[i, background_peak_pos:Partical_peak]
                ) == len(multiple_to_background_LiberatedParticle):
                    No_of_voxels_towards_background_phase_1 = histogramsData.iloc[
                        i, background_peak_pos:Partical_peak
                    ]
                elif len(
                    histogramsData.iloc[i, background_peak_pos:Partical_peak]
                ) > len(multiple_to_background_LiberatedParticle):
                    No_of_voxels_towards_background_phase_1 = histogramsData.iloc[
                        i, background_peak_pos : Partical_peak - 1
                    ]
                else:
                    No_of_voxels_towards_background_phase_1 = histogramsData.iloc[
                        i, background_peak_pos : Partical_peak + 1
                    ]
                # Outher referes to bins lower grey value than the peak (affected by partial volume)
                nVoxels_Outer_LiberatedParticle_array = (
                    No_of_voxels_towards_background_phase_1
                    * multiple_to_background_LiberatedParticle
                )
                nVoxels_Outer_LiberatedParticle_array = (
                    nVoxels_Outer_LiberatedParticle_array.sum()
                )
                st.session_state["VolumeAnalysed"] = (
                    st.session_state["VolumeAnalysed"]
                    + nVoxels_Outer_LiberatedParticle_array
                )
                nVoxels_Outer_LiberatedParticle_append.append(
                    [nVoxels_Outer_LiberatedParticle_array]
                )
                st.session_state["ParticlesLiberated"] = (
                    st.session_state["ParticlesLiberated"] + 1
                )
                st.session_state["ParticlesAnalysed"] = (
                    st.session_state["ParticlesAnalysed"] + 1
                )
            i = i + 1

        nVoxels_Outer_LiberatedParticle = pd.DataFrame(
            nVoxels_Outer_LiberatedParticle_append,
            columns=["nVoxels_Outer_LiberatedParticle"],
        )
        Quantify_LiberatedParticle = pd.DataFrame(
            Quantify_LiberatedParticle, columns=["nVoxels_inner_LiberatedParticle"]
        )
        Quantify_LiberatedParticle["total_nVoxels_LiberatedParticle"] = (
            Quantify_LiberatedParticle["nVoxels_inner_LiberatedParticle"]
            + nVoxels_Outer_LiberatedParticle["nVoxels_Outer_LiberatedParticle"]
        )
        Index_LiberatedParticle = pd.DataFrame(
            Index_LiberatedParticle, columns=["Label"]
        )
        AllPeaks = pd.DataFrame(AllPeaks, columns=["All Peaks"])
        # Forcing the 100% to be the ideal peak position (biggest particles) -> change in the future to the detected peak position
        Quantify_LiberatedParticle_sorted = pd.DataFrame(
            columns=[
                "Peak_1",
                "Peak_2",
                "Peak_3",
                "Peak_4",
                "Peak_5",
                "Phase_1_total_quantification",
                "Phase_2_total_quantification",
                "Phase_3_total_quantification",
                "Phase_4_total_quantification",
                "Phase_5_total_quantification",
            ]
        )

        Quantify_LiberatedParticle_sorted["Peak_1"] = np.where(
            AllPeaks["All Peaks"] <= Phase_1_threshold, AllPeaks["All Peaks"], 0
        )
        Quantify_LiberatedParticle_sorted["Phase_1_total_quantification"] = np.where(
            AllPeaks["All Peaks"] <= Phase_1_threshold,
            Quantify_LiberatedParticle["total_nVoxels_LiberatedParticle"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Peak_2"] = np.where(
            (AllPeaks["All Peaks"] > Phase_1_threshold)
            & (AllPeaks["All Peaks"] <= Phase_2_threshold),
            AllPeaks["All Peaks"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Phase_2_total_quantification"] = np.where(
            (AllPeaks["All Peaks"] > Phase_1_threshold)
            & (AllPeaks["All Peaks"] <= Phase_2_threshold),
            Quantify_LiberatedParticle["total_nVoxels_LiberatedParticle"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Peak_3"] = np.where(
            (AllPeaks["All Peaks"] > Phase_2_threshold)
            & (AllPeaks["All Peaks"] <= Phase_3_threshold),
            AllPeaks["All Peaks"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Phase_3_total_quantification"] = np.where(
            (AllPeaks["All Peaks"] > Phase_2_threshold)
            & (AllPeaks["All Peaks"] <= Phase_3_threshold),
            Quantify_LiberatedParticle["total_nVoxels_LiberatedParticle"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Peak_4"] = np.where(
            (AllPeaks["All Peaks"] > Phase_3_threshold)
            & (AllPeaks["All Peaks"] <= Phase_4_threshold),
            AllPeaks["All Peaks"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Phase_4_total_quantification"] = np.where(
            (AllPeaks["All Peaks"] > Phase_3_threshold)
            & (AllPeaks["All Peaks"] <= Phase_4_threshold),
            Quantify_LiberatedParticle["total_nVoxels_LiberatedParticle"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Peak_5"] = np.where(
            (AllPeaks["All Peaks"] > Phase_4_threshold)
            & (AllPeaks["All Peaks"] <= Phase_5_threshold),
            AllPeaks["All Peaks"],
            0,
        )
        Quantify_LiberatedParticle_sorted["Phase_5_total_quantification"] = np.where(
            (AllPeaks["All Peaks"] > Phase_4_threshold)
            & (AllPeaks["All Peaks"] <= Phase_5_threshold),
            Quantify_LiberatedParticle["total_nVoxels_LiberatedParticle"],
            0,
        )

        Quantify_LiberatedParticle_sorted["Label"] = Index_LiberatedParticle["Label"]
        Quantify_LiberatedParticle_sorted.index = Index_LiberatedParticle["Label"]

        Quantification = pd.concat([Quantify_LiberatedParticle_sorted], axis=0)
        Quantification = Quantification.sort_index(ascending=True)
        Quantification["Total_quantification"] = (
            Quantification["Phase_1_total_quantification"]
            + Quantification["Phase_2_total_quantification"]
            + Quantification["Phase_3_total_quantification"]
            + Quantification["Phase_4_total_quantification"]
            + Quantification["Phase_5_total_quantification"]
        )
        Quantification["Difference"] = (
            propertiesDataWPeaks["Volume"] - Quantification["Total_quantification"]
        )

        # volume to mass fraction conversion
        if Quantification.shape[0] > 0:  # check if there are this type of particles
            mass_p1 = (
                Quantification["Phase_1_total_quantification"].sum()
            ) * inputDensityA
            st.session_state["PhaseA_mass"] = mass_p1
            mass_p2 = (
                Quantification["Phase_2_total_quantification"].sum()
            ) * inputDensityB
            st.session_state["PhaseB_mass"] = mass_p2
            mass_p3 = (
                Quantification["Phase_3_total_quantification"].sum()
            ) * inputDensityC
            st.session_state["PhaseC_mass"] = mass_p3
            mass_p4 = (
                Quantification["Phase_4_total_quantification"].sum()
            ) * inputDensityD
            st.session_state["PhaseD_mass"] = mass_p4
            mass_p5 = (
                Quantification["Phase_5_total_quantification"].sum()
            ) * inputDensityE
            st.session_state["PhaseE_mass"] = mass_p5
            st.session_state["VolumeAnalysed"] = (
                Quantification["Phase_1_total_quantification"].sum()
                + Quantification["Phase_2_total_quantification"].sum()
                + Quantification["Phase_3_total_quantification"].sum()
                + Quantification["Phase_4_total_quantification"].sum()
                + Quantification["Phase_5_total_quantification"].sum()
            )
            totalMass = mass_p1 + mass_p2 + mass_p3 + mass_p4 + mass_p5
            st.session_state["Phase A"] = round(mass_p1 * 100 / totalMass, 1)
            st.session_state["Phase B"] = round(mass_p2 * 100 / totalMass, 1)
            st.session_state["Phase C"] = round(mass_p3 * 100 / totalMass, 1)
            st.session_state["Phase D"] = round(mass_p4 * 100 / totalMass, 1)
            st.session_state["Phase E"] = round(mass_p5 * 100 / totalMass, 1)

    #### 2 Phases per particle
    def quantifyTwoPhasesParticle(
        Inner_volume_histograms,
        Outer_volume_histograms,
        Surface_mesh_histogram,
        Gradient,
    ):
        propertiesDataWPeaks = st.session_state["PropertiesAndPeaks"]
        array = propertiesDataWPeaks[["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]]
        array = array.fillna(0)
        array[array > 65535] = 65535
        Quantification_all_2_phases_1 = []
        Quantification_all_2_phases_2 = []
        Quantification_out_of_peaks_phase_1 = []
        Quantification_out_of_peaks_phase_2 = []
        Quantification_Outer_phase_1 = []
        Quantification_Outer_phase_2 = []
        Surface_ratio_data = []
        OT_append = []
        IT_append = []
        PVE_volume = []
        Peaks_1_phase = []  # phase in a particle with the lowest attenuation
        Peaks_2_phase = []  # phase in a particle with highest attenuation
        Index_2_phase = []
        i = 0
        for index, row in Inner_volume_histograms.iterrows():
            Peaks = array.iloc[[i]].values  # list of peaks per particle
            if (
                np.count_nonzero(Peaks > background_peak_pos) == 2
            ) and i > -1:  # condition 2 peaks per particle
                Partical_peak = Peaks[Peaks > background_peak_pos]
                IT = Inner_volume_histograms.iloc[
                    i, 0:65535
                ].sum()  # sum of voxels inside the particle (no PV with background)
                IT_append.append([IT])
                Partical_peak_1 = int(
                    (Partical_peak).flat[0]
                )  # first entry in the list of peaks (Particle_peak)
                Partical_peak_1 = int(float(Partical_peak_1))

                # Conditions to find the maximum grey value of the least attenuating phase in a particle (Phase_1)
                if Partical_peak_1 < Phase_1_threshold:
                    Phase_limit = Phase_1_threshold
                elif Phase_1_threshold <= Partical_peak_1 < Phase_2_threshold:
                    Phase_limit = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_1 < Phase_3_threshold:
                    Phase_limit = Phase_3_threshold
                elif Phase_3_threshold <= Partical_peak_1 < Phase_4_threshold:
                    Phase_limit = Phase_4_threshold
                elif Phase_4_threshold <= Partical_peak_1 < Phase_5_threshold:
                    Phase_limit = Phase_5_threshold

                Partical_peak_2 = int(
                    (Partical_peak).flat[1]
                )  # second entry in the list of peaks
                Partical_peak_2 = int(float(Partical_peak_2))
                # ATTENTION: everything bellow peak1 and above peak2 are considered 100% of phase1 or phase 2 respectively!!!!!!!!!
                Sum_phase_1 = Inner_volume_histograms.iloc[
                    i, background_peak_pos:Partical_peak_1
                ].sum()  # voxels bellow peak 1
                Sum_phase_2 = Inner_volume_histograms.iloc[
                    i, Partical_peak_2:65535
                ].sum()  # voxels above peak 2
                # Appending the phase 2 quantification sum
                Quantification_all_2_phases_2.append([Sum_phase_2])
                Peaks_1_phase.append([Partical_peak_1])
                Peaks_2_phase.append([Partical_peak_2])

                # Creating a vector of linear equatin with which phase 2 transition towards phase 1 voxels will be multiplied
                No_of_voxels = Inner_volume_histograms.iloc[
                    i, Partical_peak_1:Partical_peak_2
                ]  # voxels between peak 1 and peak 2
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

                # Calculte the quantification of phase 2 towards phase 1 voxels
                out_of_peak_volume_2 = No_of_voxels * multiples_towards_Partical_peak_1
                out_of_peak_volume_1 = No_of_voxels * multiples_towards_Partical_peak_2
                # Appending the phase 1 quantification sum
                Quantification_all_2_phases_1.append([Sum_phase_1])
                out_of_peak_volume_1 = out_of_peak_volume_1.sum()
                Quantification_out_of_peaks_phase_1.append([out_of_peak_volume_1])
                out_of_peak_volume_2 = out_of_peak_volume_2.sum()
                Quantification_out_of_peaks_phase_2.append([out_of_peak_volume_2])
                index = int((array.iloc[[i]].index.values).flat[0])
                Index_2_phase.append([index])

                # Outer volume - interphases with the background
                Oter_volume_full_phase_1 = Outer_volume_histograms.iloc[
                    i, Partical_peak_1:Phase_limit
                ].sum()  # grey values between the peak and the threshold of the next phase (not necessarily Phase 2), peak2-background?????
                Oter_volume_full_phase_2 = Outer_volume_histograms.iloc[
                    i, Partical_peak_2:65535
                ].sum()  # grey values larger than peak 2 (should be zero!!!!!)
                OT = Outer_volume_histograms.iloc[i, 0:65535].sum()
                multiples_towards_background_phase_1 = np.arange(
                    0, 1, 1 / ((Partical_peak_1 - 1) - background_peak_pos)
                )
                multiples_towards_background_phase_1 = np.array(
                    multiples_towards_background_phase_1
                )
                if len(
                    Outer_volume_histograms.iloc[i, background_peak_pos:Partical_peak_1]
                ) == len(multiples_towards_background_phase_1):
                    No_of_voxels_towards_background_phase_1 = (
                        Outer_volume_histograms.iloc[
                            i, background_peak_pos:Partical_peak_1
                        ]
                    )
                elif len(
                    Outer_volume_histograms.iloc[i, background_peak_pos:Partical_peak_1]
                ) > len(multiples_towards_background_phase_1):
                    No_of_voxels_towards_background_phase_1 = (
                        Outer_volume_histograms.iloc[
                            i, background_peak_pos : Partical_peak_1 - 1
                        ]
                    )
                else:
                    No_of_voxels_towards_background_phase_1 = (
                        Outer_volume_histograms.iloc[
                            i, background_peak_pos : Partical_peak_1 + 1
                        ]
                    )
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
                    Outer_volume_histograms.iloc[i, background_peak_pos:Partical_peak_2]
                ) == len(multiples_towards_background_phase_2):
                    No_of_voxels_towards_background_phase_2 = (
                        Outer_volume_histograms.iloc[
                            i, background_peak_pos:Partical_peak_2
                        ]
                    )
                elif len(
                    Outer_volume_histograms.iloc[i, background_peak_pos:Partical_peak_2]
                ) > len(multiples_towards_background_phase_2):
                    No_of_voxels_towards_background_phase_2 = (
                        Outer_volume_histograms.iloc[
                            i, background_peak_pos : Partical_peak_2 - 1
                        ]
                    )
                else:
                    No_of_voxels_towards_background_phase_2 = (
                        Outer_volume_histograms.iloc[
                            i, background_peak_pos : Partical_peak_2 + 1
                        ]
                    )
                Quantification_Outer_phase_2_array = (
                    No_of_voxels_towards_background_phase_2
                    * multiples_towards_background_phase_2
                )

                Vol_to_subtract_from_phase_1 = Quantification_Outer_phase_2_array[
                    background_peak_pos:Phase_limit
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
                    Oter_volume_full_phase_1
                    + Oter_volume_full_phase_2
                    + Quantification_Outer_phase_1_array
                    + Quantification_Outer_phase_2_array
                )  # ???????????????????
                PVE_volume.append([PVE_adjusted_volume])  # ???????????????????
                OT_append.append([OT])
                # Gradient ratio is a factor <1 that is multiplied by the peak position (int(gradient_ratio*Phase_limit))
                # in order to predict where the peak is expected at the second eroded layer used to derive the surface mesh (shift to lower greyvalues)
                # The surface_ratio of phase 1 is number of voxels between the background and the peak1 threshold (recalculated to the surface using the gradient_ratio) divided by the total number of voxels on the surface
                Gradient_ratio = Gradient.iloc[i]["Gradient_2"]
                if Gradient_ratio < 0.75:
                    Gradient_ratio = 0.75
                Surface_ratio = (
                    Surface_mesh_histogram.iloc[
                        i, background_peak_pos : int(Gradient_ratio * Phase_limit)
                    ].sum()
                ) / (Surface_mesh_histogram.iloc[i, background_peak_pos:65536].sum())
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
                Surface_ratio_data.append([Surface_ratio])
                st.session_state["Particles2Phases"] = (
                    st.session_state["Particles2Phases"] + 1
                )
                st.session_state["ParticlesAnalysed"] = (
                    st.session_state["ParticlesAnalysed"] + 1
                )

            i = i + 1

        PVE_volume = pd.DataFrame(PVE_volume, columns=["PVE_volume"])
        OT_append = pd.DataFrame(OT_append, columns=["OT_append"])
        IT_append = pd.DataFrame(IT_append, columns=["IT_append"])

        Quantification_all_2_phases_1 = pd.DataFrame(
            Quantification_all_2_phases_1, columns=["Phase_1_quantification_outer"]
        )
        Quantification_all_2_phases_2 = pd.DataFrame(
            Quantification_all_2_phases_2, columns=["Phase_2_quantification_outer"]
        )
        Index_2_phase = pd.DataFrame(Index_2_phase, columns=["Label"])

        Quantification_out_of_peaks_1 = pd.DataFrame(
            Quantification_out_of_peaks_phase_1,
            columns=["Quantification_out_of_peaks_1_outer"],
        )
        Quantification_out_of_peaks_1 = Quantification_out_of_peaks_1.fillna(0)
        Quantification_out_of_peaks_2 = pd.DataFrame(
            Quantification_out_of_peaks_phase_2,
            columns=["Quantification_out_of_peaks_2_outer"],
        )
        Quantification_out_of_peaks_2 = Quantification_out_of_peaks_2.fillna(0)
        Quantification_Outer_phase_1 = pd.DataFrame(
            Quantification_Outer_phase_1, columns=["Quantification_Outer_phase_1"]
        )
        Quantification_Outer_phase_1 = Quantification_Outer_phase_1.fillna(0)
        Quantification_Outer_phase_2 = pd.DataFrame(
            Quantification_Outer_phase_2, columns=["Quantification_Outer_phase_2"]
        )
        Quantification_Outer_phase_2 = Quantification_Outer_phase_2.fillna(0)

        Surface_ratio_data = pd.DataFrame(Surface_ratio_data, columns=["Surface_ratio"])
        Surface_ratio_data = Surface_ratio_data.fillna(0)

        # Phase_limit_data = pd.DataFrame(Phase_limit_data, columns = ["Phase_limit"])         ?????????????
        # Phase_limit_data = Phase_limit_data.fillna(0)

        Peaks_1_phase = pd.DataFrame(Peaks_1_phase, columns=["Peak_1"])
        Peaks_2_phase = pd.DataFrame(Peaks_2_phase, columns=["Peak_2"])

        Quantification_2_phases_inner = pd.concat(
            [
                Index_2_phase,
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
                "Label",
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
        # Quantification_2_phases = Quantification_2_phases[['Label','Peak_1','Peak_2','total_quantification_phase_1','total_quantification_phase_2']]

        Quantification_2_phases_sum = (
            Quantification_2_phases["total_quantification_phase_1"]
            + Quantification_2_phases["total_quantification_phase_2"]
        )
        Quantification_2_phases_sum = pd.DataFrame(
            Quantification_2_phases_sum, columns=["Total_Sum"]
        )

        # Reorganize the dataset to attribute the two phases in each particle to the right phase/class output
        cols = ["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]
        thresholds = [
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
            Phase_5_threshold,
        ]

        Quantification_2_phase_sorted = pd.DataFrame(
            columns=cols + [f"Phase_{i}_total_quantification" for i in range(1, 7)]
        )  # number of phases +2
        Quantification_2_phase_sorted_1 = Quantification_2_phase_sorted.copy()
        for i in range(1, 6):  # number of phases +1
            mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
                Peaks_1_phase["Peak_1"] <= thresholds[i]
            )
            Quantification_2_phase_sorted[f"Peak_{i}"] = np.where(
                mask, Peaks_1_phase["Peak_1"], 0
            )
            Quantification_2_phase_sorted[f"Phase_{i}_total_quantification"] = np.where(
                mask, Quantification_2_phases[f"total_quantification_phase_1"], 0
            )
        for i in range(1, 6):  # number of phases +1
            mask = (Peaks_2_phase["Peak_2"] > thresholds[i - 1]) & (
                Peaks_2_phase["Peak_2"] <= thresholds[i]
            )
            Quantification_2_phase_sorted_1[f"Peak_{i}"] = np.where(
                mask, Peaks_2_phase["Peak_2"], 0
            )
            Quantification_2_phase_sorted_1[
                f"Phase_{i}_total_quantification"
            ] = np.where(
                mask, Quantification_2_phases[f"total_quantification_phase_2"], 0
            )

        Quantification = Quantification_2_phase_sorted.mask(
            Quantification_2_phase_sorted == 0, Quantification_2_phase_sorted_1
        )
        Quantification["Label"] = Quantification_2_phases["Label"]
        Quantification.index = Quantification["Label"]

        # volume to mass fraction conversion
        if Quantification.shape[0] > 0:  # check if there are this type of particles
            mass_p1 = (
                Quantification["Phase_1_total_quantification"].sum()
            ) * inputDensityA
            st.session_state["PhaseA_mass"] = st.session_state["PhaseA_mass"] + mass_p1
            mass_p2 = (
                Quantification["Phase_2_total_quantification"].sum()
            ) * inputDensityB
            st.session_state["PhaseB_mass"] = st.session_state["PhaseB_mass"] + mass_p2
            mass_p3 = (
                Quantification["Phase_3_total_quantification"].sum()
            ) * inputDensityC
            st.session_state["PhaseC_mass"] = st.session_state["PhaseC_mass"] + mass_p3
            mass_p4 = (
                Quantification["Phase_4_total_quantification"].sum()
            ) * inputDensityD
            st.session_state["PhaseD_mass"] = st.session_state["PhaseD_mass"] + mass_p4
            mass_p5 = (
                Quantification["Phase_5_total_quantification"].sum()
            ) * inputDensityE
            st.session_state["PhaseE_mass"] = st.session_state["PhaseE_mass"] + mass_p5
            st.session_state["VolumeAnalysed"] = (
                st.session_state["VolumeAnalysed"]
                + Quantification["Phase_1_total_quantification"].sum()
                + Quantification["Phase_2_total_quantification"].sum()
                + Quantification["Phase_3_total_quantification"].sum()
                + Quantification["Phase_4_total_quantification"].sum()
                + Quantification["Phase_5_total_quantification"].sum()
            )
            totalMass = mass_p1 + mass_p2 + mass_p3 + mass_p4 + mass_p5
            st.session_state["Phase A"] = round(mass_p1 * 100 / totalMass, 1)
            st.session_state["Phase B"] = round(mass_p2 * 100 / totalMass, 1)
            st.session_state["Phase C"] = round(mass_p3 * 100 / totalMass, 1)
            st.session_state["Phase D"] = round(mass_p4 * 100 / totalMass, 1)
            st.session_state["Phase E"] = round(mass_p5 * 100 / totalMass, 1)

    #### 3 Phases per particle
    def quantify3Phases_particle():
        propertiesDataWPeaks = st.session_state["PropertiesAndPeaks"]
        array = propertiesDataWPeaks[["Peak_1", "Peak_2", "Peak_3", "Peak_4", "Peak_5"]]
        array = array.fillna(0)
        array[array > 65535] = 65535
        Quantification_all_3_phases_1 = []
        Quantification_all_3_phases_2 = []
        Quantification_all_3_phases_3 = []
        Peaks_1_phase = []
        Peaks_2_phase = []
        Peaks_3_phase = []
        Index_3_phase = []
        i = 0
        for index, row in histogramsData.iterrows():
            Peaks = array.iloc[[i]].values
            if (np.count_nonzero(Peaks > background_peak_pos) == 3) and i > -1:
                Partical_peak = Peaks[Peaks > background_peak_pos]
                Partical_peak_1 = Partical_peak.flat[0]
                Partical_peak_1 = int(float(Partical_peak_1))
                Partical_peak_2 = Partical_peak.flat[1]
                Partical_peak_2 = int(float(Partical_peak_2))
                Partical_peak_3 = Partical_peak.flat[2]
                Partical_peak_3 = int(float(Partical_peak_3))

                if Partical_peak_1 < Phase_1_threshold:
                    Phase_limit = Phase_1_threshold
                elif Phase_1_threshold <= Partical_peak_1 < Phase_2_threshold:
                    Phase_limit = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_1 < Phase_3_threshold:
                    Phase_limit = Phase_3_threshold
                elif Phase_3_threshold <= Partical_peak_1 < Phase_4_threshold:
                    Phase_limit = Phase_4_threshold
                elif Phase_4_threshold <= Partical_peak_1 < Phase_5_threshold:
                    Phase_limit = Phase_5_threshold

                if Partical_peak_2 < Phase_1_threshold:
                    Phase_limit_2 = Phase_1_threshold
                elif Phase_1_threshold <= Partical_peak_2 < Phase_2_threshold:
                    Phase_limit_2 = Phase_2_threshold
                elif Phase_2_threshold <= Partical_peak_2 < Phase_3_threshold:
                    Phase_limit_2 = Phase_3_threshold
                elif Phase_3_threshold <= Partical_peak_2 < Phase_4_threshold:
                    Phase_limit_2 = Phase_4_threshold
                elif Phase_4_threshold <= Partical_peak_2 < Phase_5_threshold:
                    Phase_limit_2 = Phase_5_threshold
                # Sum between the minimum greyscale value of Phase 1 (less attenuating of the 3 phases in a particle) until Phase1_max_limit
                Sum_phase_1 = histogramsData.iloc[
                    i, background_peak_pos:Phase_limit
                ].sum()
                Sum_phase_1 = Sum_phase_1.sum()
                Quantification_all_3_phases_1.append([Sum_phase_1])
                # Sum between the minimum greyscale value of Phase 2 (middle attenuating of the 3 phases) until Phase2_max_limit
                Sum_phase_2 = histogramsData.iloc[i, Phase_limit:Phase_limit_2].sum()
                Sum_phase_2 = Sum_phase_2.sum()
                Quantification_all_3_phases_2.append([Sum_phase_2])
                # Sum between the minimum greyscale value of Phase 3 (highest attenuating of the 3 phases in a particle) until Phase3_max_limit
                Sum_phase_3 = histogramsData.iloc[i, Phase_limit_2:65535].sum()
                Sum_phase_3 = Sum_phase_3.sum()
                Quantification_all_3_phases_3.append([Sum_phase_3])

                index = int((array.iloc[[i]].index.values).flat[0])
                Index_3_phase.append([index])

                Peaks_1_phase.append([Partical_peak_1])
                Peaks_2_phase.append([Partical_peak_2])
                Peaks_3_phase.append([Partical_peak_3])

                st.session_state["Particles3Phases"] = (
                    st.session_state["Particles3Phases"] + 1
                )
                st.session_state["ParticlesAnalysed"] = (
                    st.session_state["ParticlesAnalysed"] + 1
                )
            i = i + 1
        # Quantification_all: quantifies voxels which have 100% a phase
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
        thresholds = [
            Phase_0_threshold,
            Phase_1_threshold,
            Phase_2_threshold,
            Phase_3_threshold,
            Phase_4_threshold,
            Phase_5_threshold,
        ]
        Quantification_3_phase_sorted = pd.DataFrame(
            columns=cols + [f"Phase_{i}_total_quantification" for i in range(1, 7)]
        )  # empty
        Quantification_3_phase_sorted_1 = Quantification_3_phase_sorted.copy()  # empty
        Quantification_3_phase_sorted_2 = Quantification_3_phase_sorted.copy()  # empty
        for i in range(1, 6):
            mask = (Peaks_1_phase["Peak_1"] > thresholds[i - 1]) & (
                Peaks_1_phase["Peak_1"] <= thresholds[i]
            )
            Quantification_3_phase_sorted[f"Peak_{i}"] = np.where(
                mask, Peaks_1_phase["Peak_1"], 0
            )
            Quantification_3_phase_sorted[f"Phase_{i}_total_quantification"] = np.where(
                mask, Quantification_3_phases[f"total_quantification_phase_1"], 0
            )
        for i in range(1, 6):
            mask = (Peaks_2_phase["Peak_2"] > thresholds[i - 1]) & (
                Peaks_2_phase["Peak_2"] <= thresholds[i]
            )
            Quantification_3_phase_sorted_1[f"Peak_{i}"] = np.where(
                mask, Peaks_2_phase["Peak_2"], 0
            )
            Quantification_3_phase_sorted_1[
                f"Phase_{i}_total_quantification"
            ] = np.where(
                mask, Quantification_3_phases[f"total_quantification_phase_2"], 0
            )
        for i in range(1, 6):
            mask = (Peaks_3_phase["Peak_3"] > thresholds[i - 1]) & (
                Peaks_3_phase["Peak_3"] <= thresholds[i]
            )
            Quantification_3_phase_sorted_2[f"Peak_{i}"] = np.where(
                mask, Peaks_3_phase["Peak_3"], 0
            )
            Quantification_3_phase_sorted_2[
                f"Phase_{i}_total_quantification"
            ] = np.where(
                mask, Quantification_3_phases[f"total_quantification_phase_3"], 0
            )
        Quantification_3_phase_sorted = Quantification_3_phase_sorted.mask(
            Quantification_3_phase_sorted == 0, Quantification_3_phase_sorted_1
        )
        Quantification_3_phase_sorted = Quantification_3_phase_sorted.mask(
            Quantification_3_phase_sorted == 0, Quantification_3_phase_sorted_2
        )
        Quantification_3_phase_sorted.index = Quantification_3_phases["Label"]
        Quantification_3_phase_sorted["Label"] = Quantification_3_phase_sorted.index

        # volume to mass fraction conversion
        if (
            Quantification_3_phase_sorted.shape[0] > 0
        ):  # check if there are this type of particles
            mass_p1 = (
                Quantification_3_phase_sorted["Phase_1_total_quantification"].sum()
            ) * inputDensityA
            st.session_state["PhaseA_mass"] = st.session_state["PhaseA_mass"] + mass_p1
            mass_p2 = (
                Quantification_3_phase_sorted["Phase_2_total_quantification"].sum()
            ) * inputDensityB
            st.session_state["PhaseB_mass"] = st.session_state["PhaseB_mass"] + mass_p2
            mass_p3 = (
                Quantification_3_phase_sorted["Phase_3_total_quantification"].sum()
            ) * inputDensityC
            st.session_state["PhaseC_mass"] = st.session_state["PhaseC_mass"] + mass_p3
            mass_p4 = (
                Quantification_3_phase_sorted["Phase_4_total_quantification"].sum()
            ) * inputDensityD
            st.session_state["PhaseD_mass"] = st.session_state["PhaseD_mass"] + mass_p4
            mass_p5 = (
                Quantification_3_phase_sorted["Phase_5_total_quantification"].sum()
            ) * inputDensityE
            st.session_state["PhaseE_mass"] = st.session_state["PhaseE_mass"] + mass_p5
            st.session_state["VolumeAnalysed"] = (
                st.session_state["VolumeAnalysed"]
                + Quantification_3_phase_sorted["Phase_1_total_quantification"].sum()
                + Quantification_3_phase_sorted["Phase_2_total_quantification"].sum()
                + Quantification_3_phase_sorted["Phase_3_total_quantification"].sum()
                + Quantification_3_phase_sorted["Phase_4_total_quantification"].sum()
                + Quantification_3_phase_sorted["Phase_5_total_quantification"].sum()
            )
            totalMass = mass_p1 + mass_p2 + mass_p3 + mass_p4 + mass_p5
            st.session_state["Phase A"] = round(mass_p1 * 100 / totalMass, 1)
            st.session_state["Phase B"] = round(mass_p2 * 100 / totalMass, 1)
            st.session_state["Phase C"] = round(mass_p3 * 100 / totalMass, 1)
            st.session_state["Phase D"] = round(mass_p4 * 100 / totalMass, 1)
            st.session_state["Phase E"] = round(mass_p5 * 100 / totalMass, 1)

    def quantifyAll():
        totalMass = (
            st.session_state["PhaseA_mass"]
            + st.session_state["PhaseB_mass"]
            + st.session_state["PhaseC_mass"]
            + st.session_state["PhaseD_mass"]
            + st.session_state["PhaseE_mass"]
        )
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

        Inner_volume_histograms = loadInVolume(Path_load_inner_histograms)
        Outer_volume_histograms = loadOutVolume(Path_load_outer_histograms)
        Surface_mesh_histogram = loadMesh(Path_load_surface_mesh_histograms)
        Gradient = loadGradient(Path_load_gradient)
        propertiesData = loadPropertiesWPeaks(dataDirectory)
        st.session_state["Particles2Phases"] = 0
        st.session_state["Particles3Phases"] = 0
        st.session_state["ParticlesAnalysed"] = 0
        st.session_state["ParticlesLiberated"] = 0
        st.session_state["VolumeAnalysed"] = 0
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
        totalParticleVolume = propertiesData["Volume"].sum()
        with tabQuantify:
            st.subheader("Mass percent of maximum 5 phases")
            col1Phase, col2Phase, col3Phase, col4Phase = st.columns(4)
            with col1Phase:
                st.header("1 phase", help="mineralogy of liberated particles")
                quantifyLiberatedParticles()
                plotMineralogy()
            with col2Phase:
                st.header(
                    "2 phases",
                    help="mineralogy of particles containing 1 or 2 phases (comulative)",
                )
                quantifyTwoPhasesParticle(
                    Inner_volume_histograms,
                    Outer_volume_histograms,
                    Surface_mesh_histogram,
                    Gradient,
                )
                plotMineralogy()
            with col3Phase:
                st.header(
                    "3 phases",
                    help="mineralogy of particles containing 1-3 phases (comulative)",
                )
                quantify3Phases_particle()
                plotMineralogy()
            with col4Phase:
                st.header("All particles", help="overal mineralogy")
                quantifyAll()
                plotMineralogy()
            with col1Phase:
                st.metric(
                    label="Number particles liberated",
                    value=st.session_state["ParticlesLiberated"],
                    help="particles with only one phase",
                )
            with col2Phase:
                st.metric(
                    label="Number particles with 2 phases",
                    value=st.session_state["Particles2Phases"],
                )
            with col3Phase:
                st.metric(
                    label="Number particles with more than 2 phases",
                    value=st.session_state["Particles3Phases"],
                    help="partial volume not corrected",
                )
            with col4Phase:
                st.metric(
                    label="Particles analysed",
                    value=st.session_state["ParticlesAnalysed"],
                    delta=numberParticles,
                    delta_color="inverse",
                    help="If number of particles analysed is very different from the number of particles segmented means something is wrong with the classification. Check the peaks and thresholds",
                )
                st.metric(
                    label="Volume analysed",
                    value=round(st.session_state["VolumeAnalysed"], 0),
                    delta=round(
                        st.session_state["VolumeAnalysed"] / totalParticleVolume, 2
                    ),
                    delta_color="inverse",
                    help=" compare volume fraction analysed = volume analysed / total volume",
                )


binInput = st.sidebar.number_input(
    "bins",
    value=256,
    max_value=initialBins,
    step=16,
    help="number to be divided by the initial number of bins. The higher the input the less number of bins plotted",
)
numberBins = int(initialBins / binInput)
savgolInput = st.sidebar.slider(
    "Savgol filter input", min_value=3, value=3, max_value=26
)
numbPartSubData = st.sidebar.number_input(
    "number particles in subset",
    value=3,
    min_value=3,
    max_value=maxParticleNumber,
    step=2,
)
buttRandomize = st.sidebar.button("Randomize")
particleNumberBox = st.sidebar.number_input(
    "Label particle X",
    step=1,
    help="specific particle. Does not need to be in the random dataset, but the label must exist in the full dataset",
)
buttRunPeaks = st.sidebar.button(
    label="Run Peaks",
    help="applies the peak parameters to all particles and apends the grey-values of the peaks to the properties file",
)
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
buttRunQuantify = st.sidebar.button(
    "Run Quantification", help="must be pressed for the new thresholds to take effect"
)

st.session_state["Peak_Width"] = sliderWidth
st.session_state["Peak_Height"] = sliderHeight
st.session_state["Peak_Prominence"] = Prominence
st.session_state["Peak_Horizontal_Distance"] = horizDistance
st.session_state["Peak_Vertical_Distance"] = vertDistance
st.session_state["Particle_X"] = particleNumberBox

if buttRandomize:  # Generates random subset of data
    subData1 = createSubdata1(numbPartSubData)
    subData1_binned = binning(binInput, subData1, n_jobs=-1)
    if savgolInput > 3:
        savgolSmooth = smooth_histograms_Savgol(
            subData1_binned, savgolInput, n_jobs=-1
        )  ############# Savgol filter applied if the slider input is >1
        normalizedSubData1 = normalizeVolume(savgolSmooth)
    else:
        normalizedSubData1 = normalizeVolume(subData1_binned)
    plotSubdata1 = transformColumnsXY(normalizedSubData1)
    st.session_state["plotSubData1"] = plotSubdata1
    #    if len(st.session_state['plotDataFromList'])<1:
    st.session_state["plotDataFromList"] = st.session_state["plotSubData1"]
    st.session_state["list6Particles"] = st.session_state["particleLabels"]

with tabHistOverview:
    colLoad, colSave, colA, colB, colC, colD, colE, colF = st.columns(8)
    with colLoad:
        buttLoadListLabels = st.button(
            "Load labels", help="Loads a list of labels created from the image viewer"
        )
    with colSave:
        buttSaveListLabels = st.button(
            "Save labels", help="Saves the label input on the"
        )
    lenghtOfList = len(st.session_state["particleLabels"])
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
    list6Particles = {
        "Label Index": [
            st.session_state["Particle_A"],
            st.session_state["Particle_B"],
            st.session_state["Particle_C"],
            st.session_state["Particle_D"],
            st.session_state["Particle_E"],
            st.session_state["Particle_F"],
        ]
    }
    st.session_state["list6Particles"] = pd.DataFrame(list6Particles)

if (
    buttLoadListLabels
):  # Loads list of particle labelsfrom CSV, Particles A to F created either from 'Histograms Overview' tab or from Napari
    subDataFromList = loadLabelList(dataDirectory)
    print("butt", subDataFromList)
    subDataFromList_binned = binning(binInput, subDataFromList, n_jobs=-1)
    if savgolInput > 3:
        savgolSmooth = smooth_histograms_Savgol(
            subDataFromList_binned, savgolInput, n_jobs=-1
        )  ############# Savgol filter applied if the slider input is >1
        normalizedSubDataFromList = normalizeVolume(savgolSmooth)
    else:
        normalizedSubDataFromList = normalizeVolume(subDataFromList_binned)
    plotDataFromList = transformColumnsXY(
        normalizedSubDataFromList
    )  # Creates a list of particles A-F
    st.session_state["plotDataFromList"] = plotDataFromList
    st.session_state["plotSubData1"] = st.session_state["plotDataFromList"]
    st.session_state["particleLabels"] = st.session_state["list6Particles"]

if buttSaveListLabels:
    saveLabelList()

PeaksDF = peaks(
    st.session_state["plotDataFromList"], st.session_state["list6Particles"]
)
PeaksDF = PeaksDF.reset_index(drop=True)
PeaksDF = PeaksDF.rename(
    columns={"X": "Particle", "Y": "GreyVal", "frequency": "PeakHeight"}
)

with tabHistOverview:
    plotHistogramOverview(st.session_state["plotSubData1"])
    with st.expander("binned data"):
        column8bit, columnLabels = st.columns(2)
        with columnLabels:
            st.dataframe(st.session_state["particleLabels"], hide_index=False)
        with column8bit:
            st.dataframe(st.session_state["data_8bit"], hide_index=True)

with tabHistogramProperty:
    colSavgolSl, column1, column2, column3, column4 = st.columns(5)
    # with colSavgolSl:
    #     savgolInput=st.slider('Savgol filter input',min_value=1, value=1,max_value=26)
    with column4:
        propertiesSize = st.selectbox(
            "Size property", propertiesData.columns[:].unique(), index=5
        )
    with column3:
        propertiesColor = st.selectbox(
            "Color property", propertiesData.columns[:].unique(), index=2
        )
    with column2:
        propertiesY = st.selectbox(
            "Y-property", propertiesData.columns[:].unique(), index=4
        )
    with column1:
        propertiesX = st.selectbox(
            "X-property", propertiesData.columns[:].unique(), index=1
        )
    plotProperties()
    with st.expander("Histograms Subset"):
        column8bit, columnLabels = st.columns(2)
        with columnLabels:
            st.dataframe(st.session_state["particleLabels"], hide_index=False)
        with column8bit:
            st.dataframe(st.session_state["data_8bit"], hide_index=True)
with tabFindPeaks:
    col1, col2 = st.columns(2)
    with col2:
        loadInputFiles = st.file_uploader(
            label="Load input densities and thresholds",
            help="if already saved for a known mineral list",
        )
    with col1:
        inclusionsBox = st.checkbox("inclusions")
    st.subheader("Input table of thresholds and densities")
    if loadInputFiles:
        inputsLoaded = pd.read_csv(loadInputFiles)
        inputs = st.data_editor(inputsLoaded)
        inputDensityA = int(inputs.iloc[0]["DensityA"])
        inputDensityB = int(inputs.iloc[0]["DensityB"])
        inputDensityC = int(inputs.iloc[0]["DensityC"])
        inputDensityD = int(inputs.iloc[0]["DensityD"])
        inputDensityE = int(inputs.iloc[0]["DensityE"])
        background_peak_pos = int(inputs.iloc[0]["BackgroundThreshold"])
        Phase_1_threshold = int(inputs.iloc[0]["ThresholdA"])
        Phase_2_threshold = int(inputs.iloc[0]["ThresholdB"])
        Phase_3_threshold = int(inputs.iloc[0]["ThresholdC"])
        Phase_4_threshold = int(inputs.iloc[0]["ThresholdD"])
        Phase_5_threshold = int(inputs.iloc[0]["ThresholdE"])
    else:
        input4Quantification = {
            "BackgroundThreshold": [600],
            "DensityA": [2.6],
            "ThresholdA": [6000],
            "DensityB": [3.2],
            "ThresholdB": [11111],
            "DensityC": [4.2],
            "ThresholdC": [22222],
            "DensityD": [5.1],
            "ThresholdD": [25555],
            "DensityE": [0],
            "ThresholdE": [65555],
        }
        input4Quantification = pd.DataFrame(input4Quantification)
        inputs = st.data_editor(input4Quantification)
        inputDensityA = int(inputs.iloc[0]["DensityA"])
        inputDensityB = int(inputs.iloc[0]["DensityB"])
        inputDensityC = int(inputs.iloc[0]["DensityC"])
        inputDensityD = int(inputs.iloc[0]["DensityD"])
        inputDensityE = int(inputs.iloc[0]["DensityE"])
        background_peak_pos = int(inputs.iloc[0]["BackgroundThreshold"])
        Phase_1_threshold = int(inputs.iloc[0]["ThresholdA"])
        Phase_2_threshold = int(inputs.iloc[0]["ThresholdB"])
        Phase_3_threshold = int(inputs.iloc[0]["ThresholdC"])
        Phase_4_threshold = int(inputs.iloc[0]["ThresholdD"])
        Phase_5_threshold = int(inputs.iloc[0]["ThresholdE"])
    Phase_0_threshold = background_peak_pos
if buttRunPeaks:
    allData_binned = binning(binInput, histogramsData)
    normalizedData = normalizeVolume(allData_binned)
    # applyPeaks(normalizedData)
    Peaks1 = process_peaks(normalizedData, histogramsData, propertiesData, numberBins)
    peaksArranged = Arrange_peaks(
        Peaks1,
        Phase_1_threshold,
        Phase_2_threshold,
        Phase_3_threshold,
        Phase_4_threshold,
        Phase_5_threshold,
        Phase_0_threshold,
        propertiesData,
    )

with tabAnalysePeaks:
    propertiesAndPeaks = pd.DataFrame(st.session_state["PropertiesAndPeaks"])
    column1, column2, column3 = st.columns(3)
    with column3:
        propertiesSize = st.selectbox(
            "Size property", propertiesAndPeaks.columns[:].unique(), index=1
        )
    with column2:
        properties = st.selectbox(
            "Property", propertiesAndPeaks.columns[:].unique(), index=1
        )
    with column1:
        buttAnalysePeaks = st.button(label="Plot Peaks")
    plotPeaksAndProperty()

    with st.expander("Properties And Peaks"):
        st.table(st.session_state["PropertiesAndPeaks"])

with tabFindPeaks:
    plotPeaksBalls()
    column4, column5 = st.columns(2)
    with column4:
        st.dataframe(PeaksDF)
    with column5:
        st.write(
            "Number of Peak1:", propertiesAndPeaks["Peak_1"].astype(bool).sum(axis=0)
        )
        st.write(
            "Number of Peak2:", propertiesAndPeaks["Peak_2"].astype(bool).sum(axis=0)
        )
        st.write(
            "Number of Peak3:", propertiesAndPeaks["Peak_3"].astype(bool).sum(axis=0)
        )
        st.write(
            "Number of Peak4:", propertiesAndPeaks["Peak_4"].astype(bool).sum(axis=0)
        )

if buttRunQuantify:
    quntifyMineralogy(dataDirectory)

################################## QUANTIFICATION ##################################
##Side note: in Shuvam's code the peaks are calculated from the average of the 5 larger peaks
# with tabQuantify:
#     st.download_button(label='Save parameters',data=inputs.to_csv(),file_name='thresholds and densities.csv')
#     st.metric(label="Particles analysed", value=st.session_state['ParticlesAnalysed'], delta=numberParticles,delta_color="inverse")
#     st.metric(label="Particles Liberated", value=st.session_state['ParticlesLiberated'], delta=numberParticles,delta_color="inverse")
#     st.metric(label="Volume analysed", value=st.session_state['VolumeAnalysed'], delta=totalVolume,delta_color="inverse")

# # Inclusions quantification ######### NOT READY #### function will not be called
# def quantifyInclusions():
#     array = (np.array(filtered_df.columns)).astype(int)
#     binning= 200   ###################  Input for inclusions only ????????????????????????????????????????????????????
#     file1 = []
#     file2 = []
#     k = 0
#     for index,row in filtered_df.iterrows():
#         if k > -1:
#             num = row.to_numpy()
#             num = np.pad(num, (0, 1), 'constant')
#             num = num.ravel()
#             rang = int(round(len(num)/binning))
#             bins = np.linspace(0,max(array)+1,rang)
#             full_range = np.linspace(0, max(array),len(array)+1)
#             digitized = np.digitize(full_range, bins)
#             bin_sum = [num[digitized == i].sum() for i in range(1, len(bins))]
#             bin_sum = np.array(bin_sum)
#             row1 = bin_sum[bin_sum>0]                 #list of non-zero entries in the histograms

#             bin_sum[bin_sum > 0] = row1
#             yhat = row1                                 #histogram of particle in new input bin format

#             bin_sum = [num[digitized == i].sum() for i in range(1, len(bins))]

#             bin_sum = np.array(bin_sum)
#             bin_sum[bin_sum > 0] = yhat
#             file1.append([bin_sum])                     #file1 creates the raw histogram after bining

#             yhat1 = row1
#             if (len(row1) < 11) and (len(row1) >4):                            #What is the meaning of these values??????????smoothening factors????????????????????????
#                 if (len(row1)) %2 == 0:
#                     yhat1 = savgol_filter(row1,len(row1)-1, 3)
#                 else:
#                     yhat1 = savgol_filter(row1,len(row1), 3)
#             elif (len(row1) <= 4):
#                 yhat1 = row1
#             else:
#                 yhat1 = savgol_filter(row1,11, 3)                                   # soothened histogram
#             bin_sum = [num[digitized == i].sum() for i in range(1, len(bins))]
#             bin_sum = np.array(bin_sum)
#             bin_sum[bin_sum > 0] = yhat1
#             file2.append([bin_sum])                            ####################file2 creates the smothened histogram
#         k = k+1

#     #####creates dataframe with particle indicies and file1 (not smoothened)
#     x = np.linspace(0,len(filtered_df.columns)-1, rang-1)
#     x = x.astype(int)
#     file = np.array(file1)
#     file = file.reshape(file.shape[0], (file.shape[1]*file.shape[2]))
#     file = pd.DataFrame(file, columns = x)
#     file.index = filtered_df.index
#     file[file < 0] = 0
#     #####creates dataframe with particle indicies and file2 (smoothened with savgol_filter)
#     file2 = np.array(file2)
#     file2 = file2.reshape(file2.shape[0], (file2.shape[1]*file2.shape[2]))
#     file2 = pd.DataFrame(file2, columns = x)
#     file2.index = filtered_df.index
#     file2[file2 < 0] = 0

#     #### Divide each row by its maximum value               I don't understand this bit???????????????????????????????????????????????????
#     df = file.div(file.max(axis=1), axis=0)
#     df1 = file2.div(file2.max(axis=1), axis=0)
#     noise = ((df1-df)**2).sum(axis=1)
#     noise = pd.DataFrame(noise,columns = ['noise'])
#     for index, row in noise.iterrows():
#         condition = row['noise'] > 0.11
#         if condition:
#             file.loc[index]= file2.loc[index]
#     ############################the rest needs to be integrated with the rest of the script.
#     # ############# To do next: Determine the associated phase - calculate the parcial volume as if 2 phase particle - recalculate mass percentage of that particle

# with tabInstructions:
#     st.write('- change the directory with the CSVs')
#     st.write('- input the densities')
#     st.write('- input thresholds for peaks')
#     st.write('- press "run" button')
#     st.write('Note: the plots are comulative from 1 to 3 phases per particle')
