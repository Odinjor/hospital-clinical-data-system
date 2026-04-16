from models.db import execute_query

class Study:
    def __init__(self, study_id=None, study_name=None, start_date=None, end_date=None, principal_investigator=None):
        self.study_id = study_id
        self.study_name = study_name
        self.start_date = start_date
        self.end_date = end_date
        self.principal_investigator = principal_investigator

    @staticmethod
    def get_all_studies():
        query = "SELECT * FROM Study ORDER BY study_id DESC"
        result = execute_query(query, fetch=True)
        return [Study(*row) for row in result] if result else []
    
    @staticmethod
    def search_study(study_id):
        query = "SELECT * FROM Study WHERE study_id = %s"
        result = execute_query(query, (int(study_id),), fetch=True)
        return Study(*result[0]) if result else None
    
    @staticmethod
    def add_study(study_name, start_date, end_date, principal_investigator):
        query = """ 
        INSERT INTO Study (study_name, start_date, end_date, principal_investigator)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (study_name, start_date, end_date, principal_investigator))
        
        result = execute_query("SELECT LAST_INSERT_ID()", fetch=True)
        new_id = result[0][0] if result else None
        return Study(new_id, study_name, start_date, end_date, principal_investigator)
    
    @staticmethod
    def delete_study(study_id):
        query = "DELETE FROM Study WHERE study_id = %s"
        execute_query(query, (int(study_id),))
        return True
    
    @staticmethod
    def update_study(study_id, study_name=None, start_date=None, end_date=None, principal_investigator=None):
        updates = []
        params = []
        
        if study_name:
            updates.append("study_name = %s")
            params.append(study_name)
        if start_date:
            updates.append("start_date = %s")
            params.append(start_date)
        if end_date:
            updates.append("end_date = %s")
            params.append(end_date)
        if principal_investigator:
            updates.append("principal_investigator = %s")
            params.append(principal_investigator)

        if not updates:
            return False

        params.append(study_id)
        query = "UPDATE Study SET " + ", ".join(updates) + " WHERE study_id = %s"
        execute_query(query, tuple(params))
        
        query = "SELECT LAST_INSERT_ID()"
        result = execute_query(query, fetch=True)
        return result[0] if result else None