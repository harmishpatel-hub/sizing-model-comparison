def update_traces(fig, start, end, string, col1, col2, tick, plotWidth, plotHeight):
    fig.update_xaxes(range=[start, end], showticklabels=True)
    fig.update_yaxes(range=[start, end], showticklabels=True)
    fig.update_traces(
        marker_size = 8,
        marker_color = 'rgba(255, 255, 255, 0)',
        marker_line_width = 0.8,
        marker_line_color = 'rgba(94, 0, 0, 0.93)'
        )
    fig.update_layout(
        title = f'Unity Plot - {string} ',
        width = plotWidth,
        height = plotHeight,
        xaxis_title = f'{col1}',
        yaxis_title = f'{col2}',
        xaxis = dict(
            tick0 = tick,
            dtick = tick
        ),
        yaxis = dict(
            tick0 = tick,
            dtick = tick
        )
    )
    return fig