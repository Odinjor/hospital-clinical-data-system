from flask import jsonify, request
from models.departments import Department

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)

def list_departments():
    try:
        departments = Department.get_all_departments()
        return jsonify([
            [dept.dept_id, dept.dept_name]
            for dept in departments
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_department_by_id(dept_id):
    try:
        department = Department.get_department_by_id(dept_id)
        if not department:
            return jsonify({"error": "Department not found"}), 404
        return jsonify([department.dept_id, department.dept_name]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500