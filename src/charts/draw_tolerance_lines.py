import numpy as np
import plotly.graph_objects as go

def draw_tolerance_lines(fig, start, end, tolerance, unit="%", color='rgba(0, 123, 21, 0.58)'):
    fig.add_trace(go.Scatter(
        x = np.arange(tolerance, end+1, 1),
        y = np.arange(start, end+1, 1),
        name = f'± {tolerance} {unit}',
        mode = 'lines',
        line = dict(color=color, width=2, dash='dash'),
        legendgroup = f'± {tolerance}',
        hoverinfo = 'skip'
    ))

    fig.add_trace(go.Scatter(
        x = np.arange(start, end+1, 1),
        y = np.arange(tolerance, end+1, 1),
        mode = 'lines',
        name = f'± {tolerance} {unit}',
        line = dict(color=color, width=2, dash='dash'),
        legendgroup = f'± {tolerance}',
        showlegend = False, 
        hoverinfo = 'skip'
    ))
    return fig