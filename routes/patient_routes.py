from flask import request, render_template
from app import app, db

@app.route("/patients/search")
def search_patient():
    patient_id = request.args.get("patient_id")

    query = "SELECT * FROM Patient WHERE patient_id = %s"
    result = execute_query(query, (patient_id,))

    return render_template("patients.html", patients=result)