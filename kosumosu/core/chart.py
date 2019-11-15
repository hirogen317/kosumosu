from bokeh.plotting import figure, output_file, show
from kosumosu.core.style import Style


class Chart:

    def __init__(self):
        self.figure = figure(plot_width=800, plot_height=400, match_aspect=True)
        self.style = Style(self)
        self.style._apply_settings('chart')
        self.style._apply_settings('chart')

    def mask(self):
        pass

    def set_title(self, title):
        """Set the chart title.
        Args:
            title (str): Title text.
        Returns:
            Current chart object
        """
        self.figure.title.text = title
        return self
