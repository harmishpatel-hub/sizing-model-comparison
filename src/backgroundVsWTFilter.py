import numpy as np
from sklearn.calibration import LabelEncoder
import streamlit as st

from src.dataset_preprocessing import read_csvs
from plotly import graph_objects as go
import plotly.express as px

def extractToolUsed(string):
    return string.split(' ')[0]

def extractYear(string):
    string = string.split(" ")[1]
    string = string.split("-")[0]
    return string

def backgroundVsWT(JOINTBKGLEVEL_OPTIONS):
    pipe_size = st.sidebar.selectbox('Select Pipe Size[in]:',
                                     options=JOINTBKGLEVEL_OPTIONS)
    if pipe_size:
        tab1, tab2 = st.tabs(["📈 Chart", "💾 Data"])
        READ_CSV_FILES = f'./JointBkgLevel_dataset/{pipe_size}/'
        df = read_csvs(READ_CSV_FILES)
        df['Tool Used'] = df['Info'].apply(lambda x: extractToolUsed(x))
        le = LabelEncoder()
        df['Tool Used COLOR'] = le.fit_transform(df['Tool Used'])
        df['Year'] = df['Info'].apply(lambda x: extractYear(x))
        
        dataframeMedian = df.groupby(by=['Tool Used', 'WT[in]'], as_index=False)['BkgLevel[counts]'].apply(lambda x: sorted(x))
        tab2.dataframe(dataframeMedian)
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
        tab2.dataframe(dataframeMedianBkgLevel)

        tab1.plotly_chart(fig)

        fig = go.Figure()
        for toolUsed in df['Tool Used'].unique():
            fig.add_trace(
                go.Scatter(
                    x=df[df['Tool Used']==toolUsed]['WT[in]'],
                    y=df[df['Tool Used']==toolUsed]['BkgLevel[counts]'],
                    mode='markers',
                    showlegend=True,
                    name=toolUsed
                )
            )
        fig.update_layout(
            title = f'{pipe_size} WT [in] vs Background [Counts]',
            width = 1000,
            height = 800,
            xaxis_title = f'WT [in]',
            yaxis_title = f'Background [Counts]'
        )
        # tab1.plotly_chart(fig)
    return None