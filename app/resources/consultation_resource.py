from flask import jsonify, request
from flask_restful import Resource
from app.models import db, Consultation
from datetime import datetime

class ConsultationResource(Resource):
    def get(self, consultation_id=None, patient_id=None):
        if consultation_id:
            # Si se proporciona consultation_id, obtenemos una consulta específica
            consultation = Consultation.query.get_or_404(consultation_id)
            return jsonify({
                "id": consultation.id,
                "description": consultation.description,
                "registration_date": consultation.registration_date,
                "patient_id": consultation.patient_id
            })
        elif patient_id:
            # Si se proporciona patient_id, obtenemos solo las consultas de ese paciente
            consultations = Consultation.query.filter_by(patient_id=patient_id).all()
            return jsonify([{
                "id": consultation.id,
                "description": consultation.description,
                "registration_date": consultation.registration_date,
                "patient_id": consultation.patient_id
            } for consultation in consultations])
        else:
            # Si no se proporciona ningún ID, obtenemos todas las consultas
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

    def put(self, consultation_id):
        data = request.json
        consultation = Consultation.query.get_or_404(consultation_id)
        
        consultation.description = data.get('description', consultation.description)
        consultation.registration_date = datetime.strptime(data['registration_date'], '%Y-%m-%d %H:%M:%S') if data.get('registration_date') else consultation.registration_date
        consultation.patient_id = data.get('patient_id', consultation.patient_id)
        
        db.session.commit()
        return jsonify({"message": "Consultation updated", "id": consultation.id})

    def delete(self, consultation_id):
        consultation = Consultation.query.get_or_404(consultation_id)
        db.session.delete(consultation)
        db.session.commit()
        return jsonify({"message": "Consultation deleted"})