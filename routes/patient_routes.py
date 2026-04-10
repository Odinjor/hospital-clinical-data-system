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

@patients_bp.route("/patients/update/<int:patient_id>", methods=["GET", "POST"])
def update_patient(patient_id):
    if request.method == "POST":
        dob = request.form.get("dob")
        sex = request.form.get("sex")
        ethnicity = request.form.get("ethnicity")
    
        # Build dynamic query based on provided values
        updates = []
        params = []
        
        if patient_id:
            updates.append("patient_id = %s")
            params.append(patient_id)
        if dob:
            updates.append("dob = %s")
            params.append(dob)
        if sex:
            updates.append("sex = %s")
            params.append(sex)
        if ethnicity:
            updates.append("ethnicity = %s")
            params.append(ethnicity)
        
        if not updates:
            return redirect("/patients")  # No updates provided
        
        params.append(patient_id)
        query = f"UPDATE Patient SET {', '.join(updates)} WHERE patient_id = %s"
        execute_query(query, tuple(params))
        return redirect("/patients")
    else:
        query = "SELECT * FROM Patient WHERE patient_id = %s"
        result = execute_query(query, (patient_id,), fetch=True)
        return render_template("update_patient.html", patient=result[0])           

@patients_bp.route("/patients/<int:patient_id>/report")
def patient_report(patient_id):
    query = """ 
    SELECT e.encounter_id, d.icd10_code, p.role
    FROM Encounter e
    JOIN Diagnosis d ON e.encounter_id = d.encounter_id
    LEFT JOIN Medication_Administration m ON e.encounter_id = m.encounter_id
    LEFT JOIN Provider p ON m.provider_id = p.provider_id
    WHERE e.patient_id = %s

    """
    result = execute_query(query, (patient_id,), fetch=True)
    return render_template("patient_report.html", encounters=result)