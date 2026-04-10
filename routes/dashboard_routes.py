from flask import Blueprint, request, render_template, redirect
from models.db import execute_query

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/visits")
def visits_per_department():
    query = """ 
    SELECT d.dept_name, COUNT(*) AS total_visits
    FROM Encounter e
    JOIN Department d ON e.dept_id = d.dept_id
    GROUP BY d.dept_name
    """
    result = execute_query(query, fetch=True)
    return render_template("dashboard/visits.html", data=result)

@dashboard_bp.route("/dashboard/trends")
def workload_trends():
    query = """ 
    SELECT dept_id, COUNT(*) AS visits, WEEK(encounter_date) AS week
    FROM Encounter
    GROUP BY dept_id, week
    """
    result = execute_query(query, fetch=True)
    return render_template("dashboard/trends.html", data=result)

@dashboard_bp.route("/dashboard/diagnoses")
def common_diagnoses():
    query = """ 
    SELECT icd10_code, COUNT(*) AS count
    FROM Diagnosis
    GROUP BY icd10_code
    ORDER BY count DESC
    """
    result = execute_query(query, fetch=True)
    return render_template("dashboard/diagnoses.html", data=result)

@dashboard_bp.route("/dashboard/demands")
def resource_demands():
    query = """ 
    SELECT dept_id, AVG(daily_visits) AS avg_visits
    FROM (
        SELECT dept_id, COUNT(*) AS daily_visits
        FROM Encounter
        GROUP BY dept_id, DATE(encounter_date)
    ) AS sub
    GROUP BY dept_id

    """
    result = execute_query(query, fetch=True)
    return render_template("dashboard/demands.html", data=result)