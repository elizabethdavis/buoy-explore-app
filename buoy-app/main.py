import numpy as np
import xarray as xr
import pandas as pd
import itertools

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, CDSView, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, TextInput, LabelSet, HoverTool, NumeralTickFormatter, Select
from bokeh.models.widgets import CheckboxGroup, NumberFormatter
from bokeh.io import show, curdoc
from bokeh.layouts import column, row, grid, WidgetBox
from datetime import date
from bokeh.palettes import YlGnBu9 as palette

from bs4 import BeautifulSoup
import requests

# create empty list
buoys = []

bokeh_doc = curdoc()

tools = "pan, box_zoom, save, reset"

# ------------------------------------------------------------------------------
# Function: Find list of active buoys
# ------------------------------------------------------------------------------
def active_buoys(buoys):
    url = "https://www.ndbc.noaa.gov/activestations.xml"
    xml = requests.get(url)
    doc = BeautifulSoup(xml.content, 'xml')

    for tag in doc.find_all("station", pgm="NDBC Meteorological/Ocean"):
        buoys.append(tag['id'])

    print(type(buoys))
    return buoys

# ------------------------------------------------------------------------------
# Function: Load dataset from NDBC Thredds server
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

# ------------------------------------------------------------------------------
# Function: Create temperature plot
# Sources: Air Temperature, Sea Surface Temperature, Dewpoint Temperature
# Units: Degrees Celsius
# ------------------------------------------------------------------------------
def make_temp_plot(source, buoy_input):
    air_hover = HoverTool(
        tooltips = [
            ('Air Temp', '@air_temperature{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['air_hover'],
            mode='vline')

    sea_hover = HoverTool(
        tooltips = [
            ('Sea Surface Temperature', '@sea_surface_temperature{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['sea_hover'],
            mode='vline')

    dewpt_hover = HoverTool(
        tooltips = [
            ('Dew Point Temperature', '@dewpt_temperature{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['dewpt_hover'],
            mode='vline')

    p = figure(plot_width = 600, plot_height = 400,
               x_axis_label = 'Time',
               x_axis_type = "datetime",
               y_axis_label = 'degrees C',
               title="Temperature",
               name="temperature_plot",
               sizing_mode="scale_width",
               tools=tools)

    air = p.line(x='time', y='air_temperature', legend_label = "Air Temperature", source=source, color=palette[1], name='air_hover')
    p.add_tools(air_hover)
    sea = p.line(x='time', y='sea_surface_temperature', legend_label = "Sea Surface Temperature", source=source, color=palette[2], name='sea_hover')
    p.add_tools(sea_hover)
    dewpt = p.line(x='time', y='dewpt_temperature', legend_label = "Dew Point Temperature", source=source, color=palette[3], name='dewpt_hover')
    p.add_tools(dewpt_hover)

    p.toolbar.active_drag = None
    p.legend.click_policy = "hide"

    return p

# ------------------------------------------------------------------------------
# Function: Create pressure plot
# Sources: Air Pressure
# Units: hPa
# ------------------------------------------------------------------------------
def make_pressure_plot(source, buoy_input):
    hover_tool = HoverTool(
        tooltips = [
            ('Air Pressure', '@air_pressure{(0000.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            mode='vline')

    p_pressure = figure(plot_width = 600, plot_height = 400,
               x_axis_label = 'Time',
               x_axis_type = "datetime",
               y_axis_label = 'hPa',
               title="Air Pressure",
               name="pressure_plot",
               sizing_mode="scale_width",
               tools=tools)

    p_pressure.line(x='time', y='air_pressure', legend_label = "Air Pressure", source=source, color=palette[3])
    p_pressure.add_tools(hover_tool)

    p_pressure.toolbar.active_drag = None
    p_pressure.legend.click_policy = "hide"

    return p_pressure

# ------------------------------------------------------------------------------
# Function: Create direction plot
# Sources: Mean Wave Direction, Wind Direction
# Units: Degrees from true north
# ------------------------------------------------------------------------------
def make_dir_plot(source, buoy_input):
    mean_wave_hover = HoverTool(
        tooltips = [
            ('Mean Wave Direction', '@mean_wave_dir{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['mean_wave_hover'],
            mode='vline')

    wind_dir_hover = HoverTool(
        tooltips = [
            ('Wind Direction', '@wind_dir{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['wind_dir_hover'],
            mode='vline')

    p_dir = figure(plot_width = 600, plot_height = 400,
                   x_axis_label = 'Time',
                   x_axis_type = "datetime",
                   y_axis_label = 'Degrees from true north (degT)',
                   title="Mean wave direction & wind direction",
                   name="direction_plot",
                   sizing_mode="scale_width",
                   tools=tools)

    mean_wave = p_dir.line(x='time', y='mean_wave_dir', legend_label = "Mean Wave Direction", source=source, color=palette[2], name='mean_wave_hover')
    p_dir.add_tools(mean_wave_hover)
    wind_dir = p_dir.line(x='time', y='wind_dir', legend_label = "Wind Direction", source=source, color=palette[3], name='wind_dir_hover')
    p_dir.add_tools(wind_dir_hover)

    p_dir.toolbar.active_drag = None
    p_dir.legend.click_policy = "hide"

    return p_dir

# ------------------------------------------------------------------------------
# Function: Create speed plot
# Sources: Wind Speed, Gust
# Units: Meters per second (m/s)
# ------------------------------------------------------------------------------
def make_speed_plot(source, buoy_input):
    gust_hover = HoverTool(
        tooltips = [
            ('Gust', '@gust{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['gust_hover'],
            mode='vline')

    wind_spd_hover = HoverTool(
        tooltips = [
            ('Wind Speed', '@wind_spd{(00.00)}'),
            ('Date', '@time{%F}')],
            formatters={'@time':'datetime'},
            names=['wind_spd_hover'],
            mode='vline')

    p_speed = figure(plot_width = 600, plot_height = 400,
                     x_axis_label = 'Time',
                     x_axis_type = "datetime",
                     y_axis_label = 'm/s',
                     title="Wind Speed & Gust",
                     name="speed_plot",
                     sizing_mode="scale_width",
                     tools=tools)

    gust = p_speed.line(x='time', y='gust', legend_label = "Gust", source=source, color=palette[4], name='gust_hover')
    p_speed.add_tools(gust_hover)
    wind_spd = p_speed.line(x='time', y='wind_spd', legend_label = "Wind Speed", source=source, color=palette[5], name='wind_spd_hover')
    p_speed.add_tools(wind_spd_hover)

    p_speed.toolbar.active_drag = None
    p_speed.legend.click_policy = "hide"

    return p_speed

# ------------------------------------------------------------------------------
# Function: Create Tide plot
# Sources: Wave Height, Water Level
# Units: Meters
# ------------------------------------------------------------------------------
#def make_tide_plot(source, buoy_input):
#    p_tide = figure(plot_width = 600, plot_height = 400,
#                    x_axis_label = 'Time',
#                    x_axis_type = "datetime",
#                    y_axis_label = 'meters',
#                    title="Wave Height & Tide",
#                    name="tide_plot",
#                    sizing_mode="scale_width",
#                    tools=tools)

#    p_tide.scatter(x='time', y='wave_height', legend_label = "Wave Height", source=source, color=palette[5])
#    p_tide.scatter(x='time', y='water_level', legend_label = "Water Level", source=source, color=palette[6])

#    p_tide.toolbar.active_drag = None
#    p_tide.legend.click_policy = "hide"

#    return p_tide

# ------------------------------------------------------------------------------
# Function: Create wave period plot
# Sources: Dominant and Average Wave Period
# Units: Seconds
# ------------------------------------------------------------------------------
#def make_wvpd_plot(source, buoy_input):
#    p_wvpd = figure(plot_width = 600, plot_height = 400,
#               x_axis_label = 'Time',
#               x_axis_type = "datetime",
#               y_axis_label = 'seconds',
#               title="Dominant and Average Wave Period",
#               name="wave_period_plot",
#               sizing_mode="scale_both",
#               tools=tools)

#    p_wvpd.line(x='time', y='average_wpd', legend_label = "Average Wave Period", source=source, color=palette[0])
#    p_wvpd.line(x='time', y='dominant_wpd', legend_label = "Dominant Wave Period", source=source, color=palette[1])

#    p_wvpd.toolbar.active_drag = None
#    p_wvpd.legend.click_policy = "hide"

#    return p_wvpd

# ------------------------------------------------------------------------------
# Function: Update plots based on input modifications
# Inputs: Buoy ID Number, Date Range (start date and end date)
# ------------------------------------------------------------------------------
def update_plot(attr, old, new):

     # update start date
     start_date_updated = start_date_picker.value
     print("start date:" + start_date_updated)

     # update end date
     end_date_updated = end_date_picker.value
     print("end date:" + end_date_updated)

     # update buoy number
     buoy_input_updated = buoy_input.value
     print("buoy ID:" + buoy_input_updated)

    # dropdown_updated = dropdown.value
     #print("dropdown value: " + dropdown_updated)

     # find new source data
     source_updated = find_dataset(buoy_input = buoy_input_updated,
                                   start_date = start_date_updated,
                                   end_date = end_date_updated)

     # update source data
     source.data = dict(source_updated.data)

# ------------------------------------------------------------------------------
# Widget: Text Input for Buoy Number
# ------------------------------------------------------------------------------
buoy_input = TextInput(value='44066', title="Buoy ID Number", name="buoy_input")
buoy_input.on_change("value", update_plot)

#dropdown = Select(title="Select a Buoy", value="Select", options=buoys, name="buoy_input")
#dropdown.on_change("value", update_plot)

# ------------------------------------------------------------------------------
# Widget: Data Table
# ------------------------------------------------------------------------------
formatter = NumberFormatter(format='0.000')

columns = [
    TableColumn(field="time", title="Time", formatter=DateFormatter()),
    TableColumn(field="air_temperature", title="Air Temperature (°C)", formatter=formatter),
    TableColumn(field="sea_surface_temperature", title="Sea Surface Temperature (°C)", formatter=formatter),
    TableColumn(field="dewpt_temperature", title="Dew Point Temperature (°C)", formatter=formatter),
    TableColumn(field="air_pressure", title="Air Pressure (hPa)", formatter=formatter),
    TableColumn(field="mean_wave_dir", title="Mean Wave Direction (degT)", formatter=formatter),
    TableColumn(field="wind_dir", title="Wind Direction (°C)", formatter=formatter),
    TableColumn(field="wind_spd", title="Wind Speed (m/s)", formatter=formatter),
    TableColumn(field="gust", title="Gust (m/s)", formatter=formatter),
]

# ------------------------------------------------------------------------------
# Widget: Date Pickers
# ------------------------------------------------------------------------------
start_date_picker = DatePicker(title='Start date', value='2021-07-24', name="start_date")
start_date_picker.on_change("value", update_plot)

end_date_picker = DatePicker(title='End date', value=date.today(), name="end_date")
end_date_picker.on_change("value", update_plot)

# ------------------------------------------------------------------------------
# Create Charts
# ------------------------------------------------------------------------------
#initial_checkbox_group = [checkbox_group.labels[i] for i in checkbox_group.active]

source = find_dataset(buoy_input = buoy_input.value,
                      start_date = start_date_picker.value,
                      end_date = end_date_picker.value)

p = make_temp_plot(source, buoy_input = buoy_input.value)
#p_wvpd = make_wvpd_plot(source, buoy_input = buoy_input.value)
p_dir = make_dir_plot(source, buoy_input = buoy_input.value)
#p_tide = make_tide_plot(source, buoy_input = buoy_input.value)
p_speed = make_speed_plot(source, buoy_input = buoy_input.value)
p_pressure = make_pressure_plot(source, buoy_input = buoy_input.value)

data_table = DataTable(source=source, columns=columns, height=280, name="data_table", sizing_mode="stretch_width")

# put controls in a single element
controls = row(buoy_input, start_date_picker, end_date_picker)

buoys = active_buoys(buoys)
bokeh_doc.template_variables["buoys"] = buoys

# Send variables to index.html for display
bokeh_doc.add_root(buoy_input)
bokeh_doc.add_root(start_date_picker)
bokeh_doc.add_root(end_date_picker)
bokeh_doc.add_root(p)
bokeh_doc.add_root(p_pressure)
bokeh_doc.add_root(p_dir)
bokeh_doc.add_root(p_speed)
#bokeh_doc.add_root(p_tide)
#bokeh_doc.add_root(p_wvpd)
bokeh_doc.add_root(data_table)

# Add page title
bokeh_doc.title = "OCG592 | Buoy Explore Tool"
