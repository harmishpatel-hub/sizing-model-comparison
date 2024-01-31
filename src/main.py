from src.score.model_score import model_score
from src.charts.draw_tolerance_lines import draw_tolerance_lines
from src.charts.update_traces import update_traces
from src.dataset_preprocessing import parsed_data, read_excel
from src.dataset_preprocessing import preprocess_shape_depth
from src.dataset_preprocessing import preprocess_length_width
from src.read_model import read_model, read_xgboost_model
from src.charts.draw_unity import draw_unity
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import xgboost as xgb



st.set_page_config(layout="wide")

def depth_range(x):
    if x < 10:
        return 10
    elif x > 80:
        return 80
    else:
        return round(x)

def main():
    pipe_size = st.sidebar.selectbox("Select Pipe Size[in]:", options=[3,16,24])

    if pipe_size:
        READ_EXCEL_FILES = f"./pulltest_dataset/{pipe_size}in/"
        df = read_excel(READ_EXCEL_FILES)
        # st.dataframe(df)
        data = preprocess_shape_depth(df)
        # st.dataframe(data)
        

    select_model = st.sidebar.selectbox("Select Neural Network Model:", options=['3in', '16in', '24in'])
    if select_model:
        READ_MODEL_FILE = f"./onnx_models/{select_model}/"
        nn_model = read_model(READ_MODEL_FILE)
    
    select_xgboost_model = st.sidebar.selectbox("Select XGBoost Model:", options=['3in', '16in', '24in'])
    if select_xgboost_model:
        READ_XGBOOST_MODEL_FILE = f"./onnx_models/xgboost_model/{select_xgboost_model}/"
        xgboost_model = read_xgboost_model(READ_XGBOOST_MODEL_FILE)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Predicted Depth Data - (on ILI Dimensions)")
        predict_depths = st.checkbox("Predict the Depths (Using Neural Network Model):")
        if predict_depths:
            df_test = parsed_data(data)
            nn_depth = xgboost_model.predict(df_test)
            df_test['Shape'] = data['Shape']
            df_test['Actual Depth'] = data['Actual Depth']
            df_test['NN_Depth'] = nn_depth
            df_test['NN_Depth'] = df_test['NN_Depth'].apply(lambda x: depth_range(x))
            df_test['Depth Difference'] = abs(df_test['Actual Depth'] - df_test['NN_Depth']) 
            within_spec = len(df_test[df_test['Depth Difference']<=10])
            st.dataframe(df_test)
            unity_plot = st.checkbox("Show Unity Plots:", key="ILI")
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
                fig = update_traces(fig, 0, 90, "with ILI Predicted Dimensions", "Actual Depth (%)", "NN Depth (%)", 10)
                # st.write(f"Total: {len(df_test)}")
                st.markdown(f"Total: {len(df_test)} defects \n\n Within 10% Tolerance:{within_spec} -- {round(within_spec/len(df_test)*100)}%")
                st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], df_test['NN_Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)
        
        xgboost_depths = st.checkbox("Predict the Depths (Using XGBoost Model):")
        if xgboost_depths:
            df_test = parsed_data(data)
            df_t = xgb.DMatrix(df_test)
            xgb_depth = xgboost_model.predict(df_t)
            df_test['Shape'] = data['Shape']
            df_test['Actual Depth'] = data['Actual Depth']
            df_test['XGB_Depth'] = xgb_depth
            df_test['XGB_Depth'] = df_test['XGB_Depth'].apply(lambda x: depth_range(x))
            df_test['Depth Difference'] = abs(df_test['Actual Depth'] - df_test['XGB_Depth']) 
            within_spec = len(df_test[df_test['Depth Difference']<=10])
            st.dataframe(df_test)
            unity_plot = st.checkbox("Show Unity Plots:", key="ILI_xgb")
            if unity_plot:
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x = data['Actual Depth'],
                        y = df_test['XGB_Depth'],
                        mode = 'markers',
                        showlegend = False
                ))
                fig = draw_unity(fig, 0, 90)
                fig = draw_tolerance_lines(fig, 0, 90, 10, unit="%")
                fig = update_traces(fig, 0, 90, "with ILI Predicted Dimensions", "Actual Depth (%)", "XGB Depth (%)", 10)
                # st.write(f"Total: {len(df_test)}")
                st.markdown(f"Total: {len(df_test)} defects \n\n Within 10% Tolerance:{within_spec} -- {round(within_spec/len(df_test)*100)}%")
                st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], df_test['XGB_Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)


    with col2:
        st.subheader("Predicted Depth Data - (on Actual Dimensions)")
        retrieve_actual_dimensions = st.checkbox("Retrieve Actual Dimensions:")
        if retrieve_actual_dimensions:
            replaced_length_width_data = preprocess_length_width(data)
            parsed_df = parsed_data(replaced_length_width_data)
            nn_depth = nn_model.predict(parsed_df)
            parsed_df['Shape'] = data['Shape']
            parsed_df['Actual Depth'] = data['Actual Depth']
            parsed_df['NN_Depth'] = nn_depth
            parsed_df['NN_Depth'] = parsed_df['NN_Depth'].apply(lambda x: depth_range(x))
            parsed_df['Depth Difference'] = abs(parsed_df['Actual Depth'] - parsed_df['NN_Depth']) 
            within_spec = len(parsed_df[parsed_df['Depth Difference']<=10])
            st.dataframe(parsed_df)
            unity_plot = st.checkbox("Show Unity Plots:", key="Actual")
            if unity_plot:
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x = data['Actual Depth'],
                        y = parsed_df['NN_Depth'],
                        mode = 'markers',
                        showlegend = False
                ))
                fig = draw_unity(fig, 0, 90)
                fig = draw_tolerance_lines(fig, 0, 90, 10, unit="%")
                fig = update_traces(fig, 0, 90, "with Actual Dimensions", "Actual Depth (%)", "NN Depth (%)", 10)
                st.markdown(f"Total: {len(parsed_df)} defects \n\n Within 10% Tolerance:{within_spec} -- {round((within_spec/len(parsed_df))*100,2)}%")

                # st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], parsed_df['NN_Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)

        xgboost_depths = st.checkbox("Predict the Depths (Using XGBoost Model):", key="Actual_XGB_pred")
        if xgboost_depths:
            replaced_length_width_data = preprocess_length_width(data)
            parsed_df = parsed_data(replaced_length_width_data)
            df_p = xgb.DMatrix(parsed_df)
            xgb_depth = xgboost_model.predict(df_p)
            # xgb_depth = xgboost_model.predict(parsed_df)
            parsed_df['Shape'] = data['Shape']
            parsed_df['Actual Depth'] = data['Actual Depth']
            parsed_df['XGB_Depth'] = xgb_depth
            parsed_df['XGB_Depth'] = parsed_df['XGB_Depth'].apply(lambda x: depth_range(x))
            parsed_df['Depth Difference'] = abs(parsed_df['Actual Depth'] - parsed_df['XGB_Depth']) 
            within_spec = len(parsed_df[parsed_df['Depth Difference']<=10])
            st.dataframe(parsed_df)
            unity_plot = st.checkbox("Show Unity Plots:", key="Actual_xgb")
            if unity_plot:
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x = data['Actual Depth'],
                        y = parsed_df['XGB_Depth'],
                        mode = 'markers',
                        showlegend = False
                ))
                fig = draw_unity(fig, 0, 90)
                fig = draw_tolerance_lines(fig, 0, 90, 10, unit="%")
                fig = update_traces(fig, 0, 90, "with ILI Predicted Dimensions", "Actual Depth (%)", "XGB Depth (%)", 10)
                # st.write(f"Total: {len(df_test)}")
                st.markdown(f"Total: {len(parsed_df)} defects \n\n Within 10% Tolerance:{within_spec} -- {round(within_spec/len(parsed_df)*100)}%")
                st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], parsed_df['XGB_Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)

    



