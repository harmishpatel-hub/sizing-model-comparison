from plotly import graph_objects as go
from src.score.model_score import model_score 
from src.charts.draw_tolerance_lines import draw_tolerance_lines

from src.charts.draw_unity import draw_unity
from src.charts.update_traces import update_traces 

mlClassEncoded={
    0: 'Axial Grooving',
    1: 'Axial Slotting',
    2: 'Circ Grooving',
    3: 'Circ Slotting',
    4: 'General',
    5: 'Pinhole',
    6: 'Pitting'
}

def mlClassUnity(data,  colMLClass, model_used, title_string, actual_depth="Actual Depth"):
    listOfCharts = {}
    listOfStats = {}
    start, end = 0, 90
    tolerance = 10
    for mlCLass in data[colMLClass].unique():
        fig = go.Figure()
        dataMLClass = data[data[colMLClass]==mlCLass]
        fig.add_trace(
            go.Scatter(
                x = dataMLClass[actual_depth],
                y = dataMLClass[f"{model_used} Depth"],
                mode = "markers",
                name = f"{mlClassEncoded[mlCLass]}",
                # hovertext = data['Item #'],
                # hoverlabel=dict(namelength=0),
                # hovertemplate='Item # %{hovertext}'
            )
        )
        withinSpec = dataMLClass[dataMLClass['Depth Difference']<=10]
        totalObservationsString = f"Total: {len(dataMLClass)} defects | Within 10% Tolerance: {len(withinSpec)} -- {round((len(withinSpec)/len(dataMLClass))*100,2)}%"

        fig.add_annotation(
            x = 35,
            y = 87,
            text=f"<b>{totalObservationsString}<b>",
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="#000000"
                ),
            bordercolor="#675c58",
            borderwidth=1,
            bgcolor="#eeeee4",
            opacity=0.8
        )

        fig = draw_unity(fig, start, end)
        fig = draw_tolerance_lines(fig, start, end, tolerance, unit="%")
        fig = update_traces(fig, start, end, 
                            string=f"{title_string} - {mlClassEncoded[mlCLass]}", 
                            col1=f"{actual_depth} (%)", 
                            col2=f"{model_used} Depth (%)", 
                            tick=10, 
                            plotWidth=800, 
                            plotHeight=600)
        
        
        nn_mae, nn_mse, nn_rmse = model_score(dataMLClass[f"{actual_depth}"], dataMLClass[f"{model_used} Depth"])
        
        listOfStats[f"{mlClassEncoded[mlCLass]}"] = f"Total: {len(dataMLClass)} defects \n\n Within 10% Tolerance: {len(withinSpec)} -- {round((len(withinSpec)/len(dataMLClass))*100,2)}% \n\n Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}"

        # listOfStats[f"{mlClassEncoded[mlCLass]} Error"] = f"Mean Absolute Error: {nn_mae}\n\n Mean Squared Error: {nn_mse}\n\n Root Mean Squared Error: {nn_rmse}"
        listOfCharts[f"{mlClassEncoded[mlCLass]}"] = fig

    return listOfCharts, listOfStats