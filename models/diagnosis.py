from models.db import execute_query

class Diagnosis:
    def __init__(self, diagnosis_id, encounter_id, icd10_code, diagnosis_description, created_at):
        self.diagnosis_id = diagnosis_id
        self.encounter_id = encounter_id
        self.icd10_code = icd10_code
        self.diagnosis_description = diagnosis_description
        self.created_at = created_at

    def to_dict(self):
        return {
            "diagnosis_id":          self.diagnosis_id,
            "encounter_id":          self.encounter_id,
            "icd10_code":            self.icd10_code,
            "diagnosis_description": self.diagnosis_description,
            "created_at":        str(self.created_at) if self.created_at else None
        }

    @staticmethod
    def get_diagnosis_by_encounter(encounter_id):
        query = "SELECT * FROM Diagnosis WHERE encounter_id = %s"
        result = execute_query(query, (encounter_id,), fetch=True)
        return [Diagnosis(*row) for row in result]
    
    @staticmethod
    def add_diagnosis(encounter_id, icd10_code, diagnosis_description=None):
        query = """ 
        INSERT INTO Diagnosis (encounter_id, icd10_code, diagnosis_description, created_at)
        VALUES (%s, %s, %s, CURDATE())
        """
        execute_query(query, (encounter_id, icd10_code, diagnosis_description))
        
        query = "SELECT LAST_INSERT_ID()"
        result = execute_query(query, fetch=True)
        new_id = result[0][0] if result else None
        return Diagnosis(new_id, encounter_id, icd10_code, diagnosis_description, None)

    
    @staticmethod
    def delete_diagnosis(diagnosis_id):
        query = "DELETE FROM Diagnosis WHERE diagnosis_id = %s"
        execute_query(query, (diagnosis_id,))
        return True
    
    @staticmethod
    def update_diagnosis(diagnosis_id, encounter_id=None, icd10_code=None, diagnosis_description=None):
        updates = []
        params = []
        
        if encounter_id:
            updates.append("encounter_id = %s")
            params.append(encounter_id)
        if icd10_code:
            updates.append("icd10_code = %s")
            params.append(icd10_code)
        if diagnosis_description:
            updates.append("diagnosis_description = %s")
            params.append(diagnosis_description)

        if not updates:
            return False

        params.append(diagnosis_id)
        query = "UPDATE Diagnosis SET " + ", ".join(updates) + " WHERE diagnosis_id = %s"
        execute_query(query, tuple(params))
        
        result = execute_query("SELECT * FROM Diagnosis WHERE diagnosis_id = %s", (diagnosis_id,), fetch=True)
        return Diagnosis(*result[0]) if result else None
    
