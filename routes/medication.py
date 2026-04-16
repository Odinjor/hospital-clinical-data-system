from flask import Blueprint
from controllers.medication import get_medications, add_medication, delete_medication, update_medication

medications_bp = Blueprint('medications', __name__)

medications_bp.route('/medications', methods=['GET'])(get_medications)
medications_bp.route('/medications', methods=['POST'])(add_medication)  
medications_bp.route('/medications/<int:medication_id>', methods=['PUT'])(update_medication)
medications_bp.route('/medications/<int:medication_id>', methods=['DELETE'])(delete_medication)