import streamlit as st
import numpy as np
import pandas as pd
from plotly import graph_objects as go

from src.dataset_preprocessing import preprocess_shape_depth, read_excel, preprocess_length_width, read_excel_with_filename


def referencePeakValueRange(PULLTEST_DATASET_OPTIONS):
    """
    The function will give us an options to select the wt, external or internal, multiple shapes
    based on the selected pulltests and will reflect uplon charts and data.

    charts will have peak value (xaxis) and actual depth (yaxis)


    Args:
        PULLTEST_DATASET_OPTIONS (list): list of the pulltest data available in /pulltest_dataset/ directory
    """
    pipe_size = st.sidebar.selectbox("Select Pipe Size[in]:", options=PULLTEST_DATASET_OPTIONS)

    if pipe_size:
        READ_EXCEL_FILES = f"./pulltest_dataset/{pipe_size}/"
        df = read_excel_with_filename(READ_EXCEL_FILES)
        
        data = preprocess_shape_depth(df)
        data = preprocess_length_width(data)
        st.subheader(f'{pipe_size} Pulltest Data')
        # st.dataframe(data)
    col1, col2 = st.columns([1,3])
   
    with col1:
        wtSelection = st.selectbox('Select WT [in]', options=data['WT [in]'].unique())
        wtFilteredData = data[data['WT [in]']==wtSelection]
        extIntSelection = st.selectbox('Select External/Internal', options=wtFilteredData['Ext/Int'].unique())
        extIntFilteredData = wtFilteredData[wtFilteredData['Ext/Int']==extIntSelection]

        shapeSelection = st.multiselect('Select Shape', options=np.sort(extIntFilteredData['Shape'].unique()))
        if shapeSelection:
            tempDF = pd.DataFrame()
            for shape in shapeSelection:
                shapeFilteredData = extIntFilteredData[extIntFilteredData['Shape']==shape]
                shapeFilteredData = shapeFilteredData.sort_values(by=['Actual Depth'])
                shapeFilteredData = shapeFilteredData[[ 'Item #', 'ML Class', 'Ext/Int', 
                                                    'Peak Value', 'Actual Depth', 'Shape', 
                                                    'Length [in]', 'Width [in]',
                                                    'Pulltest Date', 'Pulltest #']]
                tempDF = pd.concat([tempDF, shapeFilteredData])
                tempDF.reset_index(inplace=True)
                tempDF = tempDF[['Item #', 'ML Class', 'Ext/Int', 'Peak Value', 
                                'Actual Depth', 'Shape', 'Length [in]', 'Width [in]',
                                'Pulltest Date', 'Pulltest #']]
                tempDF = tempDF.sort_values(by='Actual Depth')

            with col2:
                chart, data = st.tabs(["📈 Chart", "💾 Data"])
                with chart:
                    fig = go.Figure()
                    for shape in tempDF['Shape'].unique():
                        templFilteredDF = tempDF[tempDF['Shape']==shape]
                        fig.add_trace(
                            go.Scatter(
                                x=templFilteredDF['Peak Value'],
                                y=templFilteredDF['Actual Depth'],
                                mode='markers',
                                name=f"{templFilteredDF['Shape'].unique()}",
                                showlegend=True
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
                
                    st.dataframe(tempDF.style.background_gradient(subset=['Actual Depth']), height = 25*len(shapeFilteredData), hide_index=True)
            
