from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT

from hashlib import sha256

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        """Cifra la contraseña usando SHA256."""
        self.password = sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        """Verifica la contraseña contra el hash almacenado."""
        return self.password == sha256(password.encode('utf-8')).hexdigest()

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    personal_id = db.Column(db.String(14), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    follow_up = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False);
    consultations = db.relationship('Consultation', backref='patient', cascade="all, delete")

class Consultation(db.Model):
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    origin = db.Column(TINYINT, nullable=False)
    service = db.Column(TINYINT, nullable=False)
    status = db.Column(TINYINT, nullable=False)
    programed_date = db.Column(db.DateTime, nullable=True)
    registration_date = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    details_id = db.Column(db.Integer, db.ForeignKey('consultation_details.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

class ConsultationDetails(db.Model):
    __tablename__ = 'consultation_details'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(TINYINT(unsigned=True), nullable=True)
    height = db.Column(TINYINT(unsigned=True), nullable=True)
    temperature = db.Column(TINYINT, nullable=True)
    systolic_pressure = db.Column(TINYINT(unsigned=True), nullable=True)
    diastolic_pressure = db.Column(TINYINT(unsigned=True), nullable=True)
    heart_rate = db.Column(TINYINT(unsigned=True), nullable=True)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
