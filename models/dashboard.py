from models.db import execute_query

class Dashboard:

    @staticmethod
    def get_department_workload():
        query = """
            SELECT dd.dept_name,
                   COUNT(e.encounter_id)                          AS total_encounters,
                   SUM(CASE WHEN e.discharge_date IS NULL THEN 1 ELSE 0 END) AS active_encounters,
                   ROUND(AVG(DATEDIFF(
                       COALESCE(e.discharge_date, CURDATE()), e.encounter_date
                   )), 1)                                          AS avg_length_of_stay
            FROM Encounter e
            JOIN Department dd ON e.dept_id = dd.dept_id
            GROUP BY dd.dept_name
            ORDER BY total_encounters DESC
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_top_diagnoses(limit=10):
        query = """
            SELECT d.icd10_code, d.diagnosis_description,
                   COUNT(*) AS frequency
            FROM Diagnosis d
            GROUP BY d.icd10_code, d.diagnosis_description
            ORDER BY frequency DESC
            LIMIT %s
        """
        return execute_query(query, (limit,), fetch=True)

    @staticmethod
    def get_seasonal_patterns():
        query = """
            SELECT YEAR(e.encounter_date)  AS yr,
                   MONTH(e.encounter_date) AS mo,
                   WEEK(e.encounter_date)  AS wk,
                   d.icd10_code,
                   d.diagnosis_description,
                   COUNT(*)               AS case_count
            FROM Encounter e
            JOIN Diagnosis d ON e.encounter_id = d.encounter_id
            GROUP BY yr, mo, wk, d.icd10_code, d.diagnosis_description
            ORDER BY yr, mo, wk, case_count DESC
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_monthly_encounter_volume():
        query = """
            SELECT YEAR(encounter_date)  AS yr,
                   MONTH(encounter_date) AS mo,
                   WEEK(encounter_date)  AS wk,
                   COUNT(*)              AS total
            FROM Encounter
            GROUP BY yr, mo, wk
            ORDER BY yr, mo, wk
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_encounter_history_by_dept():
        query = """
            SELECT dd.dept_name,
                YEAR(e.encounter_date)  AS yr,
                MONTH(e.encounter_date) AS mo,
                WEEK(e.encounter_date)  AS wk,
                COUNT(*)                AS total
            FROM Encounter e
            JOIN Department dd ON e.dept_id = dd.dept_id
            GROUP BY dd.dept_name, yr, mo, wk
            ORDER BY dd.dept_name, yr, mo, wk
        """
        return execute_query(query, fetch=True)