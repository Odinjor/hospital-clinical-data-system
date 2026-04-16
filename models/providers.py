from models.db import execute_query

class Provider:
    def __init__(self, provider_id=None, specialty=None, role=None, dept_id=None):
        self.provider_id = provider_id
        self.specialty = specialty
        self.role = role
        self.dept_id = dept_id

    @staticmethod
    def get_all_providers():
        query = "SELECT provider_id, specialty, role, dept_id FROM Provider"
        result = execute_query(query, fetch=True)
        return [Provider(*row) for row in result] if result else []
    
    @staticmethod
    def get_provider_by_id(provider_id):
        query = "SELECT provider_id, specialty, role, dept_id FROM Provider WHERE provider_id = %s"
        result = execute_query(query, (provider_id,), fetch=True)
        return Provider(*result[0]) if result else None
    
    @staticmethod
    def add_provider(specialty, role, dept_id):
        execute_query(
            "INSERT INTO Provider (specialty, role, dept_id) VALUES (%s, %s, %s)",
            (specialty, role, int(dept_id))    # cast here
        )
        result = execute_query("SELECT LAST_INSERT_ID()", fetch=True)
        new_id = result[0][0] if result else None
        return Provider(new_id, specialty, role, int(dept_id))

        
    @staticmethod
    def delete_provider(provider_id):
        query = "DELETE FROM Provider WHERE provider_id = %s"
        execute_query(query, (provider_id,))
        return True
    
    @staticmethod
    def update_provider(provider_id, specialty=None, role=None, dept_id=None):
        updates = []
        params = []
        
        if specialty:
            updates.append("specialty = %s")
            params.append(specialty)
        if role:
            updates.append("role = %s")
            params.append(role)
        if dept_id:
            updates.append("dept_id = %s")
            params.append(int(dept_id))

        if not updates:
            return False

        params.append(int(provider_id))
        query = "UPDATE Provider SET " + ", ".join(updates) + " WHERE provider_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def get_providers_with_department(department_id):
        query = "SELECT provider_id, specialty, role, dept_id FROM Provider WHERE dept_id = %s"
        result = execute_query(query, (department_id,), fetch=True)
    
        
        return [Provider(*row) for row in result] if result else []
        
    