import plotly.graph_objects as go
from src.charts.draw_tolerance_lines import draw_tolerance_lines

from src.charts.draw_unity import draw_unity
from src.charts.update_traces import update_traces 

def unity_plot(df, data, model_used, title_string, actual_depth="Actual Depth"):
    start = 0
    end = 90
    tolerance = 10
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = data[actual_depth],
            y = df[f"{model_used} Depth"],
            mode = "markers",
            showlegend= False
        )
    )
    fig = draw_unity(fig, start, end)
    fig = draw_tolerance_lines(fig, start, end, tolerance, unit="%")
    fig = update_traces(fig, start, end, title_string, f"{actual_depth} (%)", f"{model_used} Depth (%)", 10)
    return fig