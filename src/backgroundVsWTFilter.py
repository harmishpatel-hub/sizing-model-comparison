import numpy as np
from sklearn.calibration import LabelEncoder
import streamlit as st

from src.dataset_preprocessing import read_csvs
from plotly import graph_objects as go
import plotly.express as px

def extractToolUsed(string):
    """To extract the tool used from dataframe

    Args:
        string: filename stored in dataframe column

    Returns:
        string: tool used in a pulltest
    """
    return string.split(' ')[0]

def extractYear(string):
    """to extract a year from dataframe

    Args:
        string: filename

    Returns:
        string: year
    """
    string = string.split(" ")[1]
    string = string.split("-")[0]
    return string

def backgroundVsWT(JOINTBKGLEVEL_OPTIONS):
    """Initially filters will be provided to choose the pipe size and based on
    selection it will provide a chart and dataframe indicating the different 
    background level for each wall thickness in each tool used.

    Args:
        JOINTBKGLEVEL_OPTIONS (list): the file list from JointBkgLevel_dataset path

    Returns:
        None:
    """
    pipe_size = st.sidebar.selectbox('Select Pipe Size[in]:',
                                     options=JOINTBKGLEVEL_OPTIONS)
    if pipe_size:
        tab1, tab2, tab3 = st.tabs(["📈 Chart", "📈 Median Chart", "💾 Data"])
        READ_CSV_FILES = f'./JointBkgLevel_dataset/{pipe_size}/'
        df = read_csvs(READ_CSV_FILES)
        df['Tool Used'] = df['Info'].apply(lambda x: extractToolUsed(x))
        le = LabelEncoder()
        df['Tool Used COLOR'] = le.fit_transform(df['Tool Used'])
        df['Year'] = df['Info'].apply(lambda x: extractYear(x))
        df = df.sort_values(by='WT[in]') # sort by wall thcikness
        
        dataframeGroupedbyToolUsedandWT = df.groupby(by=['Tool Used', 'WT[in]'], as_index=False)['BkgLevel[counts]'].apply(lambda x: ', '.join(str(i) for i in sorted(x)))
        tab3.dataframe(dataframeGroupedbyToolUsedandWT)
        dataframeMedianBkgLevel = df.groupby(by=['Tool Used', 'WT[in]'], as_index=False)['BkgLevel[counts]'].median()

        fig = px.scatter(dataframeMedianBkgLevel,
                         x='WT[in]',
                         y='BkgLevel[counts]',
                         color='Tool Used',
                         symbol='Tool Used',
                         hover_data=['Tool Used', 'WT[in]', 'BkgLevel[counts]'])
        fig.update_traces(
            marker_size=10,
        )
        fig.update_xaxes(type='category')
        fig.update_layout(
            title = f'{pipe_size} WT[in] vs BkgLevel[counts] (Median Values) per Tool',
            width = 1000,
            height = 800,
            xaxis = dict(
                # tick0 = 0.05,
                dtick = 0.05,
            ),
            yaxis = dict(
                # tick0 = 100,
                dtick = 50
            )
        )
        tab3.dataframe(dataframeMedianBkgLevel)

        tab2.plotly_chart(fig)

        fig = px.scatter(df,
                         x='WT[in]',
                         y='BkgLevel[counts]',
                         color='Tool Used',
                         symbol='Tool Used',
                         hover_data=['Tool Used', 'WT[in]', 'BkgLevel[counts]'])
        fig.update_traces(
            marker_size=6,
        )
        fig.update_xaxes(type='category')
        fig.update_layout(
            title = f'{pipe_size} WT[in] vs BkgLevel[counts] per Tool',
            width = 1000,
            height = 800,
            xaxis = dict(
                # tick0 = 0.05,
                dtick = 0.05,
            ),
            yaxis = dict(
                # tick0 = 100,
                dtick = 50
            )
        )
        tab1.plotly_chart(fig)
    return None