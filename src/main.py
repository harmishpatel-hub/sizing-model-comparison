from src.modelTesting import modelTestingFilter
from src.physicsFilter import physics

import streamlit as st

def main():
    st.set_page_config(layout="wide")
    mainFilter = st.sidebar.selectbox("Choose the options:", options=["Physics Charts", "Model Testing"])
    if mainFilter == "Model Testing":
        modelTestingFilter()
    if mainFilter == "Physics Charts":
        physics()

