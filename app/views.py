from flask import Blueprint, render_template, request, redirect, url_for, flash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        buoyID = request.form.get('buoy_id')
        print("Buoy ID: " + buoyID)
        return redirect(url_for('views.find_buoy', buoy_id=buoyID))
    return render_template('index.html')

@views.route('/results/<buoy_id>')
def find_buoy(buoy_id):
    return render_template('results.html', buoy_id=buoy_id)
