from flask import Blueprint
from controllers.study import get_all_studies, search_study, add_study, delete_study, update_study

study_bp = Blueprint('study', __name__)

study_bp.route('/studies', methods=['GET'])(get_all_studies)
study_bp.route('/studies/<int:study_id>', methods=['GET'])(search_study)
study_bp.route('/studies', methods=['POST'])(add_study)
study_bp.route('/studies/<int:study_id>', methods=['PUT'])(update_study)
study_bp.route('/studies/<int:study_id>', methods=['DELETE'])(delete_study)