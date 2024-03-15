from matplotlib import category
import streamlit as st
import numpy as np
import pandas as pd
from plotly import graph_objects as go
import plotly.express as px
import plotly.io as pio
from src.component.downloadPDF import downloadPDF
from plotly.subplots import make_subplots

from src.dataset_preprocessing import preprocess_shape_depth, read_excel, preprocess_length_width, read_excel_with_filename

pio.templates.default = 'plotly'

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
        extIntSelection = st.sidebar.selectbox('Select External/Internal', options=data['Ext/Int'].unique())
        extIntFilteredData = data[data['Ext/Int']==extIntSelection]
        selectShape = st.sidebar.selectbox('Select Shape #', extIntFilteredData['Shape'].unique())
        shapeFilteredData = extIntFilteredData[extIntFilteredData['Shape']==selectShape]
        shapeFilteredData = shapeFilteredData.sort_values(by=['WT [in]', 'Actual Depth'])
        # st.dataframe(shapeFilteredData)
        chart, data = st.tabs(["📈 Chart", "💾 Data"])
        fig = go.Figure()
        for wt in shapeFilteredData['WT [in]'].unique():
            dataByWT = shapeFilteredData[shapeFilteredData['WT [in]']==wt]
            fig.add_trace(
                go.Scatter(
                    x=dataByWT['Actual Depth'],
                    y=abs(dataByWT['Peak Value']),
                    # legendtitle=f'WT [in]',
                    name=f'{wt}',
                    # hovertext=f'{dataByWT["Item #"]}',
                    mode='markers'
                )
            )

        fig.update_layout(
            xaxis=dict(type='category'), 
            xaxis_title = f"Actual Depth %",
            yaxis_title = f"Peak Value",
            height=800,
            width=1000
            )
        with chart:
            st.plotly_chart(fig)
        with data:
            st.dataframe(shapeFilteredData)
    #     wtSelection = st.sidebar.selectbox('Select WT [in]', options=data['WT [in]'].unique())
    #     wtFilteredData = data[data['WT [in]']==wtSelection]
    #     wtFilteredData = wtFilteredData.sort_values(by='Distance [ft]')
    #     extIntSelection = st.sidebar.selectbox('Select External/Internal', options=wtFilteredData['Ext/Int'].unique())
    #     extIntFilteredData = wtFilteredData[wtFilteredData['Ext/Int']==extIntSelection]
    #     extIntFilteredData = extIntFilteredData.sort_values(by='Distance [ft]')
    #     # st.write(extIntFilteredData.columns)
    # col1, col2 = st.columns([2,2])
    # tempFigures = {}
    # exportPDFforAllShape = {}
    # with col1:
    #     fig = make_subplots(specs=[[{"secondary_y": True}]])
    #     for pulltest in wtFilteredData['Pulltest #'].unique():
    #         dataByPulltest = wtFilteredData[wtFilteredData['Pulltest #'] == pulltest]
    #         st.dataframe(dataByPulltest)
    #         fig.add_trace(
    #             go.Scatter(
    #                 y=dataByPulltest['Speed [ft/s]'],
    #                 x=dataByPulltest['Distance [ft]'],
    #                 legendgroup=f'{pulltest}',
    #                 legendgrouptitle_text=f'Pulltest #{pulltest}',
    #                 name=f'{pulltest} Speed [ft/s]',
    #                 connectgaps=True),
    #                 secondary_y=False
    #             )
    #         # fig.add_trace(
    #         #     go.Scatter(
    #         #         x=dataByPulltest['Distance [ft]'],
    #         #         y=dataByPulltest['Background'],
    #         #         legendgroup=f'{pulltest}',
    #         #         name=f'{pulltest} Background',
    #         #         connectgaps=False),
    #         #         secondary_y=True
    #         #     )
    #     fig.update_xaxes(
    #         title_text="Distance [ft]"
    #     )
    #     fig.update_yaxes(title_text="Speed [ft/s]", secondary_y=False)
    #     fig.update_yaxes(title_text="Background", secondary_y=True)
    #     fig.update_layout(
    #         title_text='Speed [ft/s] & Background',
    #         height = 600,
    #         width = 1000,
    #         xaxis = dict(
    #             # tick0 = 0.05,
    #             dtick = 25,
    #         )
    #     )
    #     st.plotly_chart(fig)
    #     extIntFilteredData = extIntFilteredData.sort_values(by=['WT [in]', 'Shape'])


    #     # for shape in extIntFilteredData['Shape'].unique():
    #     #     shapeFilteredData = extIntFilteredData[extIntFilteredData['Shape']==shape]
    #     #     fig = go.Figure()
    #     #     fig.add_trace(
    #     #         go.Scatter(
    #     #             x=shapeFilteredData['Peak Value'],
    #     #             y=shapeFilteredData['Actual Depth'],
    #     #             mode='markers',
    #     #             name=f'Shape# {shape}',
    #     #             showlegend=True
    #     #         )
    #     #     )
    #     #     fig.update_layout(
    #     #         title=f'{pipe_size} | WT: {wtSelection} [in] | {extIntSelection} | Shape# {shape}',
    #     #         width=750,
    #     #         height=600,
    #     #         # xaxis=dict(
    #     #         #     dtick=25),
    #     #         yaxis=dict(
    #     #             side='right'),
    #     #         legend_orientation='h'
    #     #     )
    #     #     exportPDFforAllShape[shape]=fig
        
    #     # pdfOutput = downloadPDF(exportPDFforAllShape, subheader=f'{pipe_size} | {wtSelection} | {extIntSelection}')
    #     # st.download_button(label='EXPORT ALL SHAPE PDF',
    #     #                     data = pdfOutput.output('', dest='S').encode('latin-1'),
    #     #                     file_name = f'{pipe_size}_{wtSelection}_{extIntSelection}.pdf',
    #     #                     mime = 'application/octate_stream',
    #     #                     key = 'export all shape pdf')

    #     shapeSelection = st.sidebar.multiselect('Select Shape', options=np.sort(extIntFilteredData['Shape'].unique()))
    #     if shapeSelection:
    #         tempDF = pd.DataFrame()
    #         for shape in shapeSelection:
    #             shapeFilteredData = extIntFilteredData[extIntFilteredData['Shape']==shape]
    #             shapeFilteredData = shapeFilteredData.sort_values(by=['Actual Depth'])
    #             shapeFilteredData = shapeFilteredData[[ 'Item #', 'ML Class', 'Ext/Int', 
    #                                                 'Peak Value', 'Actual Depth', 'Shape', 
    #                                                 'Length [in]', 'Width [in]',
    #                                                 'Pulltest Date', 'Pulltest #']]
    #             tempDF = pd.concat([tempDF, shapeFilteredData])
    #             tempDF.reset_index(inplace=True)
    #             tempDF = tempDF[['Item #', 'ML Class', 'Ext/Int', 'Peak Value', 
    #                             'Actual Depth', 'Shape', 'Length [in]', 'Width [in]',
    #                             'Pulltest Date', 'Pulltest #']]
    #             tempDF = tempDF.sort_values(by='Actual Depth')

    #         with col1:
    #             chart, data = st.tabs(["📈 Chart", "💾 Data"])
    #             with chart:
                    
    #                 fig = go.Figure()
    #                 for shape in tempDF['Shape'].unique():
    #                     templFilteredDF = tempDF[tempDF['Shape']==shape]
    #                     fig.add_trace(
    #                         go.Scatter(
    #                             x=templFilteredDF['Peak Value'],
    #                             y=templFilteredDF['Actual Depth'],
    #                             mode='markers',
    #                             name=f"Shape# {templFilteredDF['Shape'].unique()}",
    #                             showlegend=True
    #                         )
    #                     )
    #                 fig.update_layout(
    #                     title=f'{pipe_size} | WT: {wtSelection} [in] | {extIntSelection} | Shape# {shapeSelection}',
    #                     xaxis_title=f'Peak Value',
    #                     yaxis_title=f'Actual Depth',
    #                     width=600,
    #                     height=500,
    #                     # xaxis=dict(
    #                     #     dtick=25),
    #                     yaxis=dict(
    #                         side='right'),
    #                     legend_orientation='h',
                        
    #                 )
    #                 tempFigures[shape] = fig
    #                 st.plotly_chart(fig)
                
    #             with data:
    #                 st.dataframe(tempDF.style.background_gradient(subset=['Actual Depth']), height = 25*len(shapeFilteredData), hide_index=True)

    #         pdfOutput = downloadPDF(report=tempFigures, subheader=f'{pipe_size} | {wtSelection} | {extIntSelection}')
    #         st.download_button(label='EXPORT PDF',
    #                             data = pdfOutput.output('', dest='S').encode('latin-1'),
    #                             file_name = f'{pipe_size}_{wtSelection}_{extIntSelection}.pdf',
    #                             mime = 'application/octate_stream',
    #                             key = 'pdf download')
            
