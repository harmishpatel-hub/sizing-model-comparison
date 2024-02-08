import streamlit as st
from src.charts.update_traces import update_traces

from src.dataset_preprocessing import parsed_data, preprocess_length_width, preprocess_shape_depth, read_excel
from plotly import graph_objects as go

def backgroundComparison(PULLTEST_DATASET_OPTIONS):
    pipe_size = st.sidebar.selectbox('Select Pipe Size[in]:', options=PULLTEST_DATASET_OPTIONS)
    if pipe_size:
        READ_EXCEL_FILES = f'./pulltest_dataset/{pipe_size}/'
        df = read_excel(READ_EXCEL_FILES)
        data = preprocess_shape_depth(df)
        tab_labels = data['WT [in]'].unique().tolist()
        tab_labels_string = [str(element) for element in tab_labels]
        tabs = st.tabs(tab_labels_string)
        for label, tab in zip(tab_labels, tabs):
            with tab:
                dataframe = data[data['WT [in]']==label]
                externalOrInternalTab = ['External', 'Internal']
                innerTabs = tab.tabs(externalOrInternalTab)
                for labelExternalOrInternal, innerTab in zip(externalOrInternalTab, innerTabs):
                    with innerTab:
                        externalFilteredDataframe = dataframe[dataframe['Ext/Int'] == labelExternalOrInternal]
                        # innerTabs[0].dataframe(externalFilteredDataframe)
                        selectedDefect = innerTab.selectbox('Select a Defect:', options=externalFilteredDataframe['Shape'].unique().tolist(), key=f'{innerTab}')
                        defectFilteredDataframe = externalFilteredDataframe[externalFilteredDataframe['Shape'] == selectedDefect].sort_values('Actual Depth')
                        col1, col2 = st.columns(2)
                        with col1:
                            fig = go.Figure()
                            fig.add_trace(
                                go.Scatter(
                                    x=defectFilteredDataframe['Actual Depth'],
                                    y=defectFilteredDataframe['Background'],
                                    mode='markers',
                                    name='Background'
                                )
                            )
                            fig.add_trace(
                                go.Scatter(
                                    x=defectFilteredDataframe['Actual Depth'],
                                    y=defectFilteredDataframe['Peak Value'],
                                    mode='markers',
                                    name='Peak Value'
                                )
                            )
                            fig.update_layout(
                                title = f'<b>Background & Peak Value vs Actual Depth<b>',
                                width = 800,
                                height = 600,
                                xaxis_title = f'Actual Depth',
                                yaxis_title = f'Background & Peak Value',
                            )
                            # fig = update_traces(fig, start=-1000, end=0,
                            #                     string=f"Background and Peak vs Actual Depth",
                            #                     col1=f"Actual Depth [%]",
                            #                     col2=f"Background and Peak Value",
                            #                     tick=100,
                            #                     plotWidth=1000, plotHeight=800)
                            st.plotly_chart(fig)
                        with col2:
                            st.dataframe(defectFilteredDataframe[['WT [in]', 
                                                                  'Ext/Int', 
                                                                  'Shape', 
                                                                  'Peak Value', 
                                                                  'Background', 
                                                                  'Actual Depth']].style
                                                                  .background_gradient(
                                                                      subset='Actual Depth'), 
                                                                      hide_index=True)
    
    return None

