from src.charts.draw_tolerance_lines import draw_tolerance_lines
from src.charts.update_traces import update_traces
import streamlit as st
from src.dataset_preprocessing import read_excel
from src.dataset_preprocessing import filter_columns
from src.dataset_preprocessing import preprocess_shape_depth
from src.read_model import read_model
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go

from src.charts.draw_unity import draw_unity


def depth_range(x):
    if x < 10:
        return 10
    elif x > 80:
        return 80
    else:
        return round(x)

def main():
    pipe_size = st.sidebar.selectbox("Select Pipe Size[in]:", options=[16,24])

    if pipe_size:
        READ_EXCEL_FILES = f"./pulltest_dataset/{pipe_size}in/"
        df = read_excel(READ_EXCEL_FILES)
        # st.dataframe(df)
        data = preprocess_shape_depth(df)
        st.dataframe(data)
        columns = ['ML Class', 'Ext/Int', 'Length [in]', 'Width [in]', 'WT [in]', 'Peak Value', 'Speed [ft/s]', '% Depth']
        filtered_df = filter_columns(data, columns)
        df_test = filtered_df.rename(
            columns={
                'ML Class': 'ml_class', 
                'Length [in]': 'length', 
                'Width [in]': 'width', 
                'WT [in]': 'wt', 
                'Peak Value': 'peak_value',
                'Speed [ft/s]': 'speed',
                '% Depth': 'depth_old'
                }
            )
        old_depth = df_test['depth_old']
        df_test.drop('depth_old', axis=1, inplace=True)
        df_test['Ext/Int'] = df_test['Ext/Int'].apply(lambda x: 1 if x=='External' else 0)
        le = LabelEncoder()
        df_test['ml_class'] = le.fit_transform(df_test['ml_class'])
        # st.dataframe(df_test)
        # st.dataframe(filtered_df)

    select_model = st.sidebar.selectbox("Select Model:", options=['16in', '24in'])
    if select_model:
        READ_MODEL_FILE = f"./onnx_models/{select_model}/"
        nn_model = read_model(READ_MODEL_FILE)

        nn_depth = nn_model.predict(df_test)
        df_test['Shape'] = data['Shape']
        df_test['Actual Depth'] = data['Actual Depth']
        df_test['NN_Depth'] = nn_depth
        df_test['NN_Depth'] = df_test['NN_Depth'].apply(lambda x: depth_range(x))
        st.dataframe(df_test)
    
    unity_plot = st.checkbox("Show Unity Plots:")
    if unity_plot:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x = data['Actual Depth'],
                y = df_test['NN_Depth'],
                mode = 'markers',
                showlegend = False
        ))
        fig = draw_unity(fig, 0, 90)
        fig = draw_tolerance_lines(fig, 0, 90, 10, unit="%")
        fig = update_traces(fig, 0, 90, "", "Actual Depth (%)", "NN_Depth", 10)
        st.plotly_chart(fig)

    



