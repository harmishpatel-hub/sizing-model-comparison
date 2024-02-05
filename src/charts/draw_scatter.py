from plotly import graph_objects as go 

def drawPhysicsChart(dataframe, colX, colY, tick=5):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = dataframe[colX],
            y = dataframe[colY],
            mode = 'markers+lines'
        )
    )
    fig.update_layout(
        title = f"{colX.upper()} [in] VS {colY.upper()} [%]",
        width = 1000,
        height = 800,
        xaxis_title = f"{colX.upper()}",
        yaxis_title = f"{colY.upper()} [%]",
        xaxis = dict(dtick = 0.05),
        yaxis = dict(
            tick0 = tick,
            dtick = tick
        )
    )
    return fig
