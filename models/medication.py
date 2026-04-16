from models.db import execute_query

class Medication:
    def __init__(self, medication_id=None, drug_name=None, dosage=None, route=None):
        self.medication_id = medication_id
        self.drug_name = drug_name
        self.dosage = dosage
        self.route = route
        
    @staticmethod
    def search_medication(medication_id):
        query = "SELECT * FROM Medication WHERE medication_id = %s"
        result = execute_query(query, (medication_id,), fetch=True)
        return Medication(*result[0]) if result else None
    @staticmethod
    def add_medication(drug_name, dosage, route):
        query = """ 
        INSERT INTO Medication (drug_name, dosage, route)
        VALUES (%s, %s, %s)
        """
        execute_query(query, (drug_name, dosage, route))
        
        query = "SELECT LAST_INSERT_ID()"
        result = execute_query(query, fetch=True)
        new_id = result[0][0] if result else None
        return Medication(int(new_id), drug_name, dosage, route)
    @staticmethod
    def delete_medication(medication_id):
        query = "DELETE FROM Medication WHERE medication_id = %s"
        execute_query(query, (medication_id,))
        return True
    @staticmethod
    def update_medication(medication_id, drug_name=None, dosage=None, route=None):
        updates = []
        params = []
        
        if drug_name:
            updates.append("drug_name = %s")
            params.append(drug_name)
        if dosage:
            updates.append("dosage = %s")
            params.append(dosage)
        if route:
            updates.append("route = %s")
            params.append(route)

        if not updates:
            return False

        params.append(medication_id)
        query = "UPDATE Medication SET " + ", ".join(updates) + " WHERE medication_id = %s"
        execute_query(query, tuple(params))
        return True
    @staticmethod
    def get_all_medications():
        query = "SELECT * FROM Medication"
        result = execute_query(query, fetch=True)
        return [Medication(int(row[0]), row[1], row[2], row[3]) for row in result] if result else []