from flask import Flask, render_template

# import all route blueprints
from routes.patient import patients_bp
from routes.dashboard import dashboard_bp
from routes.encounters import encounters_bp
from routes.departments import departments_bp
from routes.providers import providers_bp
from routes.study import study_bp
from routes.study_enrollment import study_enrollment_bp
from routes.medication import medications_bp
from routes.medication_administered import medication_administered_bp
from routes.diagnosis import diagnosis_bp
from routes.observations import observations_bp

app = Flask(__name__)

# Register all blueprints with /api prefix for JSON endpoints
app.register_blueprint(patients_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
app.register_blueprint(encounters_bp, url_prefix="/api")
app.register_blueprint(departments_bp, url_prefix="/api")
app.register_blueprint(providers_bp, url_prefix="/api")
app.register_blueprint(study_bp, url_prefix="/api")
app.register_blueprint(study_enrollment_bp, url_prefix="/api")
app.register_blueprint(medications_bp, url_prefix="/api")
app.register_blueprint(medication_administered_bp, url_prefix="/api")
app.register_blueprint(diagnosis_bp, url_prefix="/api")
app.register_blueprint(observations_bp, url_prefix="/api")

# Main page - Dashboard
@app.route("/")
def home():
    return render_template("dashboard/index.html")

# Dashboard view
@app.route("/dashboard")
def dashboard_view():
    return render_template("dashboard/index.html")

# Patients view
@app.route("/patients")
def patients_view():
    return render_template("patient/index.html")

# Encounters view
@app.route("/encounters")
def encounters_view():
    return render_template("encounters/index.html")

# Departments view
@app.route("/departments")
def departments_view():
    return render_template("departments/index.html")

# Providers view
@app.route("/providers")
def providers_view():
    return render_template("providers/index.html")

# Studies view
@app.route("/studies")
def studies_view():
    return render_template("study/index.html")

if __name__ == "__main__":
    app.run(debug=True)