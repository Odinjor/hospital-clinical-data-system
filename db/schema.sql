create database hospital_db;
use hospital_db;
/*Core independent tables, have no FK*/
create table Department(
	dept_id int primary key,
	dept_name VARCHAR(100),
	location VARCHAR(100)
);

create table Patient(
	patient_id INT AUTO_INCREMENT primary key,
	dob DATE,
	sex VARCHAR(10),
	ethnicity VARCHAR(50),
	created_at DATE
);
/*Tables that depend on the above*/
create table Provider( 
	provider_id INT auto_increment primary key,
	speacialty VARCHAR(100),
	role VARCHAR(50),
	dept_id INT,
	foreign key (dept_id) references department(dept_id)
);

/*Ecounter Layer*/
create table Encounter(
	encounter_id INT AUTO_INCREMENT primary key,
	patient_id INT,
	dept_id INT,
	encounter_date DATE,
	discharge_date DATE null,
	encounter_type VARCHAR(50),
	foreign key (patient_id) references Patient(patient_id),
	foreign key (dept_id) references Department(dept_id)
);


/*Clinical Data Tables*/
create table Diagnosis(
	diagnosis_id int AUTO_INCREMENT primary key,
	encounter_id INT,
	icd10_code VARCHAR(10),
	diagnosis_date DATE,
	foreign key (encounter_id) references Encounter(encounter_id)
);

create table Observation(
	observation_id INT AUTO_INCREMENT primary key,
	encounter_id INT,
	loinc_code VARCHAR(20),
	observation_type VARCHAR(100),
	value FLOAT,
	unit VARCHAR(20),
	observed_at DATE,
	foreign key (encounter_id) references Encounter(encounter_id)
);



/*Medication System*/
create table Medication(
	medication_id INT AUTO_INCREMENT primary key,
	drug_name VARCHAR(100),
	dosage VARCHAR(50),
	route VARCHAR(50)
);

create table Medication_Administration(
	admin_id INT AUTO_INCREMENT primary key,
	encounter_id INT,
	provider_id INT,
	medication_id INT,
	administered_at DATE,
	foreign key (encounter_id) references Encounter(encounter_id),
	foreign key (provider_id) references Provider(provider_id),
	foreign key (medication_id) references Medication(medication_id)
);

/*Research Tables*/
create table Study (
	study_id INT AUTO_INCREMENT primary key,
	study_name VARCHAR(255),
	start_date DATE,
	end_date DATE,
	principal_investigator VARCHAR(100)
);

create table Study_Enrollment (
	study_id INT AUTO_INCREMENT,
	patient_id INT,
	consent_date DATE,
	enrollment_status VARCHAR(50),
	primary key (study_id, patient_id),
	foreign key (study_id) references  Study(study_id),
	foreign key (patient_id) references Patient(patient_id)
);

create table Staffing_Notes(
	staffing_date DATE,
	staff_status VARCHAR(50)
);


