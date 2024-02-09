from src.backgroundVsWTFilter import backgroundVsWT
from src.backgroundComparisonFilter import backgroundComparison
from src.modelTesting import modelTestingFilter
from src.physicsFilter import physics

import streamlit as st
import os

def main():
    st.set_page_config(layout="wide")
    PULLTEST_DATASET_OPTIONS = list(os.walk(f"./pulltest_dataset/"))[0][1]
    JOINTBKGLEVEL_OPTIONS = list(os.walk(f"./JointBkgLevel_dataset/"))[0][1]
    ONNX_MODEL_OPTIONS = list(os.walk(f"./onnx_models/"))[0][1]
    XGBOOST_MODEL_OPTIONS = list(os.walk(f"./onnx_models/xgboost_model"))[0][1]
    mainFilter = st.sidebar.selectbox("Choose the Option:", 
                                      options=[
                                          "Physics Charts", 
                                          "Model Testing", 
                                          "Background Comparisons",
                                          "Background vs WT [in]"])
    if mainFilter == "Model Testing":
        modelTestingFilter(PULLTEST_DATASET_OPTIONS, ONNX_MODEL_OPTIONS, XGBOOST_MODEL_OPTIONS)
    if mainFilter == "Physics Charts":
        physics(ONNX_MODEL_OPTIONS)
    if mainFilter == "Background vs WT [in]":
        backgroundVsWT(JOINTBKGLEVEL_OPTIONS)
    if mainFilter == "Background Comparisons":
        backgroundComparison(PULLTEST_DATASET_OPTIONS)


