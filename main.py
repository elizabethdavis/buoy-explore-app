import numpy as np
import xarray as xr
import pandas as pd
import itertools

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, CDSView, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, TextInput, LabelSet, HoverTool, NumeralTickFormatter
from bokeh.models.widgets import CheckboxGroup, NumberFormatter
from bokeh.io import show, curdoc
from bokeh.layouts import column, row, grid, WidgetBox
from datetime import date
from bokeh.palettes import Spectral4 as palette

bokeh_doc = curdoc()

# ------------------------------------------------------------------------------
# Function: load dataset
# ------------------------------------------------------------------------------
def find_dataset(buoy_input, start_date, end_date):
    data_url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/' + buoy_input + '/' + buoy_input + '.ncml'
    ds = xr.open_dataset(data_url)
    ds = ds.sel(time=slice(start_date, end_date))
    df = ds.to_dataframe().reset_index().set_index('time')
    source = ColumnDataSource(df)

    print("url: " + data_url)
    print("Data has been found for buoy #" + buoy_input)

    return source

def make_temp_plot(source, buoy_input, checkbox_group):
    p = figure(plot_width = 500, plot_height = 300,
               x_axis_label = 'Time',
               x_axis_type = "datetime",
               y_axis_label = 'degrees C',
               title="Temperature",
               name="temperature_plot")

    color = itertools.cycle(palette)

    # temperature plot (degrees Celsius)
    p.line(x='time', y='air_temperature', legend_label = "Air Temperature", source=source, color=next(color))
    p.line(x='time', y='sea_surface_temperature', legend_label = "Sea Surface Temperature", source=source, color=next(color))
    p.line(x='time', y='dewpt_temperature', legend_label = "Dew Point Temperature", source=source, color=next(color))

    p.legend.click_policy = "hide"

    return p

def make_wvpd_plot(source, buoy_input, checkbox_group):
    p_wvpd = figure(plot_width = 500, plot_height = 300,
               x_axis_label = 'Time',
               x_axis_type = "datetime",
               y_axis_label = 'seconds',
               title="Dominant and Average Wave Period",
               name="wave_period_plot")

    # wave period plot (seconds)
    p_wvpd.line(x='time', y='average_wpd', legend_label = "Average Wave Period", source=source)
    p_wvpd.line(x='time', y='dominant_wpd', legend_label = "Dominant Wave Period", source=source)

    p_wvpd.legend.click_policy = "hide"

    return p_wvpd

def make_dir_plot(source, buoy_input, checkbox_group):
    p_dir = figure(plot_width = 500, plot_height = 300,
                   x_axis_label = 'Time',
                   x_axis_type = "datetime",
                   y_axis_label = 'Degrees from true north (degT)',
                   title="Mean wave direction & wind direction",
                   name="direction_plot")

    # (degrees from true north (degT))
    p_dir.line(x='time', y='mean_wave_dir', legend_label = "Mean Wave Direction", source=source)
    p_dir.line(x='time', y='wind_dir', legend_label = "Wind Direction", source=source)

    p_dir.legend.click_policy = "hide"

    return p_dir

def make_tide_plot(source, buoy_input, checkbox_group):
    p_tide = figure(plot_width = 500, plot_height = 300,
                    x_axis_label = 'Time',
                    x_axis_type = "datetime",
                    y_axis_label = 'meters',
                    title="Wave Height & Tide",
                    name="tide_plot")

    # (meters)
    p_tide.scatter(x='time', y='wave_height', legend_label = "Wave Height", source=source)
    p_tide.scatter(x='time', y='water_level', legend_label = "Water Level", source=source)

    p_tide.legend.click_policy = "hide"

    return p_tide

def make_speed_plot(source, buoy_input, checkbox_group):
    p_speed = figure(plot_width = 500, plot_height = 300,
                     x_axis_label = 'Time',
                     x_axis_type = "datetime",
                     y_axis_label = 'm/s',
                     title="Wind Speed & Gust",
                     name="speed_plot")

    # wind speed and gust (m/s)
    p_speed.scatter(x='time', y='gust', legend_label = "Gust", source=source, alpha=0.3)
    p_speed.scatter(x='time', y='wind_spd', legend_label = "Wind Speed", source=source, alpha=0.3)

    p_speed.legend.click_policy = "hide"

    return p_speed

def make_viz_plot(source, buoy_input, checkbox_group):
    p_viz = figure(plot_width = 500, plot_height = 300,
                   x_axis_label = 'Time',
                   x_axis_type = "datetime",
                   y_axis_label = 'Nautical miles',
                   title="Visibility",
                   name="visibility_plot")

    # (nautical miles)
    p_viz.line(x='time', y='visibility', legend_label = "Visibility", source=source)

    p_viz.legend.click_policy = "hide"

    return p_viz

def make_pressure_plot(source, buoy_input, checkbox_group):
    hover_tool = HoverTool(
        tooltips = [
            ('Air Pressure', '@air_pressure{(0000.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            mode='vline')

    p_pressure = figure(plot_width = 500, plot_height = 300,
               x_axis_label = 'Time',
               x_axis_type = "datetime",
               y_axis_label = 'hPa',
               title="Air Pressure",
               name="pressure_plot")

    # (hPa)
    p_pressure.line(x='time', y='air_pressure', legend_label = "Air Pressure", source=source)
    p_pressure.add_tools(hover_tool)
    p_pressure.legend.click_policy = "hide"

    return p_pressure
# ------------------------------------------------------------------------------
# Function: update plot based on selections
# ------------------------------------------------------------------------------
def update_plot(attr, old, new):
     # update checkbox group
     checkbox_group_updated = [checkbox_group.labels[i] for i in checkbox_group.active]
     print(checkbox_group_updated)

     # update start date
     start_date_updated = start_date_picker.value
     print("start date:" + start_date_updated)

     # update end date
     end_date_updated = end_date_picker.value
     print("end date:" + end_date_updated)

     # update buoy number
     buoy_input_updated = buoy_input.value
     print("buoy ID:" + buoy_input_updated)

     # find new source data
     source_updated = find_dataset(buoy_input = buoy_input_updated,
                                   start_date = start_date_updated,
                                   end_date = end_date_updated)

     # update source data
     source.data = dict(source_updated.data)
# ------------------------------------------------------------------------------
# Widget creation and customization
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Widget: Text Input
# ------------------------------------------------------------------------------
buoy_input = TextInput(value='44066', title="Buoy ID Number", name="buoy_input")
buoy_input.on_change("value", update_plot)

# ------------------------------------------------------------------------------
# Widget: Data Table
# ------------------------------------------------------------------------------
formatter = NumberFormatter(format='0.000')

columns = [
    TableColumn(field="time", title="Time", formatter=DateFormatter()),
    TableColumn(field="wind_dir", title="Wind Direction (°C)", formatter=formatter),
    TableColumn(field="wind_spd", title="Wind Speed (m/s)", formatter=formatter),
    TableColumn(field="gust", title="Gust (m/s)", formatter=formatter),
    TableColumn(field="wave_height", title="Wave Height (m)", formatter=formatter),
    TableColumn(field="dominant_wpd", title="Dominant Wave Period (seconds)", formatter=formatter),
    TableColumn(field="average_wpd", title="Average Wave Period (seconds)", formatter=formatter),
    TableColumn(field="mean_wave_dir", title="Mean Wave Direction (degT)", formatter=formatter),
    TableColumn(field="air_pressure", title="Air Pressure (hPa)", formatter=formatter),
    TableColumn(field="air_temperature", title="Air Temperature (°C)", formatter=formatter),
    TableColumn(field="sea_surface_temperature", title="Sea Surface Temperature (°C)", formatter=formatter),
    TableColumn(field="dewpt_temperature", title="Dew Point Temperature (°C)", formatter=formatter),
    TableColumn(field="visibility", title="Visibility (nmi)", formatter=formatter),
    TableColumn(field="water_level", title="Water Level (ft)", formatter=formatter),
]

# ------------------------------------------------------------------------------
# Widget: Date Picker
# ------------------------------------------------------------------------------
start_date_picker = DatePicker(title='Start date', value='2021-07-24', name="start_date")
start_date_picker.on_change("value", update_plot)

end_date_picker = DatePicker(title='End date', value=date.today(), name="end_date")
end_date_picker.on_change("value", update_plot)

# ------------------------------------------------------------------------------
# Widget: Checkbox Group
# ------------------------------------------------------------------------------
#labels = ["wind_dir", "Wind Speed", "Gust", "Wave Height",
#          "Dominant Wave Period", "Average Wave Period", "Mean Wave Direction",
#          "Air Pressure", "air_temperature", "Sea Surface Temperature",
#          "Dew Point Temperature", "Visibility", "Water Level"]
labels = ["wind_dir", "wind_spd", "gust", "wave_height",
          "dominant_wpd", "average_wpd", "mean_wave_dir",
          "air_pressure", "air_temperature", "sea_surface_temperature",
          "dewpt_temperature", "visibility", "water_level"]
checkbox_group = CheckboxGroup(labels=labels, active=[9])
checkbox_group.on_change('active', update_plot)

# ------------------------------------------------------------------------------
# Plot: generate line chart
# ------------------------------------------------------------------------------
initial_checkbox_group = [checkbox_group.labels[i] for i in checkbox_group.active]

source = find_dataset(buoy_input = buoy_input.value,
                      start_date = start_date_picker.value,
                      end_date = end_date_picker.value)

p = make_temp_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
p_wvpd = make_wvpd_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
p_dir = make_dir_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
p_tide = make_tide_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
p_speed = make_speed_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
#p_viz = make_viz_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
p_pressure = make_pressure_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)


#p.sizing_mode = 'scale_width'
#p_wvpd.sizing_mode = 'scale_width'
#p_dir.sizing_mode = 'scale_width'
#p_tide.sizing_mode = 'scale_width'
#p_speed.sizing_mode = 'scale_width'
#p_pressure.sizing_mode = 'scale_width'

data_table = DataTable(source=source, columns=columns, width=1400, height=280, name="data_table")
#data_table.sizing_mode = 'scale_width'

# put controls in a single element
controls = row(buoy_input, start_date_picker, end_date_picker)
#controls.sizing_mode = 'scale_width'

# create a row layout
#row1 = row(controls)
#row2 = row(p, p_pressure, p_dir)
#row3 = row(p_speed, p_tide, p_wvpd)

layout = grid([
        [controls],
        [p, p_pressure, p_dir],
        [p_speed, p_tide, p_wvpd],
])
#bokeh_doc.add_root(layout)
bokeh_doc.add_root(buoy_input)
bokeh_doc.add_root(start_date_picker)
bokeh_doc.add_root(end_date_picker)
bokeh_doc.add_root(p)
bokeh_doc.add_root(p_pressure)
bokeh_doc.add_root(p_dir)
bokeh_doc.add_root(p_speed)
bokeh_doc.add_root(p_tide)
bokeh_doc.add_root(p_wvpd)
bokeh_doc.add_root(data_table)
# show all widgets and graphs on the page
#bokeh_doc.add_root(row1)
#bokeh_doc.add_root(row2)
#bokeh_doc.add_root(row3)
#bokeh_doc.add_root(data_table)
bokeh_doc.title = "OCG592 | Buoy Explore Tool"
