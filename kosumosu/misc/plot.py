from kosumosu.core.chart import Chart
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models import Range1d


def plot_histogram(data_frame, value_col=None, title=None, bins=10):
    ch = Chart()
    if title:
        ch.set_title(title)
    hist, edges = np.histogram(data_frame[value_col], bins=bins)
    histogram_data = pd.DataFrame({
        'cnts': hist,
        'min_edge': edges[:-1],
        'max_edge': edges[1:]
    })

    data = ColumnDataSource(histogram_data)
    plot = ch.figure
    plot.quad('min_edge', 'max_edge', 'cnts', 0, source=data)
    plot.x_range = Range1d(min(edges), max(edges))
    plot.y_range = Range1d(0, max(hist))

    return plot


def plot_many_histograms(data_frame, value_col=None, group_col=None, title_template=None, bins=10):
    group_values = data_frame[group_col].unique()
    plots = list()

    for group_value in group_values:
        plot = plot_histogram(data_frame[data_frame[group_col] == group_value], value_col=value_col, title=title_template.format(group_value), bins=bins)
        plots.append(plot)

    return plots
