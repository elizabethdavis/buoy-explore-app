# imports
import xarray as xr
import matplotlib.pyplot as plt
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def search():
    if request.method == "POST":
        buoy_id = request.form.get("buoy_id")
        return buoy_id
    return render_template('index.html')

# create URL with buoy ID number
def create_URL(buoy_id):
    url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/ + str(buoy_id) + / + str(buoy_id) + .ncml'
    return url

# print Buoy ID and Buoy URL
def main(buoy_id, url):
    # find_ID = search()
    print('The buoy URL is' + url)

if __name__ == '__main__':
    app.run(debug=True)
