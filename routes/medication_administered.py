from flask import Blueprint
from controllers.medication_administered import search_medication_administered, add_medication_administered, delete_medication_administered, update_medication_administered

medication_administered_bp = Blueprint('medication_administered', __name__)

medication_administered_bp.route('/medication-administered', methods=['GET'])(search_medication_administered)
medication_administered_bp.route('/medication-administered', methods=['POST'])(add_medication_administered)
medication_administered_bp.route('/medication-administered/<int:administered_medication_id>', methods=['PUT'])(update_medication_administered)
medication_administered_bp.route('/medication-administered/<int:administered_medication_id>', methods=['DELETE'])(delete_medication_administered)