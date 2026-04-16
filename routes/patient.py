from flask import Blueprint
from controllers.patient import search_patient, add_patient, delete_patient, update_patient, create_patient_report, get_all_patients

patients_bp = Blueprint('patients', __name__)

patients_bp.route('/patients/<int:patient_id>', methods=['GET'])(search_patient)
patients_bp.route('/patients', methods=['POST'])(add_patient)
patients_bp.route('/patients', methods=['GET'])(get_all_patients)
patients_bp.route('/patients/<int:patient_id>/report', methods=['GET'])(create_patient_report)  
patients_bp.route('/patients/<int:patient_id>', methods=['PUT'])(update_patient)
patients_bp.route('/patients/<int:patient_id>', methods=['DELETE'])(delete_patient)