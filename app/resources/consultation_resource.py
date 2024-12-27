from flask import jsonify, request
from flask_restful import Resource
from app.models import Patient, db, Consultation
from datetime import datetime
import pytz

class ConsultationResource(Resource):
    def get(self, consultation_id=None, patient_id=None, user_id=None):
        if consultation_id:
            # Obtener la consulta específica
            consultation = Consultation.query.get_or_404(consultation_id)
            patient = consultation.patient  # Acceso directo a la relación Patient desde Consultation
            return jsonify({
                "id": consultation.id,
                "description": consultation.description,
                "registration_date": format_iso8601(consultation.registration_date),
                "patient": {
                    "id": patient.id,
                    "personal_id": patient.personal_id,
                    "name": patient.name,
                    "lastname": patient.lastname,
                    "birthdate": format_iso8601(patient.birthdate),
                    "email": patient.email,
                    "phone": patient.phone,
                    "follow_up": patient.follow_up
                }
            })
        elif patient_id:
            # Obtener todas las consultas para un paciente específico
            consultations = Consultation.query.filter_by(patient_id=patient_id).all()
        elif user_id:
            consultations = Consultation.query.join(Patient).filter(Patient.user_id == user_id).all();
        else:
            # Obtener todas las consultas
            consultations = Consultation.query.all()
        return jsonify([{
            "id": consultation.id,
            "description": consultation.description,
            "registration_date": format_iso8601(consultation.registration_date),
            "patient": {
                "id": consultation.patient.id,
                "personal_id": consultation.patient.personal_id,
                "name": consultation.patient.name,
                "lastname": consultation.patient.lastname,
                "birthdate": format_iso8601(consultation.patient.birthdate),
                "email": consultation.patient.email,
                "phone": consultation.patient.phone,
                "follow_up": consultation.patient.follow_up
            }
        } for consultation in consultations])

    def post(self):
        data = request.json
        consultation = Consultation(
            description=data['description'],
            patient_id=data['patient_id']
        )
        db.session.add(consultation)
        db.session.commit()
        return jsonify({"message": "Consultation created", "id": consultation.id})

    def put(self, consultation_id):
        data = request.json
        consultation = Consultation.query.get_or_404(consultation_id)
        
        consultation.description = data.get('description', consultation.description)
        consultation.patient_id = data.get('patient_id', consultation.patient_id)
        
        db.session.commit()
        return jsonify({"message": "Consultation updated", "id": consultation.id})

    def delete(self, consultation_id):
        consultation = Consultation.query.get_or_404(consultation_id)
        db.session.delete(consultation)
        db.session.commit()
        return jsonify({"message": "Consultation deleted"})
    
def parse_iso8601(date_str):
    """Convierte una cadena en formato ISO 8601 a un objeto datetime con UTC."""
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)

def format_iso8601(dt):
    """Convierte un objeto datetime a una cadena en formato ISO 8601 en UTC."""
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ') if dt else None