# Hospital Clinical Data System

A comprehensive web-based clinical data management system designed for hospitals to centralize patient records, encounter tracking, provider management, and clinical analytics.

## Overview

The Hospital Clinical Data System is a Flask-based application that provides integrated management of clinical operations including patient data, medical encounters, diagnoses, medications, observations, departments, providers, and clinical studies. The system includes real-time dashboards with advanced analytics and forecasting capabilities.

## Features

### Core Management
- **Patient Management** - Comprehensive patient profiles with demographic data, medical history, and encounter tracking
- **Encounter Tracking** - Manage patient visits/encounters with discharge status, encounter types, and clinical data
- **Provider Management** - Track healthcare providers by specialty, role, and department assignment
- **Department Management** - Organize and monitor hospital departments and workload distribution
- **Medication Management** - Catalog medications with dosage and administration tracking
- **Clinical Observations** - Record LOINC-coded observations (vital signs, lab results, etc.)
- **Diagnosis Tracking** - ICD-10 coded diagnoses with patient encounter linkage
- **Clinical Studies** - Manage research studies with patient enrollment and tracking

### Analytics & Reporting
- **Department Workload Dashboard** - Visualize encounter volume and staffing utilization by department
- **Common Diagnoses Chart** - Identify most frequent diagnoses in your patient population
- **Monthly Volume Trends** - Track encounter patterns over time
- **Resource Forecast** - Predict department demand for the next 3 months with trend analysis
- **Patient Reports** - Generate comprehensive patient reports with encounter, diagnosis, medication, and observation details

### Advanced Features
- Real-time data visualization using Matplotlib charts
- Statistical forecasting with linear regression models
- Multi-tab interface for organized data management
- Responsive navigation between different modules
- Form validation and error handling
- Professional empty-state messaging

## Technology Stack

- **Backend**: Python 3.11, Flask 3.0.3
- **Database**: MySQL/MariaDB
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Visualization**: Pandas, Matplotlib, Scikit-learn
- **ORM**: Custom database abstraction layer

## Installation

### Prerequisites
- Python 3.11 or higher
- MySQL/MariaDB server
- pip (Python package manager)

### Setup Steps

1. **Clone/Navigate to the project**
   ```bash
   cd c:\dev\hospital-clinical-data-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Update `models/db.py` with your MySQL credentials
   - Import the database schema: `mysql -u root -p < db/schema.sql`
   - Load sample data: `mysql -u root -p < db/seed_data.sql`

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open browser and navigate to `http://localhost:5000`
   - Default development server runs on port 5000

## Project Structure

```
hospital-clinical-data-system/
├── app.py                          # Flask application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── controllers/                    # Request handlers & business logic
│   ├── dashboard.py               # Analytics and chart generation
│   ├── patient.py                 # Patient management
│   ├── encounters.py              # Encounter/visit management
│   ├── providers.py               # Provider management
│   ├── medications.py             # Medication catalog
│   ├── medication_administered.py # Medication administration tracking
│   ├── observations.py            # Clinical observations
│   ├── diagnosis.py               # Diagnosis code management
│   ├── departments.py             # Department management
│   ├── study.py                   # Clinical study management
│   └── study_enrollment.py        # Study enrollment tracking
│
├── models/                         # Data models & ORM
│   ├── db.py                      # Database connection & query execution
│   ├── dashboard.py               # Dashboard data queries
│   ├── patient.py                 # Patient model
│   ├── encounters.py              # Encounter model
│   ├── providers.py               # Provider model
│   ├── medications.py             # Medication model
│   ├── medication_administered.py # Medication administration model
│   ├── observations.py            # Observation model
│   ├── diagnosis.py               # Diagnosis model
│   ├── departments.py             # Department model
│   ├── study.py                   # Study model
│   └── study_enrollment.py        # Study enrollment model
│
├── routes/                         # URL route registration
│   ├── dashboard.py               # Dashboard routes
│   ├── patient.py                 # Patient routes
│   ├── encounters.py              # Encounter routes
│   ├── providers.py               # Provider routes
│   ├── medications.py             # Medication routes
│   ├── medication_administered.py # Medication admin routes
│   ├── observations.py            # Observation routes
│   ├── diagnosis.py               # Diagnosis routes
│   ├── departments.py             # Department routes
│   ├── study.py                   # Study routes
│   └── study_enrollment.py        # Study enrollment routes
│
├── static/
│   └── style.css                  # Global stylesheet
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── dashboard/
│   │   ├── index.html             # Main dashboard
│   │   ├── demands.html           # Department demand view
│   │   ├── diagnoses.html         # Top diagnoses view
│   │   ├── trends.html            # Trends view
│   │   └── visits.html            # Visit volume view
│   ├── patient/
│   │   ├── index.html             # Patient list and management
│   │   ├── report.html            # Patient report view
│   │   └── update.html            # Patient update form
│   ├── encounters/
│   │   ├── index.html             # Encounter management
│   │   └── update.html            # Encounter update form
│   ├── departments/
│   │   └── index.html             # Department management
│   ├── providers/
│   │   └── index.html             # Provider management
│   ├── study/
│   │   └── index.html             # Study management
│   └── observations/              # Observation templates
│
├── db/
│   ├── schema.sql                 # Database schema
│   └── seed_data.sql              # Sample data for testing
│
└── utils/
    └── request_helpers.py         # Utility functions
```

## API Endpoints

### Dashboard Analytics
- `GET /api/dashboard/workload` - Department workload statistics
- `GET /api/dashboard/diagnoses` - Top diagnoses data
- `GET /api/dashboard/seasonal` - Seasonal pattern data
- `GET /api/dashboard/charts/workload` - Department workload chart (PNG)
- `GET /api/dashboard/charts/diagnoses` - Common diagnoses chart (PNG)
- `GET /api/dashboard/charts/volume` - Monthly volume chart (PNG)
- `GET /api/dashboard/forecast` - Department forecast data (JSON)
- `GET /api/dashboard/charts/forecast` - Forecast chart (PNG)

### Patient Management
- `GET /api/patients` - List all patients
- `GET /api/patients/<id>` - Get patient details
- `POST /api/patients` - Create new patient
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Delete patient
- `GET /api/patients/<id>/report` - Generate patient report

### Encounters
- `GET /api/encounters` - List all encounters
- `GET /api/encounters/patient/<patient_id>` - Get encounters for patient
- `POST /api/encounters` - Create encounter
- `PUT /api/encounters/<id>` - Update encounter
- `DELETE /api/encounters/<id>` - Delete encounter

### Providers
- `GET /api/providers` - List all providers
- `GET /api/providers/<id>` - Get provider details
- `GET /api/providers/department/<dept_id>` - Get providers by department
- `POST /api/providers` - Create provider
- `PUT /api/providers/<id>` - Update provider
- `DELETE /api/providers/<id>` - Delete provider

### Additional Resources
- `/api/diagnoses` - Diagnosis management
- `/api/medications` - Medication catalog
- `/api/observations` - Clinical observations
- `/api/departments` - Department management
- `/api/studies` - Clinical studies
- `/api/study_enrollments` - Study enrollment tracking

## Database Schema

### Core Tables
- **Patient** - Patient demographics and identification
- **Encounter** - Clinical encounters/visits with discharge tracking
- **Provider** - Healthcare provider profiles with specialty
- **Department** - Hospital departments
- **Diagnosis** - ICD-10 coded diagnoses linked to encounters
- **Medication** - Medication catalog
- **Medication_Administration** - Administered medications with timestamp
- **Observation** - LOINC-coded clinical observations (vitals, labs)
- **Study** - Research studies
- **Study_Enrollment** - Patient enrollment in studies

## Usage Guide

### Dashboard
1. Navigate to home page to see overview of system
2. Click on analytics cards to view charts:
   - **Department Workload** - See current encounter distribution
   - **Common Diagnoses** - Identify frequent diagnoses
   - **Monthly Volume** - Track trends over time
   - **Resource Forecast** - Plan for future demand

### Patient Management
1. Go to "Manage Patients" section
2. View all patients or search by ID
3. Add new patients with DOB, sex, and ethnicity
4. Update patient information
5. Generate comprehensive patient reports
6. View patient encounters, diagnoses, medications, and observations

### Encounters
1. Navigate to Encounters section
2. Create encounters for patients
3. Link encounters to departments
4. Add discharge dates for tracking
5. Manage encounter type classifications

### Providers
1. Access Provider Management
2. View all providers by department
3. Add new providers with specialty and role
4. Update provider information
5. Filter providers by department

### Clinical Studies
1. Go to Clinical Studies section
2. Create new research studies
3. Set study dates and principal investigator
4. Enroll patients in studies
5. Track enrollment status (Active, Completed, Withdrawn)
6. Manage study information

### Analytics
1. Use dashboard charts for insights
2. Export data through API endpoints
3. View seasonal patterns in diagnoses
4. Review forecast predictions for resource planning

## Key Features Explained

### Smart Forecasting
- Uses 3-month historical trends to predict department demand
- Linear regression model identifies increasing/decreasing/stable trends
- Helps with staffing and resource planning

### Comprehensive Patient Reports
- Aggregates all patient data in single view
- Includes encounters, diagnoses, medications, and observations
- Links related clinical data automatically

### Multi-Tab Navigation
- Organized interface for each module
- Search and filter capabilities
- Form validation with helpful error messages
- Professional empty states when no data exists

### Real-Time Visualization
- PNG chart generation on-demand
- Responsive charts that adapt to data volume
- Professional styling and annotations

## Troubleshooting

### Charts Not Displaying
- Ensure database has sample data loaded
- Check that encounters and diagnoses exist
- Verify matplotlib is properly installed

### Database Connection Errors
- Confirm MySQL server is running
- Check credentials in `models/db.py`
- Verify database user permissions

### Port Already in Use
- Change port in `app.py` or use: `python app.py --port 5001`
- Or kill existing process using port 5000

## Sample Data

The system includes `db/seed_data.sql` with:
- 5 departments (Cardiology, Emergency, Neurology, Orthopedics, General Medicine)
- Multiple patients with demographics
- Various encounters across departments
- Sample diagnoses and observations
- Multiple providers with specialties

## Development

### Adding New Features
1. Create model in `models/` folder
2. Create controller in `controllers/` folder
3. Define routes in `routes/` folder
4. Create template in `templates/` folder
5. Register blueprint in `app.py`

### Database Modifications
1. Update `db/schema.sql`
2. Create corresponding model class
3. Add CRUD methods to model
4. Create controller functions
5. Define API routes

## License

This is a demo application for clinical data management education and evaluation purposes.

## Support

For issues or questions about the system:
1. Check the troubleshooting section
2. Review database schema in `db/schema.sql`
3. Verify all dependencies in `requirements.txt` are installed
4. Check Flask debug output in terminal

---

**Version**: 1.0.0  
**Last Updated**: April 15, 2026  
**Python**: 3.11+  
**Flask**: 3.0.3
