from models.db import execute_query

class MedicationAdministered:
    def __init__(self, admin_id=None, encounter_id=None, provider_id=None, medication_id=None, drug_name=None, dosage=None, route=None, administered_at=None):
        self.admin_id = admin_id
        self.encounter_id = encounter_id
        self.provider_id = provider_id
        self.medication_id = medication_id
        self.drug_name = drug_name
        self.dosage = dosage
        self.route = route
        self.administered_at = administered_at

    def to_dict(self):
        return {
            "admin_id":        self.admin_id,
            "encounter_id":    self.encounter_id,
            "provider_id":     self.provider_id,
            "medication_id":   self.medication_id,
            "drug_name":       self.drug_name,
            "dosage":          self.dosage,
            "route":           self.route,
            "administered_at": str(self.administered_at) if self.administered_at else None
        }
    
    @staticmethod
    def search_medication_administered(encounter_id):
        query = "SELECT * FROM Medication_Administered WHERE encounter_id = %s"
        result = execute_query(query, (encounter_id,), fetch=True)
        return [MedicationAdministered(*row) for row in result] if result else []   

    @staticmethod
    def add_medication_administered(encounter_id, provider_id, medication_id, administered_at):
        query = """ 
        INSERT INTO Medication_Administered (encounter_id, provider_id, medication_id, administered_at)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (encounter_id, provider_id, medication_id, administered_at))
        
        query = "SELECT LAST_INSERT_ID()"
        result = execute_query(query, fetch=True)
        new_id = result[0][0] if result else None
        return MedicationAdministered(int(new_id), int(encounter_id), int(provider_id), int(medication_id), administered_at)

    @staticmethod
    def delete_medication_administered(encounter_id):
        query = "DELETE FROM Medication_Administered WHERE encounter_id = %s"
        execute_query(query, (encounter_id,))
        return True
    
    @staticmethod
    def update_medication_administered(encounter_id, provider_id=None, medication_id=None, administered_at=None):
        updates = []
        params = []
        
        if provider_id:
            updates.append("provider_id = %s")
            params.append(provider_id)
        if medication_id:
            updates.append("medication_id = %s")
            params.append(medication_id)
        if administered_at:
            updates.append("administered_at = %s")
            params.append(administered_at)

        if not updates:
            return False

        params.append(encounter_id)
        query = "UPDATE Medication_Administered SET " + ", ".join(updates) + " WHERE encounter_id = %s"
        execute_query(query, tuple(params))
        
        result = execute_query("SELECT * FROM Medication_Administered WHERE encounter_id = %s", (encounter_id,), fetch=True)
        if result:
            return MedicationAdministered(*result[0])
        return None