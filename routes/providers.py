from flask import Blueprint
from controllers.providers import get_all_providers, get_provider_by_id, get_providers_with_department, add_provider, delete_provider, update_provider

providers_bp = Blueprint('providers', __name__)

providers_bp.route('/providers', methods=['GET'])(get_all_providers)
providers_bp.route('/providers/<int:provider_id>', methods=['GET'])(get_provider_by_id)
providers_bp.route('/providers/department/<int:department_id>', methods=['GET'])(get_providers_with_department)
providers_bp.route('/providers', methods=['POST'])(add_provider)
providers_bp.route('/providers/<int:provider_id>', methods=['PUT'])(update_provider)
providers_bp.route('/providers/<int:provider_id>', methods=['DELETE'])(delete_provider)

