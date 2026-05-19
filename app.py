from flask import Flask, render_template, request, redirect, url_for
from database import database
from services import ai_agent as ai
import json
import uuid

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('search.html')


@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/analyze', methods=['POST'])
def analyze_search():
    # grab inputs and sanitize strings
    car_make = request.form.get('make', '').strip()
    car_model = request.form.get('model', '').strip()
    car_listing = request.form.get('listing_text', '').strip()
    car_carfax = request.form.get('carfax_text', '').strip()

    # parse int from year
    try:
        car_year = int(request.form.get('year', 0))
    except ValueError:
        return "Error, year invalid", 400
        
    # grab vehicle id and handle cars not in db
    vehicle_id = database.getVehicleID(car_year, car_make, car_model)
    if not vehicle_id:
        return f"Error: {car_year} {car_make} {car_model} is not supported in the database", 404

    # implement search save logic !!!
    search_uuid = str(uuid.uuid4())

    database.create_search(
       uuid=search_uuid,
       make=car_make,
       model=car_model,
       year=car_year,
       listing=car_listing,
       carfax=car_carfax 
    )

    return redirect(url_for('hello_world', search_uuid=search_uuid))


@app.route('/deb')
def video_page():
    return render_template('video_page.html')