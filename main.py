import numpy as np
import xarray as xr
import pandas as pd

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, CDSView, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, TextInput, LabelSet
from bokeh.models.widgets import CheckboxGroup
from bokeh.io import show, curdoc
from bokeh.layouts import column, row, grid, WidgetBox
from datetime import date
from bokeh.palettes import Spectral4

bokeh_doc = curdoc()

# Order of opterations
# find_dataset()
# make_plot()
# filter_dataset()
# update_plot()
# find_dataset()
# filter_dataset()

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

def make_plot(source, buoy_input, checkbox_group):
    p = figure(plot_width = 700, plot_height = 700,
               x_axis_label = 'Time',
               x_axis_type = "datetime")

    # this needs to become a multiline plot?
    p.line(x='time', y='sea_surface_temperature', legend_label = "Sea Surface Temperature", source=source)
    p.line(x='time', y='air_temperature', legend_label = "Air Temperature", source=source)

    p.legend.click_policy = "hide"

    return p

def filter_dataset(source, checkbox_group):
    view = CDSView(source=source, filters=[IndexFilter([0,2,4])])
    # create one view that finds which checkboxes are checked, and displays that on the multiline chart

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

     source_updated = find_dataset(buoy_input = buoy_input_updated,
                                   start_date = start_date_updated,
                                   end_date = end_date_updated)

     source.data = dict(source_updated.data)
# ------------------------------------------------------------------------------
# Widget creation and customization
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Widget: Text Input
# ------------------------------------------------------------------------------
buoy_input = TextInput(value='44066', title="Buoy ID Number")
buoy_input.on_change("value", update_plot)

# ------------------------------------------------------------------------------
# Widget: Data Table
# ------------------------------------------------------------------------------
columns = [
    TableColumn(field="time", title="Time", formatter=DateFormatter()),
    TableColumn(field="wind_dir", title="Wind Direction"),
    TableColumn(field="wind_spd", title="Wind Speed"),
    TableColumn(field="gust", title="Gust"),
    TableColumn(field="wave_height", title="Wave Height"),
    TableColumn(field="dominant_wpd", title="Dominant Wave Period"),
    TableColumn(field="average_wpd", title="Average Wave Period"),
    TableColumn(field="mean_wave_dir", title="Mean Wave Direction"),
    TableColumn(field="air_pressure", title="Air Pressure"),
    TableColumn(field="air_temperature", title="Air Temperature"),
    TableColumn(field="sea_surface_temperature", title="Sea Surface Temperature"),
    TableColumn(field="dewpt_temperature", title="Dew Point Temperature"),
    TableColumn(field="visibility", title="Visibility"),
    TableColumn(field="water_level", title="Water Level"),
]

# ------------------------------------------------------------------------------
# Widget: Date Picker
# ------------------------------------------------------------------------------
start_date_picker = DatePicker(title='Start date', value='2021-07-24')
start_date_picker.on_change("value", update_plot)

end_date_picker = DatePicker(title='End date', value=date.today())
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

#labels = LabelSet(x='Time', title="Buoy # " + buoy_input.value, source=source)

p = make_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)
data_table = DataTable(source=source, columns=columns, width=1400, height=280)

# put controls in a single element
controls = column(start_date_picker, end_date_picker, buoy_input, checkbox_group)

# create a row layout
layout = row(controls, p)

# make a tab with the layout
#tab = Panel(child=layout, title="Buoy Data")
#tabs = Tabs(tabs=[tab])

# display everything
#bokeh_doc.add_root(tabs)

# show all widgets and graphs on the page
#bokeh_doc.add_root(start_date_picker)
#bokeh_doc.add_root(end_date_picker)
#bokeh_doc.add_root(buoy_input)
#bokeh_doc.add_root(checkbox_group)
#bokeh_doc.add_root(p)
#bokeh_doc.add_root(data_table)
bokeh_doc.add_root(layout)
bokeh_doc.add_root(data_table)
bokeh_doc.title = "Buoy Interactive Tool"

#src = ColumnDataSource(data=dict(
#    xs=[[1,2,3], [1,3,4], [2, 3, 4]],
#    ys=[[1,3,2], [5,4,3], [9, 8, 9]],
#    alpha=[1, 1, 1]
#))

#p = figure(y_range=(0, 10))
#p.multi_line("xs", "ys", line_alpha="alpha", line_width=3, source=src)

#cb = CheckboxGroup(labels=["L0", "L1", "L2"], active=[0, 1, 2])

#def update(attr, old, new):
    # you'll have to supply logic to determine which indices to "show" and
    # which to "hide" based on checkbox according to your actual situation
#    src.data["alpha"] = [int(i in cb.active) for i in range(len(cb.labels))]

#cb.on_change('active', update)

#curdoc().add_root(row(p, cb))
