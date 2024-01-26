from keras.models import load_model
from os import listdir
import streamlit as st

def read_model(PATH):
    file = listdir(PATH)[0]
    # st.write(file)
    model = load_model(f"{PATH}{file}")
    return model

