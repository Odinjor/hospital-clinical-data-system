from flask import Blueprint
from controllers.encounters import get_encounter_by_patient, add_encounter, delete_encounter, update_encounter, list_all_encounters

encounters_bp = Blueprint('encounters', __name__)

encounters_bp.route('/encounters/patient/<int:patient_id>', methods=['GET'])(get_encounter_by_patient)
encounters_bp.route('/encounters', methods=['POST'])(add_encounter)
encounters_bp.route('/encounters/<int:encounter_id>', methods=['DELETE'])(delete_encounter)
encounters_bp.route('/encounters/<int:encounter_id>', methods=['PUT'])(update_encounter)
encounters_bp.route('/encounters', methods=['GET'])(list_all_encounters)

