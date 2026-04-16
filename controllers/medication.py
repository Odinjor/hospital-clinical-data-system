from flask import jsonify, request
from models.medication import Medication

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def get_medications():
    try:
        medications = Medication.get_all_medications()
        return jsonify([
            [m.medication_id, m.drug_name, m.dosage, m.route]
            for m in medications
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_medication():
    try:
        drug_name = _get("drug_name")
        dosage = _get("dosage")
        route = _get("route")

        if not all([drug_name, dosage, route]):
            return jsonify({"error": "medication_id, drug_name, dosage, and route are required"}), 400

        medication = Medication.add_medication(drug_name, dosage, route)
        return jsonify([f"Medication_id: {medication.medication_id}, drug_name: {medication.drug_name}, dosage: {medication.dosage}, route: {medication.route}"]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_medication(medication_id):
    try:
        deleted = Medication.delete_medication(medication_id)
        if not deleted:
            return jsonify({"error": "Medication not found"}), 404
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_medication(medication_id):
    try:
        drug_name = _get("drug_name")
        dosage = _get("dosage")
        route = _get("route")

        updated = Medication.update_medication(
            medication_id,
            drug_name=drug_name,
            dosage=dosage,
            route=route
        )
        if not updated:
            return jsonify({"error": "No fields to update"}), 400
        return jsonify([f"Medication_id: {medication_id}, drug_name: {drug_name}, dosage: {dosage}, route: {route}"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def search_medication(medication_id):
    try:
        medication = Medication.search_medication(medication_id)
        if not medication:
            return jsonify({"error": "Medication not found"}), 404
        return jsonify([f"Medication_id: {medication.medication_id}, drug_name: {medication.drug_name}, dosage: {medication.dosage}, route: {medication.route}"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500