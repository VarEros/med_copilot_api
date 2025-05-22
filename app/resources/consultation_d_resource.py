from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from app.models import Consultation, Patient, db, ConsultationDetails
from datetime import datetime
import pytz

class ConsultationDetailsResource(Resource):
    @jwt_required()
    def get(self, consultation_details_id):
        # Obtener los detalles de la consulta específica
        consultation_details = ConsultationDetails.query.get_or_404(consultation_details_id)
        return jsonify({
            "id": consultation_details.id,
            "weight": consultation_details.weight,
            "height": consultation_details.height,
            "temperature": consultation_details.temperature,
            "systolic_pressure": consultation_details.systolic_pressure,
            "diastolic_pressure": consultation_details.diastolic_pressure,
            "heart_rate": consultation_details.heart_rate,
            "symptoms": consultation_details.symptoms,
            "diagnosis": consultation_details.diagnosis,
            "treatment": consultation_details.treatment
        })
    
    @jwt_required()
    def post(self, consultation_id):
        data = request.get_json()
        consultation_details = ConsultationDetails()
        consultation_details.weight = data['weight']
        consultation_details.height = data['height']
        consultation_details.temperature = data['temperature']
        consultation_details.systolic_pressure = data['systolic_pressure']
        consultation_details.diastolic_pressure = data['diastolic_pressure']
        consultation_details.heart_rate = data['heart_rate']
        consultation_details.symptoms = data['symptoms']
        consultation_details.diagnosis = data['diagnosis']
        consultation_details.treatment = data['treatment']
        db.session.add(consultation_details)
        db.session.commit()
        consultation = Consultation.query.get_or_404(consultation_id)
        consultation.details_id = consultation_details.id
        db.session.commit()
        
        return jsonify({"message": "Consultation details created successfully."})
    
    @jwt_required()
    def put(self, consultation_details_id):
        data = request.get_json()
        consultation_details = ConsultationDetails.query.get_or_404(consultation_details_id)
        consultation_details.weight = data['weight']
        consultation_details.height = data['height']
        consultation_details.temperature = data['temperature']
        consultation_details.systolic_pressure = data['systolic_pressure']
        consultation_details.diastolic_pressure = data['diastolic_pressure']
        consultation_details.heart_rate = data['heart_rate']
        consultation_details.symptoms = data['symptoms']
        consultation_details.diagnosis = data['diagnosis']
        consultation_details.treatment = data['treatment']
        db.session.commit()
        return jsonify({"message": "Consultation details updated successfully."})