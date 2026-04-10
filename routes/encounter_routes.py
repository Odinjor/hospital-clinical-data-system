from flask import Blueprint, request, render_template, redirect
from models.db import execute_query

encounters_bp = Blueprint("encounters", __name__)

@encounters_bp.route("/encounters")
def list_encounters():
    query = """ 
    SELECT * FROM Encounter e
    """
    result = execute_query(query, fetch=True)
    return render_template("encounters.html", data=result)

@encounters_bp.route("/encounters/add", methods=["POST"])
def add_encounter():
    patient_id = request.form["patient_id"]
    dept_id = request.form["dept_id"]
    encounter_type = request.form["encounter_type"]

    query = """ 
    INSERT INTO Encounter (patient_id, dept_id, encounter_date, encounter_type)
    VALUES (%s, %s, CURDATE(), %s)
    """
    execute_query(query, (patient_id, dept_id, encounter_type))
    return redirect("/encounters")

@encounters_bp.route("/encounters/update/<int:encounter_id>", methods=["GET", "POST"])
def update_encounter(encounter_id):
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        dept_id = request.form.get("dept_id")
        encounter_type = request.form.get("encounter_type")
        discharge_date = request.form.get("discharge_date")
        
        # Build dynamic query based on provided values
        updates = []
        params = []
        
        if patient_id:
            updates.append("patient_id = %s")
            params.append(patient_id)
        if dept_id:
            updates.append("dept_id = %s")
            params.append(dept_id)
        if encounter_type:
            updates.append("encounter_type = %s")
            params.append(encounter_type)
        if discharge_date:
            updates.append("discharge_date = %s")
            params.append(discharge_date)
        
        if not updates:
            return redirect("/encounters")  # No updates provided
        
        params.append(encounter_id)
        query = f"UPDATE Encounter SET {', '.join(updates)} WHERE encounter_id = %s"
        execute_query(query, tuple(params))
        return redirect("/encounters")
    else:
        query = "SELECT * FROM Encounter WHERE encounter_id = %s"
        result = execute_query(query, (encounter_id,), fetch=True)
        return render_template("update_encounter.html", encounter=result[0])
    
@encounters_bp.route("/encounters/search/<int:patient_id>")
def search_encounters(patient_id):
    query = """ 
    SELECT * FROM Encounter e
    WHERE e.patient_id = %s
    """
    result = execute_query(query, (patient_id,), fetch=True)
    return render_template("encounters.html", data=result)