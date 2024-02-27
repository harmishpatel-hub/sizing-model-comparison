from keras.models import load_model
from os import listdir
import streamlit as st
import xgboost as xgb

def read_model(PATH):
    file = listdir(PATH)[0]
    # st.write(file)
    model = load_model(f"{PATH}/{file}")
    return model

def read_xgboost_model(PATH):
    file = listdir(PATH)[0]
    # st.write(f"{PATH}{file}")
    model = xgb.Booster()
    model.load_model(f"{PATH}/{file}")
    return model


