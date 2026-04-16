from flask import jsonify, request
from models.medication_administered import MedicationAdministered

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def search_medication_administered(encounter_id):
    try:
        medications_administered = MedicationAdministered.search_medication_administered(encounter_id)
        return jsonify([
            [m.admin_id, m.encounter_id, m.provider_id, m.medication_id, str(m.administered_at) if m.administered_at else None]
            for m in medications_administered
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def add_medication_administered():
    try:
        encounter_id = _get("encounter_id")
        provider_id = _get("provider_id")
        medication_id = _get("medication_id")
        administered_at = _get("administered_at")

        if not all([encounter_id, provider_id, medication_id, administered_at]):
            return jsonify({"error": "encounter_id, provider_id, medication_id, and administered_at are required"}), 400

        ma = MedicationAdministered.add_medication_administered(encounter_id, provider_id, medication_id, administered_at)
        return jsonify([f"Admin_id: {ma.admin_id}, encounter_id: {ma.encounter_id}, provider_id: {ma.provider_id}, medication_id: {ma.medication_id}, administered_at: {ma.administered_at}"]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_medication_administered(encounter_id):
    try:
        deleted = MedicationAdministered.delete_medication_administered(encounter_id)
        if not deleted:
            return jsonify({"error": "Medication administration record not found"}), 404
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_medication_administered(encounter_id):
    try:
        provider_id = _get("provider_id")
        medication_id = _get("medication_id")
        administered_at = _get("administered_at")

        updated = MedicationAdministered.update_medication_administered(
            encounter_id,
            provider_id=provider_id,
            medication_id=medication_id,
            administered_at=administered_at
        )
        if not updated:
            return jsonify({"error": "Medication administration record not found or no fields to update"}), 404
        return jsonify([f"Admin_id: {updated.admin_id}, encounter_id: {updated.encounter_id}, provider_id: {updated.provider_id}, medication_id: {updated.medication_id}, administered_at: {updated.administered_at}"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
