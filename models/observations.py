from models.db import execute_query

class Observation:
    def __init__(self, observation_id=None, encounter_id=None, loinc_code=None, observation_type=None, value=None, unit=None, observed_at=None):
        self.observation_id = observation_id
        self.encounter_id = encounter_id
        self.loinc_code = loinc_code
        self.observation_type = observation_type
        self.value= value
        self.unit = unit
        self.observed_at = observed_at
    
    def to_dict(self):
        return {
            "observation_id":   self.observation_id,
            "encounter_id":     self.encounter_id,
            "loinc_code":       self.loinc_code,
            "observation_type": self.observation_type,
            "value":            self.value,
            "unit":             self.unit,
            "observed_at":      str(self.observed_at) if self.observed_at else None
        }

    @staticmethod
    def search_observations(encounter_id):
        query = "SELECT * FROM Observation WHERE encounter_id = %s"
        result = execute_query(query, (encounter_id,), fetch=True)
        observations = [Observation(int(row[0]), int(row[1]), row[2], row[3], float(row[4]), row[5], row[6]) for row in result] if result else []
        return observations

    @staticmethod
    def add_observation(encounter_id, loinc_code, observation_type, value, unit, observed_at):
        query = """ 
        INSERT INTO Observation (encounter_id, loinc_code, observation_type, value, unit, observed_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (encounter_id, loinc_code, observation_type, value, unit, observed_at))
        
        
        result = execute_query("SELECT LAST_INSERT_ID()", fetch=True)
        new_id = result[0][0] if result else None
        return Observation(int(new_id), int(encounter_id), loinc_code, observation_type, float(value) if value else None, unit, observed_at)

    @staticmethod
    def delete_observation(observation_id):
        query = "DELETE FROM Observation WHERE observation_id = %s"
        execute_query(query, (observation_id,))
        return True
    

    @staticmethod
    def update_observation(observation_id, encounter_id=None, loinc_code=None, observation_type=None, value=None, unit=None, observed_at=None):
        updates = []
        params = []
        
        if encounter_id:
            updates.append("encounter_id = %s")
            params.append(encounter_id)
        if loinc_code:
            updates.append("loinc_code = %s")
            params.append(loinc_code)
        if observation_type:
            updates.append("observation_type = %s")
            params.append(observation_type)
        if value:
            updates.append("value = %s")
            params.append(value)
        if unit:
            updates.append("unit = %s")
            params.append(unit)
        if observed_at:
            updates.append("observed_at = %s")
            params.append(observed_at)              

        if not updates:
            return False

        params.append(observation_id)
        query = "UPDATE Observation SET " + ", ".join(updates) + " WHERE observation_id = %s"
        execute_query(query, tuple(params))
        return True