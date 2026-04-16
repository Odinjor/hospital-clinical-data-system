from flask import jsonify, request
from models.encounters import Encounter

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def get_encounter_by_patient(patient_id):
    try:
        encounter = Encounter.search_encounter_by_patient(patient_id)
        if not encounter:
            return jsonify({"error": "Encounter not found"}), 404
        return jsonify([encounter.encounter_id, encounter.patient_id, encounter.dept_id, str(encounter.encounter_date) if encounter.encounter_date else None]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_encounter():
    try:
        patient_id = _get("patient_id")
        dept_id = _get("dept_id")
        encounter_date = _get("encounter_date")
        discharge_date = _get("discharge_date")
        encounter_type = _get("encounter_type")

        if not all([patient_id, dept_id, encounter_date]):
            return jsonify({"error": "patient_id, dept_id, and encounter_date are required"}), 400

        new_encounter = Encounter.add_encounter(patient_id, dept_id, encounter_date, discharge_date, encounter_type)
        return jsonify([f"Encounter_id: {new_encounter.encounter_id}, Patient_id: {new_encounter.patient_id}, Dept_id: {new_encounter.dept_id}, Encounter_date: {new_encounter.encounter_date}"]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_encounter(encounter_id):
    try:
        deleted = Encounter.delete_encounter(encounter_id)
        if not deleted:
            return jsonify({"error": "Encounter not found"}), 404
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_encounter(encounter_id):
    try:
        patient_id = _get("patient_id")
        dept_id = _get("dept_id")
        encounter_date = _get("encounter_date")
        discharge_date = _get("discharge_date")
        encounter_type = _get("encounter_type")

        updated = Encounter.update_encounter(
            encounter_id,
            patient_id=patient_id,
            dept_id=dept_id,
            encounter_date=encounter_date,
            discharge_date=discharge_date,
            encounter_type=encounter_type
        )
        if not updated:
            return jsonify({"error": "No fields to update"}), 400
        return jsonify([f"Encounter_id: {updated.encounter_id}, Patient_id: {updated.patient_id}, Dept_id: {updated.dept_id}, Encounter_date: {updated.encounter_date}, Discharge_date: {updated.discharge_date}, Encounter_type: {updated.encounter_type}"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def list_all_encounters():
    try:
        encounters = Encounter.list_all_encounters()
        return jsonify([
            [e.encounter_id, e.patient_id, e.dept_id, str(e.encounter_date) if e.encounter_date else None, str(e.discharge_date) if e.discharge_date else None, e.encounter_type]
            for e in encounters
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500