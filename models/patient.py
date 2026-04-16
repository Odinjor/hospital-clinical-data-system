from models.db import execute_query
from models.encounters     import Encounter
from models.diagnosis     import Diagnosis
from models.medication_administered    import MedicationAdministered
from models.observations   import Observation

class Patient:
    def __init__(self, patient_id=None, dob=None, sex=None, ethnicity=None, created_at=None):
        self.patient_id = patient_id
        self.dob = dob
        self.sex = sex
        self.ethnicity = ethnicity
        self.created_at = created_at

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "dob":        str(self.dob) if self.dob else None,
            "sex":        self.sex,
            "ethnicity":  self.ethnicity,
            "created_at": str(self.created_at) if self.created_at else None
        }
    
    @staticmethod
    def search_patient(patient_id):
        query = "SELECT * FROM Patient WHERE patient_id = %s"
        result = execute_query(query, (patient_id,), fetch=True)
        return Patient(int(result[0][0]), result[0][1], result[0][2], result[0][3], result[0][4]) if result else None

    @staticmethod
    def add_patient(dob, sex, ethnicity):
        query = """ 
        INSERT INTO Patient (dob, sex,  ethnicity, created_at)
        VALUES (%s, %s, %s, CURDATE())
        """
        execute_query(query, (dob, sex, ethnicity))
        
        
        result = execute_query("SELECT LAST_INSERT_ID()", fetch=True)
        new_id = result[0][0] if result else None
        return Patient(int(new_id), dob, sex, ethnicity)

    @staticmethod
    def delete_patient(patient_id):
        query = "DELETE FROM Patient WHERE patient_id = %s"
        execute_query(query, (patient_id,))
        return True
    
    @staticmethod
    def update_patient(patient_id, dob=None, sex=None, ethnicity=None):
        updates = []
        params = []
        
        if dob:
            updates.append("dob = %s")
            params.append(dob)
        if sex:
            updates.append("sex = %s")
            params.append(sex)
        if ethnicity:
            updates.append("ethnicity = %s")
            params.append(ethnicity)

        if not updates:
            return False

        params.append(patient_id)
        query = "UPDATE Patient SET " + ", ".join(updates) + " WHERE patient_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def get_all_patients():
        query = "SELECT * FROM Patient"
        result = execute_query(query, fetch=True)
        return [Patient(int(row[0]), row[1], row[2], row[3], row[4]) for row in result] if result else []
    
    @staticmethod
    def create_patient_report(patient_id):
        query = """
            SELECT p.patient_id, p.dob, p.sex, p.ethnicity,
                dd.dept_name, ma.provider_id,
                d.diagnosis_id, d.icd10_code, d.diagnosis_description, d.diagnosis_date,
                e.encounter_id, e.encounter_type, e.encounter_date, e.discharge_date,
                o.observation_id, o.loinc_code, o.observation_type,
                o.value, o.unit, o.observed_at,
                ma.admin_id, ma.medication_id, m.drug_name, m.dosage, m.route,
                ma.administered_at
            FROM Patient p
            LEFT JOIN Encounter e
                ON p.patient_id = e.patient_id
            LEFT JOIN Department dd
                ON e.dept_id = dd.dept_id
            LEFT JOIN Diagnosis d
                ON e.encounter_id = d.encounter_id
            LEFT JOIN Medication_Administration ma
                ON e.encounter_id = ma.encounter_id
            LEFT JOIN Medication m
                ON ma.medication_id = m.medication_id
            LEFT JOIN Observation o
                ON e.encounter_id = o.encounter_id
            WHERE p.patient_id = %s
        """
        rows = execute_query(query, (patient_id,), fetch=True)
        if not rows:
            return None

        first = rows[0]
        patient = Patient(first[0], first[1], first[2], first[3], None)

       

        encounters, diagnoses, medications, observations = {}, {}, {}, {}

        for row in rows:
            (pid, dob, sex, ethnicity, dept_name, provider_id,
            diag_id, icd10, diag_desc, diag_date,
            enc_id, enc_type, enc_date, disc_date,
            obs_id, loinc, obs_type, obs_val, obs_unit, observed_at,
            admin_id, med_id, drug_name, dosage, route, admin_at) = row

            if enc_id and enc_id not in encounters:
                encounters[enc_id] = Encounter(
                    enc_id, enc_type, enc_date, disc_date, provider_id, dept_name
                )

            if diag_id and diag_id not in diagnoses:
                diagnoses[diag_id] = Diagnosis(
                    diag_id, enc_id, icd10, diag_desc, diag_date
                )

            if admin_id and admin_id not in medications:
                medications[admin_id] = MedicationAdministered(
                    admin_id, enc_id, provider_id, med_id,
                    drug_name, dosage, route, admin_at
                )

            if obs_id and obs_id not in observations:
                observations[obs_id] = Observation(
                    obs_id, enc_id, loinc, obs_type, obs_val, obs_unit, observed_at
                )

        return {
            "patient":      patient,
            "encounters":   list(encounters.values()),
            "diagnoses":    list(diagnoses.values()),
            "medications":  list(medications.values()),
            "observations": list(observations.values())
        }

        