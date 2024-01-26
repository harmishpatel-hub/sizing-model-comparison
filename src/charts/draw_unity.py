import numpy as np
import plotly.graph_objects as go


def draw_unity(fig, start, end):
    fig.update_xaxes(range=[start, end], zeroline=False)
    fig.update_yaxes(range=[start, end])
    fig.add_trace(go.Scatter(
        x = np.arange(start, end+1, 1),
        y = np.arange(start, end+1, 1),
        mode = 'lines',
        line = dict(color='rgba(96, 3, 3, 0.5)', width=2, dash='dash'),
        name = 'Unity Line',
        hoverinfo = 'skip'
    ))
    return fig