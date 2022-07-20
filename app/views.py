from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import itertools
import xarray as xr
import matplotlib.pyplot as plt

views = Blueprint('views', __name__)

# Function: Get buoy information from homepage
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        buoyID = request.form.get('buoy_id')
        checkbox_data = request.form.getlist('checkbox_data')
        session["params"] = checkbox_data

        return redirect(url_for('views.find_buoy', buoy_id=buoyID))

    return render_template('index.html')

# Function: create url to pull data from
def create_url(buoy_id):
    url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/' + buoy_id + '/' + buoy_id + '.ncml'

    return url

# Function: Find Buoy and print results to page
@views.route('/results/<buoy_id>')
def find_buoy(buoy_id):
    url = create_url(buoy_id)
    checkbox_data = session["params"]

    data = xr.open_dataset(url)
    ds = data.sel(time=slice('2021-01-01', '2022-01-01'))
    df = ds.to_dataframe()

#    print(df.columns)
#    print(df.head())
#    df.sea_surface_temperature.plot()
#    air_temp = data.air_temperature

    return render_template('results.html', buoy_id=buoy_id, checkbox_data=checkbox_data, url=url)
