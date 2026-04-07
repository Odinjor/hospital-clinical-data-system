from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="StarMan#4490",
    database="hospital_db"
)

@app.route("/")
def home():
    return "Hospital Dashboard Running"

@app.route("/patients")
def patients():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Patient")
    data = cursor.fetchall()
    return render_template("patients.html", patients=data)

@app.route("/encounters")
def encounters():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Encounter")
    data = cursor.fetchall()
    return render_template("encounters.html", encounters=data)

@app.route("/diagnosis")
def diagnosis():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Diagnosis")
    data = cursor.fetchall()
    return render_template("diagnosis.html", diagnosis=data)

@app.route("/observations")
def observations():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Observation")
    data = cursor.fetchall()
    return render_template("observations.html", observations=data)

if __name__ == "__main__":
    app.run(debug=True)