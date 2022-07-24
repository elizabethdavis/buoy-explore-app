import numpy as np
import xarray as xr
import pandas as pd

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, TextInput
from bokeh.models.widgets import CheckboxGroup
from bokeh.io import show, curdoc
from bokeh.layouts import column, row, grid, WidgetBox
from datetime import date

bokeh_doc = curdoc()

# ------------------------------------------------------------------------------
# Function: load dataset
# ------------------------------------------------------------------------------
#def get_dataset():
#    data = xr.open_dataset('https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/44025/44025.ncml')
#    data = data.sel(time=slice('2019-01-01', '2020-01-01'))
#    df = data.to_dataframe().reset_index().set_index('time')
#    source = ColumnDataSource(df)

#    return source

def make_dataset(buoy_input, checkbox_group, start_date, end_date):

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
               title = 'Plot for Buoy #' + buoy_input,
               x_axis_label = 'Time')

    for i in checkbox_group:
        print("labels: " + i)

    print("Generating plot for buoy # " + buoy_input)

    # this needs to become a multiline plot
    p.line(x='time', y=checkbox_group[0], source=source)

    return p

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

     source_updated = make_dataset(buoy_input = buoy_input_updated,
                                   checkbox_group = checkbox_group_updated,
                                   start_date = start_date_updated,
                                   end_date = end_date_updated)

     # i think this is the problem child for not updating the plot
     source.data.update(source_updated.data)
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

#data_table = DataTable(source=source, columns=columns, width=1400, height=280)

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

source = make_dataset(buoy_input = buoy_input.value,
                      checkbox_group = initial_checkbox_group,
                      start_date = start_date_picker.value,
                      end_date = end_date_picker.value)

p = make_plot(source, buoy_input = buoy_input.value, checkbox_group=initial_checkbox_group)

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
