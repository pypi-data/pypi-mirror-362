# importing all the required packages
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Step 7 Overview with properties")
tabHistOverview, tabHistogramProperty = st.tabs(
    ["Histogram Overview", "Histograms + Properties"]
)


@st.cache_data(experimental_allow_widgets=True)
def loadHistograms():
    uploadHistoBut = st.sidebar.file_uploader("Upload Histograms", type="csv")
    histogramsRawData = pd.read_csv(uploadHistoBut, encoding="unicode_escape")
    histogramsRawData.index = histogramsRawData.iloc[:, 0]
    histogramsRawData = histogramsRawData.iloc[:, 2:]
    return histogramsRawData


@st.cache_data(experimental_allow_widgets=True)
def loadProperties():
    uploadPropertyBut = st.sidebar.file_uploader("Upload Properties", type="csv")
    propertiesData = pd.read_csv(uploadPropertyBut, encoding="unicode_escape")
    return propertiesData


histogramsData = loadHistograms()
propertiesData = loadProperties()
maxParticleNumber = len(histogramsData)

if "particleLabels" not in st.session_state:
    st.session_state["particleLabels"] = []
if "data_8bit" not in st.session_state:
    st.session_state["data_8bit"] = []
if "plotDataframe" not in st.session_state:
    st.session_state["plotDataframe"] = []
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


@st.cache_data
def histogramsOverview(plotData):
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


binInput = st.sidebar.number_input("bins", value=256, max_value=65535, step=2)


def createSubdata1(n):
    labels_array = np.array(histogramsData.index)
    labels_array = labels_array[labels_array > 0]
    random_labels = np.random.choice(labels_array, n, replace=False)
    random_labels = np.sort(random_labels)
    random_labels = pd.DataFrame(random_labels)
    random_labels = random_labels.rename(
        columns={random_labels.columns[0]: "Label Index"}
    )
    subData1 = random_labels.merge(
        histogramsData, left_on="Label Index", right_on=histogramsData.index, how="left"
    )
    subData1.index = subData1["Label Index"]
    subData1 = subData1.iloc[:, 1:]

    st.session_state["particleLabels"] = random_labels
    return random_labels, subData1


def binningFrom16bit(binInput, bit16):
    bit16toOther = pd.DataFrame(bit16)
    binning = int(65535 / binInput)
    file1 = []
    Index_particle_labels = []
    k = 0
    for index, row in bit16toOther.iterrows():
        if k > -1:
            num = row.to_numpy()
            num = num.ravel()
            rang = int(round(len(num) / binning))
            bins = np.linspace(0, 65535, rang)
            full_range = np.linspace(0, 65534, 65535)
            digitized = np.digitize(full_range, bins)
            bin_sum = [num[digitized == i].sum() for i in range(1, len(bins))]
            file1.append([bin_sum])
            Index_particle_labels.append([index])
        k = k + 1
    x = np.linspace(0, len(bit16toOther.columns) - 1, rang - 1)
    x = x.astype(int)
    file1 = np.array(file1)
    file1 = file1.reshape(file1.shape[0], (file1.shape[1] * file1.shape[2]))
    file1 = pd.DataFrame(file1)
    Index_particle_labels = pd.DataFrame(Index_particle_labels)
    file1.index = Index_particle_labels.iloc[:, 0]
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
            index_array = (normalizedSubData1_8bit.index)[i]
            element = array[i][j]
            row.append([index_array, j, element])
    DataFrame = pd.DataFrame(row, dtype="float32")
    DataFrame.columns = ["X", "Y", "frequency"]
    pd.set_option("display.float_format", "{:.10f}".format)
    DataFrame["X"] = DataFrame["X"].astype(int)
    DataFrame["Y"] = DataFrame["Y"].astype(int)
    st.session_state["plotDataframe"] = DataFrame


def plotHistogramProperty():
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
        alt.Chart(st.session_state["plotDataframe"], height=1000)
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


numbPartSubData = st.sidebar.number_input(
    "number particles in subset", value=2, max_value=maxParticleNumber, step=1
)
buttNewSubdata = st.sidebar.button("Randomize")
checkboxBin = st.sidebar.checkbox("rebin")
if buttNewSubdata:
    particleLabels, subData1 = createSubdata1(numbPartSubData)
    if checkboxBin:
        subData1_binned = binningFrom16bit(binInput, subData1)
    else:
        subData1_binned = subData1
    normalizedSubData1_8bit = normalizeVolume(subData1_binned)
    transformColumnsXY(normalizedSubData1_8bit)

particleNumberBox = st.sidebar.number_input("Particle Number", step=1)
st.session_state["Particle_X"] = particleNumberBox
dropdown1 = st.sidebar.selectbox(
    label="Particle_A", options=st.session_state["particleLabels"]
)
st.session_state["Particle_A"] = dropdown1
dropdown2 = st.sidebar.selectbox(
    label="Particle_B", options=st.session_state["particleLabels"]
)
st.session_state["Particle_B"] = dropdown2
dropdown3 = st.sidebar.selectbox(
    label="Particle_C", options=st.session_state["particleLabels"]
)
st.session_state["Particle_C"] = dropdown3
dropdown4 = st.sidebar.selectbox(
    label="Particle_D", options=st.session_state["particleLabels"]
)
st.session_state["Particle_D"] = dropdown4
dropdown5 = st.sidebar.selectbox(
    label="Particle_E", options=st.session_state["particleLabels"]
)
st.session_state["Particle_E"] = dropdown5
dropdown6 = st.sidebar.selectbox(
    label="Particle_F", options=st.session_state["particleLabels"]
)
st.session_state["Particle_F"] = dropdown6

with tabHistOverview:
    histogramsOverview(st.session_state["plotDataframe"])
    with st.expander("binned data"):
        column8bit, columnLabels = st.columns(2)
        with columnLabels:
            st.dataframe(st.session_state["particleLabels"], hide_index=False)
        with column8bit:
            st.dataframe(st.session_state["data_8bit"], hide_index=True)

with tabHistogramProperty:
    column1, column2, column3, column4 = st.columns(4)
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
    plotHistogramProperty()
    with st.expander("Histograms Subset"):
        column8bit, columnLabels = st.columns(2)
        with columnLabels:
            st.dataframe(st.session_state["particleLabels"], hide_index=False)
        with column8bit:
            st.dataframe(st.session_state["data_8bit"], hide_index=True)
