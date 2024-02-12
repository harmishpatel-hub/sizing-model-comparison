import streamlit as st
import xgboost as xgb
import matplotlib
import os
from src.component.downloadPDF import downloadPDF
from src.charts.draw_mlClassUnity import mlClassUnity
from src.charts.unity_figure import unity_plot
from src.dataset_postprocessing import post_processing

from src.dataset_preprocessing import parsed_data, preprocess_length_width, preprocess_shape_depth, read_excel
from src.read_model import read_model, read_xgboost_model
from src.score.model_score import model_score 

def modelTestingFilter(PULLTEST_DATASET_OPTIONS, ONNX_MODEL_OPTIONS, XGBOOST_MODEL_OPTIONS):
    
    # st.write(XGBOOST_MODEL_OPTIONS)
    pipe_size = st.sidebar.selectbox("Select Pipe Size[in]:", options=PULLTEST_DATASET_OPTIONS)

    if pipe_size:
        READ_EXCEL_FILES = f"./pulltest_dataset/{pipe_size}/"
        df = read_excel(READ_EXCEL_FILES)
        # st.dataframe(df)
        data = preprocess_shape_depth(df)
        # st.dataframe(data)
        

    select_model = st.sidebar.selectbox("Select Neural Network Model:", options=ONNX_MODEL_OPTIONS)
    if select_model:
        READ_MODEL_FILE = f"./onnx_models/{select_model}/"
        nn_model = read_model(READ_MODEL_FILE)
    
    select_xgboost_model = st.sidebar.selectbox("Select XGBoost Model:", options=XGBOOST_MODEL_OPTIONS)
    if select_xgboost_model:
        READ_XGBOOST_MODEL_FILE = f"./onnx_models/xgboost_model/{select_xgboost_model}/"
        xgboost_model = read_xgboost_model(READ_XGBOOST_MODEL_FILE)

    col1, col2 = st.columns(2)
    ### ILI PREDICTED DIMENSION
    with col1:
        st.subheader("Predicted Depth - (ILI Dimensions)")
        predict_depths = st.checkbox("Predict the Depths with NN (ILI Dimensions):")
        if predict_depths:
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Unity Plot", "💹 ML Class Unity Plot", "📊 Statistics", "💾 Data"])
            df_test = parsed_data(data)
            nn_depth = nn_model.predict(df_test)
            df_test = post_processing(df_test, data, "NN", nn_depth)
            within_spec = len(df_test[df_test['Depth Difference']<=10])
            # showDf = df_test
            # tab4.dataframe(df_test.style.background_gradient(subset=['Actual Depth']), height=100*len(df_test))
            tab4.dataframe(df_test)
            totalObservationsString = f"Total: {len(df_test)} defects \n\n Within ±10% Tolerance:{within_spec} -- {round(within_spec/len(df_test)*100)}%"
            tab3.markdown(totalObservationsString)
            # st.write()
            nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], df_test['NN Depth'])
            tab3.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")

            fig = unity_plot(df_test, data, "NN", "ILI Predicted Dimensions", totalObservationsString)
            # mlClassUnityFigList = mlClassUnity(data=df_test, colMLClass="ml_class", model_used="NN", title_string="ILI Predicted Dimensions")
            mlClassUnityFigList, mlClassStats = mlClassUnity(data=df_test, 
                                               colMLClass="ml_class", 
                                               model_used="NN", 
                                               title_string="ILI Predicted Dimensions")
            
            tab1.plotly_chart(fig)
            for i in mlClassUnityFigList:
                tab2.plotly_chart(mlClassUnityFigList[i])
            for i in mlClassStats:
                tab3.divider()
                tab3.subheader(i)
                tab3.write(f"\n\n {mlClassStats[i]}")
                
                
        
        xgboost_depths = st.checkbox("Predict the Depths with XGBoost (ILI Dimensions):")
        if xgboost_depths:
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Unity Plot", "💹 ML Class Unity Plot", "📊 Statistics", "💾 Data"])
            df_test = parsed_data(data)
            df_t = xgb.DMatrix(df_test)
            xgb_depth = xgboost_model.predict(df_t)
            df_test = post_processing(df_test, data, "XGB", xgb_depth)
            within_spec = len(df_test[df_test['Depth Difference']<=10])
            tab4.dataframe(df_test)
            totalObservationsString = f"Total: {len(df_test)} defects \n\n Within ±10% Tolerance:{within_spec} -- {round(within_spec/len(df_test)*100)}%"
            tab3.markdown(totalObservationsString)
            # st.write()
            nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], df_test['XGB Depth'])
            tab3.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
            fig = unity_plot(df_test, data, "XGB", "ILI Predicted Dimensions", totalObservationsString=totalObservationsString)
            # mlClassUnityFigList = mlClassUnity(data=df_test, colMLClass="ml_class", model_used="XGB", title_string="ILI Predicted Dimensions")
            mlClassUnityFigList, mlClassStats = mlClassUnity(data=df_test, 
                                               colMLClass="ml_class", 
                                               model_used="XGB", 
                                               title_string="ILI Predicted Dimensions")
            
            tab1.plotly_chart(fig)
            for i in mlClassUnityFigList:
                tab2.plotly_chart(mlClassUnityFigList[i])
            for i in mlClassStats:
                tab3.divider()
                tab3.subheader(i)
                tab3.write(f"\n\n {mlClassStats[i]}")

    ### ACTUAL DIMENSION
    with col2:
        st.subheader("Predicted Depth - (Actual Dimensions)")
        retrieve_actual_dimensions = st.checkbox("Predict the Depths with NN (Actual Dimensions):")
        if retrieve_actual_dimensions:
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Unity Plot", "💹 ML Class Unity Plot", "📊 Statistics", "💾 Data"])
            replaced_length_width_data = preprocess_length_width(data)
            parsed_df = parsed_data(replaced_length_width_data)
            nn_depth = nn_model.predict(parsed_df)
            parsed_df = post_processing(parsed_df, data, "NN", nn_depth)
            within_spec = len(parsed_df[parsed_df['Depth Difference']<=10])
            tab4.dataframe(parsed_df)
            totalObservationsString = f"Total: {len(parsed_df)} defects | Within ±10% Tolerance:{within_spec} -- {round((within_spec/len(parsed_df))*100,2)}%"
            tab3.markdown(totalObservationsString)
            # st.write()
            nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], parsed_df['NN Depth'])
            tab3.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")
            
            fig = unity_plot(parsed_df, data, "NN", "Actual Dimensions", totalObservationsString=totalObservationsString)
            mlClassUnityFigList, mlClassStats = mlClassUnity(data=parsed_df, 
                                               colMLClass="ml_class", 
                                               model_used="NN", 
                                               title_string="Actual Dimensions")
            
            
            tab1.plotly_chart(fig)
            for i in mlClassUnityFigList:
                tab2.plotly_chart(mlClassUnityFigList[i])
            for i in mlClassStats:
                tab3.divider()
                tab3.subheader(i)
                tab3.write(f"\n\n {mlClassStats[i]}")
            # re = downloadPDF(mlClassUnityFigList, "Unity Plot", "Metal Loss")
            # tab2.download_button(label="Export Charts",
            #                      data=re.output('', dest='S').encode('latin-1'),
            #                      file_name=f"Unity Plot.pdf",
            #                      mime = 'application/octate_stream',
            #                      key = 'pdf download'
            #                     )

        xgboost_depths = st.checkbox("Predict the Depths with XGBoost (Actual Dimensions):")
        if xgboost_depths:
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Unity Plot", "💹 ML Class Unity Plot", "📊 Statistics", "💾 Data"])
            replaced_length_width_data = preprocess_length_width(data)
            parsed_df = parsed_data(replaced_length_width_data)
            df_p = xgb.DMatrix(parsed_df)
            xgb_depth = xgboost_model.predict(df_p)
            parsed_df = post_processing(parsed_df, data, "XGB", xgb_depth)
            within_spec = len(parsed_df[parsed_df['Depth Difference']<=10])
            tab4.dataframe(parsed_df)
            totalObservationsString = f"Total: {len(parsed_df)} defects \n\n Within ±10% Tolerance:{within_spec} -- {round(within_spec/len(parsed_df)*100)}%"
            tab3.markdown(totalObservationsString)
            # st.write()
            nn_mae, nn_mse, nn_rmse = model_score(data['Actual Depth'], parsed_df['XGB Depth'])
            tab3.markdown(f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}")

            fig = unity_plot(parsed_df, data, "XGB", "Actual Dimensions", totalObservationsString=totalObservationsString)
            mlClassUnityFigList, mlClassStats = mlClassUnity(data=parsed_df, 
                                               colMLClass="ml_class", 
                                               model_used="XGB", 
                                               title_string="Actual Dimensions")
            
            tab1.plotly_chart(fig)
            for i in mlClassUnityFigList:
                tab2.plotly_chart(mlClassUnityFigList[i])
            
            for i in mlClassStats:
                tab3.divider()
                tab3.subheader(i)
                tab3.write(f"\n\n {mlClassStats[i]}")