from flask import request, jsonify
from models.study_enrollment import StudyEnrollment

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def add_study_enrollment():
    try:
        patient_id = _get('patient_id')
        study_id = _get('study_id')
        consent_date = _get('consent_date')
        enrollment_status = _get('enrollment_status')

        if not all([patient_id, study_id, consent_date, enrollment_status]):
            return jsonify({"error": "Missing required fields"}), 400
        
        study_enrollment = StudyEnrollment.add_study_enrollment(patient_id, study_id, consent_date, enrollment_status)
        return jsonify([f"patient_id: {study_enrollment.patient_id}, study_id: {study_enrollment.study_id}, consent_date: {study_enrollment.consent_date}, enrollment_status: {study_enrollment.enrollment_status}"]), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def search_study_enrollment(patient_id):
    try:
        enrollment = StudyEnrollment.search_study_enrollment(patient_id)
        if enrollment:
            return jsonify(enrollment), 200
        else:
            return jsonify({"error": "Study enrollment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_study_enrollment(patient_id):
    try:
        StudyEnrollment.delete_study_enrollment(patient_id)
        return jsonify({"message": "Study enrollment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_study_enrollment(patient_id):
    try:
        study_id = _get('study_id')
        consent_date = _get('consent_date')
        enrollment_status = _get('enrollment_status')

        if not any([study_id, consent_date, enrollment_status]):
            return jsonify({"error": "At least one field must be provided for update"}), 400

        success = StudyEnrollment.update_study_enrollment(patient_id, study_id, consent_date, enrollment_status)
        if success:
            return jsonify({"message": "Study enrollment updated successfully"}), 200
        else:
            return jsonify({"error": "No fields to update or study enrollment not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500