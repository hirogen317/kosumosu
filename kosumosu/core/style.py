

class Style:

    def __init__(self, chart):
        self.settings = {
            'chart': {
                # use for chart
                'figure.background_fill_color': "white",
                'figure.xgrid.grid_line_color': None,
                'figure.ygrid.grid_line_color': None,
                'figure.border_fill_color': "white",
                'figure.xaxis.axis_line_width': 1,
                'figure.yaxis.axis_line_width': 1,
                'figure.yaxis.axis_line_color': "#C0C0C0",
                'figure.xaxis.axis_line_color': "#C0C0C0",
                'figure.yaxis.axis_label_text_color': "#666666",
                'figure.xaxis.axis_label_text_color': "#666666",
                'figure.xaxis.major_tick_line_color': "#C0C0C0",
                'figure.xaxis.minor_tick_line_color': "#C0C0C0",
                'figure.yaxis.major_tick_line_color': "#C0C0C0",
                'figure.yaxis.minor_tick_line_color': "#C0C0C0",
                'figure.xaxis.major_label_text_color': '#898989',
                'figure.yaxis.major_label_text_color': '#898989',
            },
            'categorical_xaxis': {
                # Used for grouped categorical axes
                'figure.xaxis.separator_line_alpha': 0,
                'figure.xaxis.subgroup_text_font': 'helvetica',
                'figure.xaxis.group_text_font': 'helvetica',
                'figure.xaxis.subgroup_text_font_size': "11pt",
                'figure.xaxis.group_text_font_size': "11pt",
                'figure.x_range.factor_padding': .25
            },
            'categorical_yaxis': {
                # Used for grouped categorical axes
                'figure.yaxis.separator_line_alpha': 0,
                'figure.yaxis.subgroup_text_font': 'helvetica',
                'figure.yaxis.group_text_font': 'helvetica',
                'figure.y_range.factor_padding': .25,
                'figure.yaxis.subgroup_text_font_size': "11pt",
                'figure.yaxis.group_text_font_size': "11pt",
            },
        }
        self._chart = chart

    def _apply_bokeh_settings(self, attributes):
        for key, value in attributes.items():
            self._apply_bokeh_setting(key, value)

    def _apply_bokeh_setting(self, attribute, value, base_obj=None):
        """Recursively apply the settings value to the given settings attribute.
        Recursion is necessary because some bokeh objects may
        have multiple child objects.
        E.g. figures can have more than one x-axis.
        """
        # If not a bokeh attribute then we don't need to apply anything.
        if 'figure' not in attribute and base_obj is None:
            return

        split_attribute = attribute.split('.')
        if base_obj is None:
            base_obj = self._chart
        if len(split_attribute) == 1:
            setattr(base_obj, attribute, value)
        else:
            for i, attr in enumerate(split_attribute):
                # If the attribute contains a list, the slice the list.
                list_split = attr.split('[')
                list_index = None
                if len(list_split) > 1:
                    list_index = int(list_split[1].replace(']', ''))
                    attr = list_split[0]

                if i < len(split_attribute) - 1:
                    base_obj = getattr(base_obj, attr)
                # Slice the list if list_index is not None
                if list_index is not None:
                    base_obj = base_obj[list_index]
                # If the base object is a list, then apply settings to each
                # element.
                if isinstance(base_obj, (list, )):
                    for obj in base_obj:
                        self._apply_bokeh_setting(
                            '.'.join(split_attribute[i + 1:]),
                            value,
                            base_obj=obj)
                    break
            else:
                setattr(base_obj, attr, value)

    def _apply_settings(self, key):
        setting_values = self.settings[key]
        self._apply_bokeh_settings(setting_values)


