from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///earthquakes.db'
db = SQLAlchemy(app)

# Define the model for the Earthquake data
class Earthquake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(20))
    jam = db.Column(db.String(20))
    lintang = db.Column(db.String(20))
    bujur = db.Column(db.String(20))
    kedalaman = db.Column(db.String(20))
    magnitude = db.Column(db.String(10))
    wilayah = db.Column(db.String(100))

# Explicitly create the tables
with app.app_context():
    db.create_all()

from datetime import datetime

from datetime import datetime

@app.route('/')
def index():
    # Fetch JSON data from the given URL
    url = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
    response = requests.get(url)
    data = response.json()

    # Check the actual structure of the JSON data
    if "Infogempa" in data and "gempa" in data["Infogempa"]:
        earthquakes_data = data["Infogempa"]["gempa"]
    else:
        # Handle the case where the structure is different
        earthquakes_data = []

    # Iterate through the fetched earthquakes data
    for earthquake_data in earthquakes_data:
        # Check if the earthquake with the same date and time already exists in the database
        existing_earthquake = Earthquake.query.filter_by(
            tanggal=earthquake_data["Tanggal"],
            jam=earthquake_data["Jam"]
        ).first()

        if existing_earthquake:
            # Update the existing entry if needed (you can customize this part based on your requirements)
            existing_earthquake.lintang = earthquake_data["Lintang"]
            existing_earthquake.bujur = earthquake_data["Bujur"]
            existing_earthquake.kedalaman = earthquake_data["Kedalaman"]
            existing_earthquake.magnitude = earthquake_data["Magnitude"]
            existing_earthquake.wilayah = earthquake_data["Wilayah"]
        else:
            # Add a new entry if the earthquake doesn't exist in the database
            new_earthquake = Earthquake(
                tanggal=earthquake_data["Tanggal"],
                jam=earthquake_data["Jam"],
                lintang=earthquake_data["Lintang"],
                bujur=earthquake_data["Bujur"],
                kedalaman=earthquake_data["Kedalaman"],
                magnitude=earthquake_data["Magnitude"],
                wilayah=earthquake_data["Wilayah"]
            )
            db.session.add(new_earthquake)

    # Commit the changes to the database
    db.session.commit()

    # Print the number of earthquakes added or updated (for debugging)
    print(f"Number of earthquakes added or updated: {len(earthquakes_data)}")

    # Print the number of earthquakes in the database (for debugging)
    print(f"Number of earthquakes in the database: {Earthquake.query.count()}")

    # Print the earthquakes fetched from the database (for debugging)
    print("Earthquakes in the database:")
    for earthquake in Earthquake.query.all():
        print(earthquake.id, earthquake.tanggal, earthquake.jam, earthquake.lintang, earthquake.bujur, earthquake.kedalaman, earthquake.magnitude, earthquake.wilayah)

    # Render the HTML template and pass the earthquake data to it
    return render_template('index.html', earthquakes=Earthquake.query.all())



if __name__ == '__main__':
    app.run(debug=True)
