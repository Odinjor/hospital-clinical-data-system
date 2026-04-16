from models.db import execute_query


class Department:
    def __init__(self, dept_id, dept_name, location):
        self.dept_id = dept_id
        self.dept_name = dept_name
        self.location = location

    def to_dict(self):
        return {
            "dept_id":   self.dept_id,
            "dept_name": self.dept_name,
            "location":  self.location
        }

    @staticmethod
    def get_all_departments():
        query = "SELECT * FROM Department"
        result = execute_query(query, fetch=True)
        return [Department(*row) for row in result]
    
    @staticmethod
    def get_department_by_id(dept_id):
        query = "SELECT * FROM Department WHERE dept_id = %s"
        result = execute_query(query, (dept_id,), fetch=True)
        return Department(*result[0]) if result else None