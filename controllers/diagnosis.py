from flask import jsonify, request
from models.diagnosis import Diagnosis

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def get_diagnosis_by_encounter(encounter_id):
    try:
        diagnoses = Diagnosis.get_diagnosis_by_encounter(encounter_id)
        return jsonify([
            [d.diagnosis_id, d.encounter_id, d.icd10_code, d.diagnosis_description]
            for d in diagnoses
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def add_diagnosis():
    try:
        encounter_id = _get("encounter_id")
        icd10_code = _get("icd10_code")
        diagnosis_description = _get("diagnosis_description")

        if not all([encounter_id, icd10_code]):
            return jsonify({"error": "encounter_id and icd10_code are required"}), 400

        diagnosis = Diagnosis.add_diagnosis(encounter_id, icd10_code, diagnosis_description)
        return jsonify([f"Diagnosis_id: {diagnosis.diagnosis_id}, Encounter_id: {diagnosis.encounter_id}, icd10_id: {diagnosis.icd10_code}, Diagnosis_id: {diagnosis.diagnosis_description}"]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_diagnosis(diagnosis_id):
    try:
        deleted = Diagnosis.delete_diagnosis(diagnosis_id)
        if not deleted:
            return jsonify({"error": "Diagnosis not found"}), 404
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_diagnosis(diagnosis_id):
    try:
        encounter_id = _get("encounter_id")
        icd10_code = _get("icd10_code")
        diagnosis_description = _get("diagnosis_description")

        updated = Diagnosis.update_diagnosis(
            diagnosis_id,
            encounter_id=encounter_id,
            icd10_code=icd10_code,
            diagnosis_description=diagnosis_description
        )
        if not updated:
            return jsonify({"error": "No fields to update"}), 400
        return jsonify([f"Diagnosis_id: {updated.diagnosis_id}, Encounter_id: {updated.encounter_id}, icd10_id: {updated.icd10_code}, Diagnosis_id: {updated.diagnosis_description}"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
