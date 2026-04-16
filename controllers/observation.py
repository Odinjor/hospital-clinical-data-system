from flask import jsonify, request
from models.observations import Observation

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def search_observations(encounter_id):
    try:
        observations = Observation.search_observations(encounter_id)
        return jsonify([
            [o.observation_id, o.encounter_id, o.loinc_code, o.observation_type, o.value, o.unit, o.observed_at]
            for o in observations
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

def add_observation():
    try:
        encounter_id = _get("encounter_id")
        loinc_code = _get("loinc_code")
        observation_type = _get("observation_type")
        value = _get("value")
        unit = _get("unit")
        observed_at = _get("observed_at")

        if not all([encounter_id, loinc_code, observation_type, observed_at]):
            return jsonify({"error": "encounter_id, loinc_code, observation_type, and observed_at are required"}), 400

        observation = Observation.add_observation(encounter_id, loinc_code, observation_type, value, unit, observed_at)
        return jsonify([f"Observation_id: {observation.observation_id}, encounter_id: {observation.encounter_id}, loinc_code: {observation.loinc_code}, observation_type: {observation.observation_type}, value: {observation.value}, unit: {observation.unit}, observed_at: {observation.observed_at}"]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_observation(observation_id):
    try:
        deleted = Observation.delete_observation(observation_id)
        if not deleted:
            return jsonify({"error": "Observation not found"}), 404
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_observation(observation_id):
    try:
        encounter_id = _get("encounter_id")
        loinc_code = _get("loinc_code")
        observation_type = _get("observation_type")
        value = _get("value")
        unit = _get("unit")
        observed_at = _get("observed_at")

        updated = Observation.update_observation(
            observation_id,
            encounter_id=encounter_id,
            loinc_code=loinc_code,
            observation_type=observation_type,
            value=value,
            unit=unit,
            observed_at=observed_at
        )
        if not updated:
            return jsonify({"error": "No fields to update"}), 400
        return jsonify({"updated": True, "observation_id": observation_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

