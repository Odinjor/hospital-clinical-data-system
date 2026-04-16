from models.db import execute_query

class Encounter:
    def __init__(self, encounter_id=None, patient_id=None, dept_id=None, encounter_date=None, discharge_date=None, encounter_type=None, provider_id=None, dept_name=None):
        self.encounter_id = encounter_id
        self.patient_id = patient_id
        self.dept_id = dept_id
        self.encounter_date = encounter_date
        self.discharge_date = discharge_date
        self.created_at = None
        self.encounter_type = encounter_type
        self.provider_id = provider_id
        self.dept_name = dept_name
    
    def to_dict(self):
        return {
            "encounter_id":   self.encounter_id,
            "encounter_type": self.encounter_type,
            "encounter_date": str(self.encounter_date) if self.encounter_date else None,
            "discharge_date": str(self.discharge_date) if self.discharge_date else None,
            "provider_id":    self.provider_id,
            "dept_name":      self.dept_name
        }

    @staticmethod
    def search_encounter_by_patient(patient_id):
        query = "SELECT * FROM Encounter WHERE patient_id = %s"
        result = execute_query(query, (patient_id,), fetch=True)
        
        return Encounter(*result[0]) if result else None

    @staticmethod
    def add_encounter(patient_id, dept_id, encounter_date, discharge_date=None, encounter_type=None):
        query = """ 
        INSERT INTO Encounter (patient_id, dept_id, encounter_date, discharge_date, encounter_type, created_at)
        VALUES (%s, %s, %s, %s, %s, CURDATE())
        """
        execute_query(query, (patient_id, dept_id, encounter_date, discharge_date, encounter_type))
        
        query = "SELECT LAST_INSERT_ID()"
        result = execute_query(query, fetch=True)
        new_id = result[0][0] if result else None
        return Encounter(int(new_id), int(patient_id), int(dept_id), encounter_date, discharge_date, encounter_type)

    @staticmethod
    def delete_encounter(encounter_id):
        query = "DELETE FROM Encounter WHERE encounter_id = %s"
        execute_query(query, (encounter_id,))
        return True
    
    @staticmethod
    def update_encounter(encounter_id, patient_id=None, dept_id=None, encounter_date=None, discharge_date=None, encounter_type=None):
        updates = []
        params = []
        
        if patient_id:
            updates.append("patient_id = %s")
            params.append(patient_id)
        if dept_id:
            updates.append("dept_id = %s")
            params.append(dept_id)
        if encounter_date:
            updates.append("encounter_date = %s")
            params.append(encounter_date)
        if discharge_date:
            updates.append("discharge_date = %s")
            params.append(discharge_date)   
        if encounter_type:
            updates.append("encounter_type = %s")
            params.append(encounter_type)

        if not updates:
            return False

        params.append(encounter_id)
        query = "UPDATE Encounter SET " + ", ".join(updates) + " WHERE encounter_id = %s"
        execute_query(query, tuple(params))
        
        result = execute_query("SELECT * FROM Encounter WHERE encounter_id = %s", (encounter_id,), fetch=True)
        return Encounter(*result[0]) if result else None
    
    @staticmethod
    def list_all_encounters():
        query = "SELECT * FROM Encounter"
        result = execute_query(query, fetch=True)
        return [Encounter(*row) for row in result] if result else []
       