from flask import Flask, render_template, request
#from database import database

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html')


@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/analyze', methods=['POST'])
def analyze_search():
        # use request to store form contents
        car_make = request.form.get('make')
        car_model = request.form.get('model')

        car_listing = request.form.get('listing_text')
        car_carfax = request.form.get('carfax_text')

        # cast to int since form sends strings
        car_year = int(request.form.get('year'))

        print(f"user searched for: {car_year} {car_make} {car_model}\nListing Text:\n{car_listing}\nCarfax Text\n{car_carfax}")

        return "<p>searching...</p>"

@app.route('/deb')
def video_page():
    return render_template('video_page.html')