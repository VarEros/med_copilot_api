from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from app.models import ConsultationDetails, Patient, db, Consultation
from datetime import datetime
import pytz

class ConsultationResource(Resource):
    @jwt_required()
    def get(self, consultation_id=None, patient_id=None):
        if consultation_id:
            # Obtener la consulta específica
            consultation = Consultation.query.get_or_404(consultation_id)
            patient = consultation.patient  # Acceso directo a la relación Patient desde Consultation
            return jsonify({
                "id": consultation.id,
                "description": consultation.description,
                "origin": consultation.origin,
                "service": consultation.service,
                "status": consultation.status,
                "programed_date": format_iso8601(consultation.programed_date),
                "registration_date": format_iso8601(consultation.registration_date),
                "duration": consultation.duration,
                "details_id": consultation.details_id,
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
        else:
            user_id = get_jwt_identity()
            consultations = Consultation.query.join(Patient).filter(Patient.user_id == user_id).all();
        
        return jsonify([{
            "id": consultation.id,
            "description": consultation.description,
            "origin": consultation.origin,
            "service": consultation.service,
            "status": consultation.status,
            "programed_date": format_iso8601(consultation.programed_date),
            "registration_date": format_iso8601(consultation.registration_date),
            "duration": consultation.duration,
            "details_id": consultation.details_id,
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

    @jwt_required()
    def post(self):
        data = request.json
        consultation = Consultation(
            description=data['description'],
            origin=data['origin'],
            service=data['service'],
            status=data['status'],
            patient_id=data['patient_id']
        )
        db.session.add(consultation)
        db.session.commit()
        return jsonify({"message": "Consultation created", "id": consultation.id})

    @jwt_required()
    def put(self, consultation_id):
        data = request.json
        consultation = Consultation.query.get_or_404(consultation_id)
        
        consultation.description = data.get('description', consultation.description)
        consultation.origin = data.get('origin', consultation.origin)
        consultation.service = data.get('service', consultation.service)
        consultation.status = data.get('status', consultation.status)
        consultation.duration = data.get('duration', consultation.duration)
        
        db.session.commit()
        return jsonify({"message": "Consultation updated", "id": consultation.id})

    @jwt_required()
    def delete(self, consultation_id):
        consultation = Consultation.query.get_or_404(consultation_id)
        consultationDetails = ConsultationDetails.query.get_or_404(consultation.details_id)
        db.session.delete(consultation)
        db.session.delete(consultationDetails)
        db.session.commit()
        return jsonify({"message": "Consultation deleted"})
    
def parse_iso8601(date_str):
    """Convierte una cadena en formato ISO 8601 a un objeto datetime con UTC."""
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)

def format_iso8601(dt):
    """Convierte un objeto datetime a una cadena en formato ISO 8601 en UTC."""
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ') if dt else None