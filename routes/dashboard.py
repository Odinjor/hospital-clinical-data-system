from flask import Blueprint
from controllers.dashboard import (
    get_department_workload, get_top_diagnoses,
    get_seasonal_patterns,   chart_department_workload,
    chart_top_diagnoses,     chart_monthly_volume,
    forecast_department_demand,
    chart_forecast_demand
)

dashboard_bp = Blueprint("dashboard", __name__)

# JSON
dashboard_bp.route("/dashboard/workload",  methods=["GET"])(get_department_workload)
dashboard_bp.route("/dashboard/diagnoses", methods=["GET"])(get_top_diagnoses)
dashboard_bp.route("/dashboard/seasonal",  methods=["GET"])(get_seasonal_patterns)

# Charts → returns PNG, drop directly into an <img src="..."> tag
dashboard_bp.route("/dashboard/charts/workload",  methods=["GET"])(chart_department_workload)
dashboard_bp.route("/dashboard/charts/diagnoses", methods=["GET"])(chart_top_diagnoses)
dashboard_bp.route("/dashboard/charts/volume",    methods=["GET"])(chart_monthly_volume)
dashboard_bp.route("/dashboard/forecast",        methods=["GET"])(forecast_department_demand)
dashboard_bp.route("/dashboard/charts/forecast", methods=["GET"])(chart_forecast_demand)