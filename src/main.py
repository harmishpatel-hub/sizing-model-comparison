from src.datasetCreation.createDataframe import create_df
from src.datasetCreation.createDataframe import createListfromRange
from src.charts.draw_scatter import drawPhysicsChart
from src.charts.unity_figure import unity_plot
from src.dataset_postprocessing import depth_range, post_processing
from src.score.model_score import model_score
from src.dataset_preprocessing import parsed_data, read_excel
from src.dataset_preprocessing import preprocess_shape_depth
from src.dataset_preprocessing import preprocess_length_width
from src.read_model import read_model, read_xgboost_model

import streamlit as st
import xgboost as xgb

def main():
    st.set_page_config(layout="wide")
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
    ### ILI PREDICTED DIMENSION
    with col1:
        st.subheader("Predicted Depth - (ILI Dimensions)")
        predict_depths = st.checkbox("Predict the Depths with NN (ILI Dimensions):")
        if predict_depths:
            df_test = parsed_data(data)
            nn_depth = nn_model.predict(df_test)
            df_test = post_processing(df_test, data, "NN", nn_depth)
            within_spec = len(df_test[df_test['Depth Difference']<=10])
            st.dataframe(df_test)
            unity_plot_checkbox = st.checkbox("Show Unity Plots (NN):", key="ILI")
            if unity_plot_checkbox:
                fig = unity_plot(df_test, data, "NN", "ILI Predicted Dimensions")
                st.markdown(f"Total: {len(df_test)} defects \n\n Within 10% Tolerance:{within_spec} -- {round(within_spec/len(df_test)*100)}%")
                # st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], df_test['NN Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)
        
        xgboost_depths = st.checkbox("Predict the Depths with XGBoost (ILI Dimensions):")
        if xgboost_depths:
            df_test = parsed_data(data)
            df_t = xgb.DMatrix(df_test)
            xgb_depth = xgboost_model.predict(df_t)
            df_test = post_processing(df_test, data, "XGB", xgb_depth)
            within_spec = len(df_test[df_test['Depth Difference']<=10])
            st.dataframe(df_test)
            unity_plot_checkbox = st.checkbox("Show Unity Plots (XGBOOST):", key="ILI_xgb")
            if unity_plot_checkbox:
                fig = unity_plot(df_test, data, "XGB", "ILI Predicted Dimensions")
                st.markdown(f"Total: {len(df_test)} defects \n\n Within 10% Tolerance:{within_spec} -- {round(within_spec/len(df_test)*100)}%")
                # st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], df_test['XGB Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)

    ### ACTUAL DIMENSION
    with col2:
        st.subheader("Predicted Depth - (Actual Dimensions)")
        retrieve_actual_dimensions = st.checkbox("Predict the Depths with NN (Actual Dimensions):")
        if retrieve_actual_dimensions:
            replaced_length_width_data = preprocess_length_width(data)
            parsed_df = parsed_data(replaced_length_width_data)
            nn_depth = nn_model.predict(parsed_df)
            parsed_df = post_processing(parsed_df, data, "NN", nn_depth)
            within_spec = len(parsed_df[parsed_df['Depth Difference']<=10])
            st.dataframe(parsed_df)
            unity_plot_checkbox = st.checkbox("Show Unity Plots (NN):", key="Actual")
            if unity_plot_checkbox:
                fig = unity_plot(parsed_df, data, "NN", "Actual Dimensions")
                st.markdown(f"Total: {len(parsed_df)} defects \n\n Within 10% Tolerance:{within_spec} -- {round((within_spec/len(parsed_df))*100,2)}%")
                # st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], parsed_df['NN Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)

        xgboost_depths = st.checkbox("Predict the Depths with XGBoost (Actual Dimensions):")
        if xgboost_depths:
            replaced_length_width_data = preprocess_length_width(data)
            parsed_df = parsed_data(replaced_length_width_data)
            df_p = xgb.DMatrix(parsed_df)
            xgb_depth = xgboost_model.predict(df_p)
            parsed_df = post_processing(parsed_df, data, "XGB", xgb_depth)
            within_spec = len(parsed_df[parsed_df['Depth Difference']<=10])
            st.dataframe(parsed_df)
            unity_plot_checkbox = st.checkbox("Show Unity Plots (XGBOOST):", key="Actual_xgb")
            if unity_plot_checkbox:
                fig = unity_plot(parsed_df, data, "XGB", "Actual Dimensions")
                # st.write(f"Total: {len(df_test)}")
                st.markdown(f"Total: {len(parsed_df)} defects \n\n Within 10% Tolerance:{within_spec} -- {round(within_spec/len(parsed_df)*100)}%")
                # st.write()
                nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], parsed_df['XGB Depth'])
                st.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
                st.plotly_chart(fig)

    physicsChart = st.checkbox("Physics Chart (Width vs Depth):")
    if physicsChart:
        wt = st.selectbox("Select Wall Thickness (in):", 
                          options = createListfromRange(
                              startingElement=0.10, 
                              lastElement=1.05, 
                              steps=0.025, 
                              decimal=3)
                              )
        external_internal = st.selectbox("Select External or Internal :", 
                                         options = ['External', 'Internal'])
        length = st.selectbox("Select Length (in):", 
                              options = createListfromRange(
                                  startingElement=0.10, 
                                  lastElement=3.05, 
                                  steps=0.05, 
                                  decimal=3)
                                  )
        peak_value = st.selectbox("Select Peak Value:", 
                                  options = createListfromRange(
                                      startingElement=0, 
                                      lastElement=-4000, 
                                      steps=-25, 
                                      decimal=0)
                                      )
        width = createListfromRange(
                    startingElement=0.10, 
                    lastElement=3.05, 
                    steps=0.05, 
                    decimal=3)
        
        dimensionDF = create_df(length, width, peak_value, wt, external_internal)
        
        nnPredictions = nn_model.predict(dimensionDF)
        dimensionDF['NN Depth'] = nnPredictions
        dimensionDF['NN Depth'] = dimensionDF['NN Depth'].apply(lambda x: depth_range(x))
        st.write(dimensionDF.shape)
        st.write(dimensionDF)
        fig = drawPhysicsChart(dimensionDF, colX='width', colY='NN Depth', tick = 5)
        fig.update_xaxes(range=[0.05, 3.05], showticklabels=True)
        fig.update_yaxes(range=[5, 85], showticklabels=True)
        st.plotly_chart(fig)

