from flask import jsonify, request
from models.providers import Provider

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)
def get_all_providers():
    try:
        providers = Provider.get_all_providers()
        return jsonify([
            [p.provider_id, p.specialty, p.role, p.dept_id]
            for p in providers
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_provider_by_id(provider_id):
    try:
        provider = Provider.get_provider_by_id(provider_id)
        if not provider:
            return jsonify({"error": "Provider not found"}), 404
        return jsonify([provider.provider_id, provider.specialty, provider.role, provider.dept_id]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def add_provider():
    try:
        specialty = _get("specialty")
        role = _get("role")
        dept_id = _get("department_id")

        if not all([specialty, role, dept_id]):
            return jsonify({"error": "specialty, role, and department_id are required"}), 400
        provider = Provider.add_provider(specialty, role, dept_id)
        return jsonify([
            f"provider_id: {provider.provider_id}, specialty: {provider.specialty}, role: {provider.role}, dept_id: {provider.dept_id}"
        ]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_provider(provider_id):
    try:
        specialty = _get("specialty")
        role      = _get("role")
        dept_id   = _get("dept_id")

        if not any([specialty, role, dept_id]):
            return jsonify({"error": "At least one field required to update"}), 400

        updated = Provider.update_provider(
            provider_id,
            specialty = specialty,
            role      = role,
            dept_id   = dept_id
        )

        if not updated:
            return jsonify({"error": "No fields were updated"}), 400

        return jsonify({"updated": True, "provider_id": provider_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def delete_provider(provider_id):
    try:
        Provider.delete_provider(provider_id)
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_providers_with_department(department_id):
    try:
        providers = Provider.get_providers_with_department(department_id)
        return jsonify([
            [p.provider_id, p.specialty, p.role, p.dept_id]
            for p in providers
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
