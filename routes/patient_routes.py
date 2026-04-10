from flask import Blueprint, request, render_template, redirect
from models.db import execute_query

patients_bp = Blueprint("patients", __name__)

patients_bp.route("/patients")
def list_patients():
    query = "SELECT * FROM Patient"
    result = execute_query(query, fetch=True)
    return render_template("patients.html", patients=result)

@patients_bp.route("/patients/search")
def search_patient():
    patient_id = request.args.get("patient_id")

    query = "SELECT * FROM Patient WHERE patient_id = %s"
    result = execute_query(query, (patient_id,))

    return render_template("patients.html", patients=result)

@patients_bp.route("/patients/add", methods=["POST"])
def add_patient():
    dob = request.form["dob"]
    sex = request.form["sex"]
    ethnicity = request.form["ethnicity"]

    query = """ 
    INSERT INTO Patient (dob, sex, ethnicity, created_at)
    VALUES (%s, %s, %s, CURDATE())
    """
    execute_query(query, (dob, sex, ethnicity))
    return redirect("/patients")

@patients_bp.route("/patients/delete/<int:patient_id>")
def delete_patient(patient_id):
    query = "DELETE FROM Patient WHERE patient_id = %s"
    execute_query(query, (patient_id,))
    return redirect("/patients")

@patients_bp.route("/patients/update/<int:patient_id>", methods=["POST"])
def update_patient(patient_id):
    dob = request.form["dob"]
    sex = request.form["sex"]
    ethnicity = request.form["ethnicity"]

    query = """ 
    UPDATE Patient 
    SET dob = %s, sex = %s, ethnicity = %s 
    WHERE patient_id = %s
    """
    execute_query(query, (dob, sex, ethnicity, patient_id))
    return redirect("/patients")