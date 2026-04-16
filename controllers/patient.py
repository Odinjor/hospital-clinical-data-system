from flask import jsonify, request
from models.patient import Patient

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def get_all_patients():
    try:
        patients = Patient.get_all_patients()
        return jsonify([
            [p.patient_id, str(p.dob) if p.dob else None, p.sex, p.ethnicity]
            for p in patients
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def search_patient(patient_id):
    try:
        patient = Patient.search_patient(patient_id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify([patient.patient_id, str(patient.dob) if patient.dob else None, patient.sex, patient.ethnicity]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_patient():
    try:
        # Try form data first, then JSON
        dob = _get("dob")
        sex = _get("sex")
        ethnicity = _get("ethnicity")

        if not all([dob, sex, ethnicity]):
            return jsonify({"error": "dob, sex, and ethnicity are required"}), 400

        patient = Patient.add_patient(dob, sex, ethnicity)
        return jsonify([f"Patient_id: {patient.patient_id}", str(patient.dob) if patient.dob else None, patient.sex, patient.ethnicity]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_patient(patient_id):
    try:
        # Try form data first, then JSON
        dob = _get("dob")
        sex = _get("sex")
        ethnicity = _get("ethnicity")

        updated = Patient.update_patient(
            patient_id,
            dob=dob,
            sex=sex,
            ethnicity=ethnicity
        )
        if not updated:
            return jsonify({"error": "No fields to update"}), 400

        return jsonify({"updated": True, "patient_id": patient_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_patient(patient_id):
    try:
        Patient.delete_patient(patient_id)
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def create_patient_report(patient_id):
    try:
        report = Patient.create_patient_report(patient_id)

        if not report:
            return jsonify({"error": "Patient not found or no data available"}), 404

        # report is a dict with patient, encounters, diagnoses, medications, observations
        return jsonify({
            "patient_id":   report["patient"].patient_id,
            "dob":          str(report["patient"].dob) if report["patient"].dob else None,
            "sex":          report["patient"].sex,
            "ethnicity":    report["patient"].ethnicity,
            "encounters":   [e.to_dict() for e in report["encounters"]],
            "diagnoses":    [d.to_dict() for d in report["diagnoses"]],
            "medications":  [m.to_dict() for m in report["medications"]],
            "observations": [o.to_dict() for o in report["observations"]]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500