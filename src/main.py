from src.referencePeakValueRangeFilter import referencePeakValueRange
from src.backgroundVsWTFilter import backgroundVsWT
from src.backgroundComparisonFilter import backgroundComparison
from src.modelTesting import modelTestingFilter
from src.physicsFilter import physics

import streamlit as st
import os
import warnings

warnings.filterwarnings('ignore')

def main():
    st.set_page_config(layout="wide")
    PULLTEST_DATASET_OPTIONS = list(os.walk(f"./pulltest_dataset/"))[0][1] # provides the list of available pulltest data under the "pulltest_dataset"
    JOINTBKGLEVEL_OPTIONS = list(os.walk(f"./JointBkgLevel_dataset/"))[0][1] # provides the list of available pipe size data under "JointBkgLevel_dataset"
    ONNX_MODEL_OPTIONS = list(os.walk(f"./onnx_models/"))[0][1] # provides the list of available ONNX (Neural Network) models under the "onnx_model"
    XGBOOST_MODEL_OPTIONS = list(os.walk(f"./onnx_models/xgboost_model"))[0][1] # provides the list of available Xgboost model under "onnx_model/xgboost_model"
    
    ## Main filter to choose which type of service needed

    """_summary_
    Main Filter to choose which type of service needed

    Physics Charts: It will show the behaviour of the model/curves 
                    Length vs Width for WT, Peak, External/Internal
    
    Model Testing: Testing a models (i.e. Neural Network, and XGBoost)
                   Two options provide:
                        Actual Dimensions: Length and Width will be replaced in pulltest\
                                           data and then predict the depths using both models.
                        ILI Predicted Dimensions: Length and Width will be the same as we export the \
                                            excel listing of pulltest dataa and then predicting the \
                                            depths using both models.
    
    Background vs WT [in]: Background level comparison vs Wall Thickness [in], the purpose is to \
                            prove the different tools for same IDOD has the same background level for thin, \
                            standard, and thick walls. 
                            If not same and significant differnece then proceed to create a different curves,\
                            for the tools. 
    """
    mainFilter = st.sidebar.selectbox("Choose the Option:", 
                                      options=[
                                          "Physics Charts", 
                                          "Model Testing", 
                                          "Reference Peak Value Range (Pulltests)",
                                        #   "Background Comparisons",
                                          "Background vs WT [in]"])
    
    if mainFilter == "Model Testing":
        modelTestingFilter(PULLTEST_DATASET_OPTIONS, ONNX_MODEL_OPTIONS, XGBOOST_MODEL_OPTIONS)
    if mainFilter == "Physics Charts":
        physics(ONNX_MODEL_OPTIONS, XGBOOST_MODEL_OPTIONS)
    if mainFilter == "Reference Peak Value Range (Pulltests)":
        referencePeakValueRange(PULLTEST_DATASET_OPTIONS)
    if mainFilter == "Background vs WT [in]":
        backgroundVsWT(JOINTBKGLEVEL_OPTIONS)
    # if mainFilter == "Background Comparisons":
    #     backgroundComparison(PULLTEST_DATASET_OPTIONS)


