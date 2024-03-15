import plotly.graph_objects as go
from src.charts.draw_tolerance_lines import draw_tolerance_lines

from src.charts.draw_unity import draw_unity
from src.charts.update_traces import update_traces 

def unity_plot(df, data, model_used, title_string, totalObservationsString, actual_depth="Actual Depth"):
    start = 0
    end = 90
    tolerance = 10
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = data[actual_depth],
            y = df[f"{model_used} Depth"],
            mode = "markers",
            showlegend= False,
            # hovertemplate='Item 3#: %{data['']}'
            hovertext = data['Item #'],
            hoverlabel=dict(namelength=0),
            hovertemplate='Item # %{hovertext}'
        )
    )
    fig.add_annotation(
        x = 35,
        y = 85,
        text=f"<b>{totalObservationsString}<b>",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=12,
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
                        string=f"{title_string} with {model_used}", 
                        col1=f"{actual_depth} (%)", 
                        col2=f"{model_used} Depth (%)", 
                        tick=10, plotWidth=800, plotHeight=600)
    return fig