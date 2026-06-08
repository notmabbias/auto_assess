from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    car_make = request.form.get('make', '').strip().lower()
    car_model = request.form.get('model', '').strip().lower()
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

    search_uuid = str(uuid.uuid4())

    database.create_pending_search(
       uuid=search_uuid,
       make=car_make,
       model=car_model,
       year=car_year,
       listing=car_listing,
       carfax=car_carfax 
    )

    return redirect(url_for('loading', search_uuid=search_uuid))

@app.route('/loading/<search_uuid>', methods=['GET'])
def loading(search_uuid):
    return render_template('loading.html', search_uuid=search_uuid)

@app.route('/process/<search_uuid>', methods=['POST'])
def process_search(search_uuid):

    search_record = database.get_pending_search(search_uuid)
    if not search_record:
        # lazy error handling, but works
        return jsonify({"status": "error", "message": "Target session token expired or invalid."}), 404
    
    # grab data on vehicle from db to send to ai
    vehicle_id = database.getVehicleID(
        search_record['input_year'], 
        search_record['input_make'], 
        search_record['input_model']
    )
    vehicle_information = database.getInformation(vehicle_id)

    result = ai.analyze_vehicle(
        vehicle_information, 
        search_record['raw_ad_text'], 
        search_record['raw_carfax_text'],
        vehicle_id
    )

    # save ai into saved results
    database.save_ai_result(search_uuid, json.dumps(result))

    return jsonify({"status":"success"})

@app.route('/results/<search_uuid>', methods=['GET'])
def view_results(search_uuid):
    # retrieve finalized analysis 
    search_record = database.get_pending_search(search_uuid)
    if not search_record or not search_record['ai_analysis_json']:
        return redirect(url_for('search'))
        
    analysis_data = json.loads(search_record['ai_analysis_json'])
    return render_template('results.html', result=analysis_data)


@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve_search():
    error = None
    if request.method == 'POST':
        search_uuid = request.form.get('uuid', '').strip()
        
        # check if the UUID exists in the database
        record = database.get_pending_search(search_uuid)
        
        # verify the record exists and the AI actually completed the JSON generation
        if record and record['ai_analysis_json'] and record['ai_analysis_json'] != '{}':
            return redirect(url_for('view_results', search_uuid=search_uuid))
        else:
            error = "ERROR: Search ID not found or analysis incomplete."
            
    return render_template('retrieve.html', error=error)