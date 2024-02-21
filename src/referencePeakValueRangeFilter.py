import streamlit as st
import numpy as np
from plotly import graph_objects as go
from src.dataset_preprocessing import preprocess_shape_depth, read_excel, preprocess_length_width


def referencePeakValueRange(PULLTEST_DATASET_OPTIONS):
    pipe_size = st.sidebar.selectbox("Select Pipe Size[in]:", options=PULLTEST_DATASET_OPTIONS)

    if pipe_size:
        READ_EXCEL_FILES = f"./pulltest_dataset/{pipe_size}/"
        df = read_excel(READ_EXCEL_FILES)
        # st.dataframe(df)
        data = preprocess_shape_depth(df)
        data = preprocess_length_width(data)
        st.subheader(f'{pipe_size} Pulltest Data')
        st.dataframe(data)

    # particularShape = st.checkbox("Particular Type of Defect?")
    # if particularShape:
    wtSelection = st.selectbox('Choose WT [in]', options=data['WT [in]'].unique())
    wtFilteredData = data[data['WT [in]']==wtSelection]
    extIntSelection = st.selectbox('Choose External/Internal', options=wtFilteredData['Ext/Int'].unique())
    extIntFilteredData = wtFilteredData[wtFilteredData['Ext/Int']==extIntSelection]
    shapeSelection = st.selectbox('Select Shape', options=np.sort(extIntFilteredData['Shape'].unique()))
    shapeFilteredData = extIntFilteredData[extIntFilteredData['Shape']==shapeSelection]
    shapeFilteredData = shapeFilteredData.sort_values(by=['Actual Depth']).reset_index()
    shapeFilteredData = shapeFilteredData[[ 'Item #',
                                            'ML Class', 
                                            'Ext/Int', 
                                            'Peak Value', 
                                            'Actual Depth',
                                            'Length [in]',
                                            'Width [in]']]

    chart, data = st.tabs(["📈 Chart", "💾 Data"])
    with chart:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=shapeFilteredData['Peak Value'],
                y=shapeFilteredData['Actual Depth'],
                mode='markers'
            )
        )
        fig.update_layout(
            title=f'{pipe_size} | WT: {wtSelection} [in] | {extIntSelection} | Shape# {shapeSelection}',
            width=800,
            height=600,
            xaxis=dict(
                dtick=50
            ),
            yaxis=dict(
                side='right'
            )
        )
        st.plotly_chart(fig)

    with data:
        # st.dataframe(shapeFilteredData)
        st.dataframe(shapeFilteredData.style.background_gradient(subset=['Actual Depth']), height = 25*len(shapeFilteredData), hide_index=True)
    # df_test.style.background_gradient(subset=['Actual Depth']), height=100*len(df_test)
    
