from flask import request

def get_field(key):
    """Safely read a field from form data or JSON body."""
    if request.content_type and 'application/json' in request.content_type:
        body = request.get_json(silent=True)
        return body.get(key) if body else None
    return request.form.get(key)