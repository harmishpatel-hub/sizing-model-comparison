import streamlit as st
from src.charts.draw_scatter import drawPhysicsChart
from src.datasetCreation.createDataframe import createListfromRange
from src.dataset_postprocessing import depth_range
from src.datasetCreation.createDataframe import create_df

from src.read_model import read_model, read_xgboost_model
import pandas as pd

def physics():
    select_model = st.sidebar.selectbox("Select Neural Network Model:", options=['3in', '16in', '24in'])
    if select_model:
        READ_NEURAL_NETWORK_MODEL = f"./onnx_models/{select_model}"
        nnModel = read_model(READ_NEURAL_NETWORK_MODEL)
    
    # select_xgboost_model = st.sidebar.selectbox("Select XGBoost Model:", options=['3in', '16in', '24in'])
    # if select_xgboost_model:
    #     READ_XGBOOST_MODEL_FILE = f"./onnx_models/xgboost_model/{select_xgboost_model}"
    #     xgboost_model = read_xgboost_model(READ_XGBOOST_MODEL_FILE)
    col1, col2 = st.columns([1, 3])
    with col1:
        wt = st.selectbox("Select Wall Thickness (in):", 
                        options = createListfromRange(
                            startingElement=0.10, 
                            lastElement=1.05, 
                            steps=0.025, 
                            decimal=3)
                            )
        external_internal = st.selectbox("Select External or Internal :", 
                                        options = ['External', 'Internal'])

        lengths = st.multiselect("Select Length (in):", 
                            options = createListfromRange(
                                startingElement=0.10, 
                                lastElement=3.05, 
                                steps=0.05, 
                                decimal=3),
                                default=0.5
                                )
        peak_value = st.selectbox("Select Peak Value:", 
                                options = createListfromRange(
                                    startingElement=0, 
                                    lastElement=-4000, 
                                    steps=-25, 
                                    decimal=0),
                                    )
        width = createListfromRange(
                    startingElement=0.10, 
                    lastElement=3.05, 
                    steps=0.05, 
                    decimal=3)
        
        if len(lengths) == 0:
            st.warning("Please Select Length [in]:")
        elif len(lengths) == 1:
            dimensionDF = create_df(lengths[0], width, peak_value, wt, external_internal)
        else:
            dimensionDF = pd.DataFrame()
            for length in lengths:
                dimensionDF = pd.concat([dimensionDF,
                                create_df(
                                    length=length, 
                                    widthList=width, 
                                    peakValue=peak_value,
                                    wallThickness=wt,
                                    externalOrinternal=external_internal
                                    )],
                                    ignore_index=True
                                )
    with col2:
        nnPredictions = nnModel.predict(dimensionDF)
        dimensionDF['NN Depth'] = nnPredictions
        dimensionDF['NN Depth'] = dimensionDF['NN Depth'].apply(lambda x: depth_range(x))
        tab1, tab2 = st.tabs(["📈 Chart", "💾 Data"])
        fig = drawPhysicsChart(dimensionDF, colX='width', colY='NN Depth', colColor='length', tick = 5)
        fig.update_xaxes(range=[0.05, 3.05], showticklabels=True)
        fig.update_yaxes(range=[5, 85], showticklabels=True)
        tab1.plotly_chart(fig)
        tab2.write(dimensionDF)