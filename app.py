from flask import Flask, render_template
from models import db

# import your route files
from routes.patient_routes import patients_bp
from routes.dashboard_routes import dashboard_bp
from routes.encounter_routes import encounters_bp

app = Flask(__name__)

# register blueprints (VERY IMPORTANT)
app.register_blueprint(patients_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(encounters_bp)

# home route
@app.route("/")
def home():
    return render_template("dashboard.html")  # your main page

if __name__ == "__main__":
    app.run(debug=True)