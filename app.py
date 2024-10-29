from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from models import db, Patient, Consultation
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Inicializamos SQLAlchemy
db.init_app(app)

# Configuramos la API
api = Api(app)

# Ruta para los pacientes
class PatientResource(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = Patient.query.get_or_404(patient_id)
            return jsonify({
                "id": patient.id,
                "personal_id": patient.personal_id,
                "name": patient.name,
                "lastname": patient.lastname,
                "birthdate": patient.birthdate,
                "email": patient.email,
                "phone": patient.phone,
                "follow_up": patient.follow_up
            })
        else:
            patients = Patient.query.all()
            return jsonify([{
                "id": patient.id,
                "personal_id": patient.personal_id,
                "name": patient.name,
                "lastname": patient.lastname,
                "birthdate": patient.birthdate,
                "email": patient.email,
                "phone": patient.phone,
                "follow_up": patient.follow_up
            } for patient in patients])

    def post(self):
        data = request.json
        patient = Patient(
            personal_id=data['personal_id'],
            name=data['name'],
            lastname=data['lastname'],
            birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d'),
            email=data.get('email'),
            phone=data.get('phone'),
            follow_up=data['follow_up']
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({"message": "Patient created", "id": patient.id})

# Ruta para las consultas
class ConsultationResource(Resource):
    def get(self, consultation_id=None):
        if consultation_id:
            consultation = Consultation.query.get_or_404(consultation_id)
            return jsonify({
                "id": consultation.id,
                "description": consultation.description,
                "registration_date": consultation.registration_date,
                "patient_id": consultation.patient_id
            })
        else:
            consultations = Consultation.query.all()
            return jsonify([{
                "id": consultation.id,
                "description": consultation.description,
                "registration_date": consultation.registration_date,
                "patient_id": consultation.patient_id
            } for consultation in consultations])

    def post(self):
        data = request.json
        consultation = Consultation(
            description=data['description'],
            registration_date=datetime.strptime(data['registration_date'], '%Y-%m-%d %H:%M:%S') if data.get('registration_date') else None,
            patient_id=data['patient_id']
        )
        db.session.add(consultation)
        db.session.commit()
        return jsonify({"message": "Consultation created", "id": consultation.id})

# Agregar los recursos a la API
api.add_resource(PatientResource, '/patients', '/patients/<int:patient_id>')
api.add_resource(ConsultationResource, '/consultations', '/consultations/<int:consultation_id>')

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)