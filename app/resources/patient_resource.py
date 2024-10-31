from flask import jsonify, request
from flask_restful import Resource
from app.models import db, Patient
from datetime import datetime
import pytz

class PatientResource(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = Patient.query.get_or_404(patient_id)
            return jsonify({
                "id": patient.id,
                "personal_id": patient.personal_id,
                "name": patient.name,
                "lastname": patient.lastname,
                "birthdate": format_iso8601(patient.birthdate),
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
                "birthdate": format_iso8601(patient.birthdate),
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
            birthdate=parse_iso8601(data['birthdate']),
            email=data.get('email'),
            phone=data.get('phone'),
            follow_up=data['follow_up']
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({"message": "Patient created", "id": patient.id})

    def put(self, patient_id):
        data = request.json
        patient = Patient.query.get_or_404(patient_id)
        
        patient.personal_id = data.get('personal_id', patient.personal_id)
        patient.name = data.get('name', patient.name)
        patient.lastname = data.get('lastname', patient.lastname)
        patient.birthdate = parse_iso8601(data['birthdate'])
        patient.email = data.get('email', patient.email)
        patient.phone = data.get('phone', patient.phone)
        patient.follow_up = data.get('follow_up', patient.follow_up)
        
        db.session.commit()
        return jsonify({"message": "Patient updated", "id": patient.id})

    def delete(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": "Patient deleted"})

def parse_iso8601(date_str):
    """Convierte una cadena en formato ISO 8601 a un objeto datetime con UTC."""
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)

def format_iso8601(dt):
    """Convierte un objeto datetime a una cadena en formato ISO 8601 en UTC."""
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ') if dt else None