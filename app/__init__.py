from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.resources.user_resource import AuthResource, UserResource
from .models import db
from .resources.patient_resource import PatientResource
from .resources.consultation_resource import ConsultationResource
from .resources.consultation_d_resource import ConsultationDetailsResource
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '43ufjuvhb943plfjhr4'  # Cambia por una clave segura
    
    # Inicializamos SQLAlchemy
    db.init_app(app)
    
    # Configuramos la API
    api = Api(app)
    jwt = JWTManager(app)
    
    # Agregar los recursos a la API
    api.add_resource(PatientResource, 
                     '/patients', 
                     '/patients/<int:patient_id>',
                     '/patients/user/<int:user_id>')
    api.add_resource(ConsultationResource, 
                    '/consultations', 
                    '/consultations/<int:consultation_id>', 
                    '/consultations/patient/<int:patient_id>',
                    '/consultations/user/<int:user_id>')
    api.add_resource(ConsultationDetailsResource, 
                    '/consultations/details/<int:consultation_details_id>',
                    '/consultations/details/consultation/<int:consultation_id>')
    api.add_resource(UserResource, '/users')
    api.add_resource(AuthResource, '/auth')
    with app.app_context():
        db.create_all()
    
    return app