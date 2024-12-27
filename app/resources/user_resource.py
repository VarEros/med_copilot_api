from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app.models import db, User
import pytz

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([{
            "id": user.id,
            "email": user.email,
            "password": user.password
        } for user in users])
    def post(self):
        """Registro de usuario."""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validar que el username y password sean proporcionados
        if not email or not password:
            return {"message": "Email y contraseña son requeridos"}, 400

        # Comprobar si el usuario ya existe
        if User.query.filter_by(email=email).first():
            return {"message": "Email ya en uso"}, 400

        # Crear un nuevo usuario
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Usuario creado con exito", "id": new_user.id}, 200

class AuthResource(Resource):
    def post(self):
        """Autenticación de usuario."""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validar que el username y password sean proporcionados
        if not email or not password:
            return {"message": "Email y contraseña son requeridos"}, 400

        # Buscar al usuario
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            
            access_token = create_access_token(identity=user.id)
            return {"user_id": user.id, "access_token": access_token}, 200
        return {"message": "Credenciales invalidas"}, 401