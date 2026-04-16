from models.db import execute_query

class StudyEnrollment:
    def __init__(self, patient_id=None, study_id=None, consent_date=None, enrollment_status=None):
        self.study_id = study_id
        self.patient_id = patient_id
        self.consent_date = consent_date
        self.enrollment_status = enrollment_status
    
    @staticmethod
    def search_study_enrollment(patient_id):
        query = "SELECT * FROM Study_Enrollment WHERE patient_id = %s"
        result = execute_query(query, (patient_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def add_study_enrollment(patient_id, study_id, consent_date, enrollment_status):
        query = "INSERT INTO Study_Enrollment (patient_id, study_id, consent_date, enrollment_status) VALUES (%s, %s, %s, %s)"
        execute_query(query, (int(patient_id), int(study_id), consent_date, enrollment_status))
        result = execute_query("SELECT LAST_INSERT_ID()", fetch=True)
        new_id = result[0][0] if result else None
        return StudyEnrollment(int(new_id), int(patient_id), int(study_id), consent_date, enrollment_status)

    @staticmethod
    def delete_study_enrollment(patient_id):
        query = "DELETE FROM Study_Enrollment WHERE patient_id = %s"
        execute_query(query, (patient_id,))
        return True
    
    @staticmethod
    def update_study_enrollment(patient_id, study_id=None, consent_date=None, enrollment_status=None):
        updates = []
        params = []
        
        if study_id:
            updates.append("study_id = %s")
            params.append(int(study_id))
        if consent_date:
            updates.append("consent_date = %s")
            params.append(consent_date)
        if enrollment_status:
            updates.append("enrollment_status = %s")
            params.append(enrollment_status)
        
        if not updates:
            return False
        params.append(int(patient_id))
        query = "UPDATE Study_Enrollment SET " + ", ".join(updates) + " WHERE patient_id = %s"
        execute_query(query, tuple(params))
        
        query = "SELECT LAST_INSERT_ID()"
        result = execute_query(query, fetch=True)
        return result[0] if result else None

        