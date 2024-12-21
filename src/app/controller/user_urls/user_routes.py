from flask import Blueprint, request, jsonify
from werkzeug.routing import ValidationError
from dataclasses import dataclass

from src.app.models.user import User
from src.app.services.user_service import UserService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.utils import Utils
from src.app.utils.validators.validators import Validators
from src.app.utils.logger.logger import Logger


@dataclass
class UserHandler:
    user_service: UserService
    logger = Logger()

    @classmethod
    def create(cls, user_service):
        return cls(user_service)

    @api_logger(logger)
    def login(self):
        request_body = request.get_json()
        try:
            email = request_body['email'].strip().lower()
            if not Validators.is_email_valid(email):
                raise ValidationError('Email is not valid')
            password = request_body['password'].strip()

            user = self.user_service.login_user(email, password)

            token = Utils.create_jwt_token(user.id, user.role)
            return {'token': token, 'role': user.role}, 200
        except Exception as e:
            print(f"Login error: {str(e)}")  # Add this line
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def signup(self):
        request_body = request.get_json()
        try:
            name = request_body['name'].strip()
            if not Validators.is_name_valid(name):
                raise ValidationError('Name is not valid')
            email = request_body['email'].strip().lower()
            if not Validators.is_email_valid(email):
                raise ValidationError('Email is not valid')
            password = request_body['password'].strip()
            if not Validators.is_password_valid(password):
                raise ValidationError('Password is not valid')
            phone_no = request_body['phone_no'].strip()
            if not Validators.is_phone_number_valid(phone_no):
                raise ValidationError('Phone number is not valid')
            address = request_body['address'].strip()
            if not Validators.is_address_valid(address):
                raise ValidationError('Address is not valid')

            user = User(name=name, email=email, password=password, phone_no=phone_no, address=address)

            self.user_service.signup_user(user)
            token = Utils.create_jwt_token(user.id, user.role)
            return jsonify({'token': token, 'role': user.role}), 200

        except Exception as e:
            return jsonify({"message": str(e)}), 400


def create_user_routes(user_service: UserService) -> Blueprint:
    user_routes_blueprint = Blueprint('user_routes', __name__)

    user_handler = UserHandler.create(user_service)

    user_routes_blueprint.add_url_rule(
        '/login',
        'login',
        user_handler.login,
        methods=['POST']
    )

    user_routes_blueprint.add_url_rule(
        '/signup',
        'signup',
        user_handler.signup,
        methods=['POST']
    )

    return user_routes_blueprint
