from flask import request, jsonify
from models.study import Study

def _get(key, alt_key=None):
    """Pull a field from form data or JSON, whichever was sent. Also check alternate field names."""
    if request.content_type and 'application/json' in request.content_type:
        data = request.get_json(silent=True, force=True)
        if data:
            return data.get(key) or (data.get(alt_key) if alt_key else None)
        return None
    return request.form.get(key) or (request.form.get(alt_key) if alt_key else None)

def get_all_studies():
    try:
        studies = Study.get_all_studies()
        if not studies:
            return jsonify([]), 200
        return jsonify([
            [s.study_id, s.study_name, str(s.start_date) if s.start_date else None, str(s.end_date) if s.end_date else None, s.principal_investigator]
            for s in studies
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def search_study(study_id):
    try:
        study = Study.search_study(study_id)
        if not study:
            return jsonify({"error": "Study not found"}), 404
        return jsonify([study.study_id, study.study_name, str(study.start_date) if study.start_date else None, str(study.end_date) if study.end_date else None, study.principal_investigator]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def add_study():
    try:
        study_name = _get("study_name", "study_title")
        start_date = _get("start_date")
        end_date = _get("end_date")
        principal_investigator = _get("principal_investigator", "investigator")

        if not all([study_name, start_date, end_date, principal_investigator]):
            return jsonify({"error": "study_name/study_title, start_date, end_date, and principal_investigator/investigator are required"}), 400

        study = Study.add_study(study_name, start_date, end_date, principal_investigator)
        return jsonify([f"study_id: {study.study_id}, study_name: {study.study_name}, start_date: {study.start_date}, end_date: {study.end_date}, principal_investigator: {study.principal_investigator}"]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_study(study_id):
    try:
        deleted = Study.delete_study(study_id)
        if not deleted:
            return jsonify({"error": "Study not found"}), 404
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_study(study_id):
    try:
        study_name = _get("study_name")
        start_date = _get("start_date")
        end_date = _get("end_date")
        principal_investigator = _get("principal_investigator")

        updated = Study.update_study(
            study_id,
            study_name=study_name,
            start_date=start_date,
            end_date=end_date,
            principal_investigator=principal_investigator
        )
        if not updated:
            return jsonify({"error": "No fields to update"}), 400
        return jsonify({"updated": True, "study_id": study_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
