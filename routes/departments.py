from flask import Blueprint
from controllers.departments import get_department_by_id, list_departments

departments_bp = Blueprint('departments', __name__)

departments_bp.route('/departments/<int:dept_id>', methods=['GET'])(get_department_by_id)
departments_bp.route('/departments', methods=['GET'])(list_departments)
