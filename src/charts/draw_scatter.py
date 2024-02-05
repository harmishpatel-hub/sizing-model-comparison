from plotly import graph_objects as go 

def drawPhysicsChart(dataframe, colX, colY, colColor, tick=5):
    fig = go.Figure()
    for len in dataframe[colColor].unique():
        fig.add_trace(
            go.Scatter(
                x = dataframe[dataframe[colColor]==len][colX],
                y = dataframe[dataframe[colColor]==len][colY],
                mode = 'markers+lines',
                name = f"{colColor.upper()} {len} [in]",
                showlegend=True
            )
        )
    fig.update_layout(
        title = f"""{colX.upper()} [in] VS {colY.upper()} [%] 
        | WT={dataframe['wt'].unique()[0]} 
        | EXT/INT = {'EXTERNAL' if dataframe['Ext/Int'].unique()[0] == 1 else 'INTERNAL'} 
        | PEAK VALUE={dataframe['peak_value'].unique()[0]}""",
        width = 1500,
        height = 1200,
        xaxis_title = f"{colX.upper()}",
        yaxis_title = f"{colY.upper()} [%]",
        xaxis = dict(dtick = 0.05),
        yaxis = dict(
            tick0 = tick,
            dtick = tick
        )
    )
    return fig
