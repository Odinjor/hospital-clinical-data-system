from flask import Blueprint
from controllers.diagnosis import get_diagnosis_by_encounter, add_diagnosis, delete_diagnosis, update_diagnosis

diagnosis_bp = Blueprint('diagnosis', __name__)

diagnosis_bp.route('/diagnosis/encounter/<int:encounter_id>', methods=['GET'])(get_diagnosis_by_encounter)
diagnosis_bp.route('/diagnosis', methods=['POST'])(add_diagnosis)
diagnosis_bp.route('/diagnosis/<int:diagnosis_id>', methods=['DELETE'])(delete_diagnosis)
diagnosis_bp.route('/diagnosis/<int:diagnosis_id>', methods=['PUT'])(update_diagnosis)