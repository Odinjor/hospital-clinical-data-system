from flask import Blueprint
from controllers.study_enrollment import search_study_enrollment, add_study_enrollment, delete_study_enrollment, update_study_enrollment

study_enrollment_bp = Blueprint('study_enrollment', __name__)

study_enrollment_bp.route('/study-enrollments', methods=['GET'])(search_study_enrollment)
study_enrollment_bp.route('/study-enrollments', methods=['POST'])(add_study_enrollment)
study_enrollment_bp.route('/study-enrollments/<int:enrollment_id>', methods=['PUT'])(update_study_enrollment)
study_enrollment_bp.route('/study-enrollments/<int:enrollment_id>', methods=['DELETE'])(delete_study_enrollment)