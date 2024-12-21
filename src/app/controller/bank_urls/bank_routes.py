from dataclasses import dataclass

from flask import Blueprint, request, jsonify, g

from src.app.middleware.middleware import auth_middleware
from src.app.models.bank import Bank
from src.app.services.bank_service import BankService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.utils import Utils
from src.app.utils.logger.logger import Logger


@dataclass
class BankHandler:
    bank_service: BankService
    logger: Logger = Logger()

    @classmethod
    def create(cls, bank_service: BankService) -> 'BankHandler':
        return cls(bank_service)

    @Utils.admin
    @api_logger(logger)
    def create_bank(self):
        request_body = request.get_json()
        try:
            bank_name = request_body['bank_name']
            if not bank_name:
                raise ValueError("bank name cannot be empty")

            new_bank = Bank(name=bank_name)

            self.bank_service.create_new_bank(new_bank)
            return jsonify({"message": "Bank created successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @Utils.admin
    @api_logger(logger)
    def update_bank(self, bank_id):
        try:
            if not bank_id:
                raise ValueError("bank id cannot be empty")

            new_bank_name = request.args.get('new-bank-name')
            if not new_bank_name:
                raise ValueError("bank name cannot be empty")

            self.bank_service.update_bank(bank_id, new_bank_name)
            return jsonify({"message": "Bank updated successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @Utils.admin
    @api_logger(logger)
    def delete_bank(self, bank_id):
        try:
            if not bank_id:
                raise ValueError("bank id cannot be empty")

            self.bank_service.delete_bank(bank_id)
            return jsonify({"message": "Bank deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def get_all_banks(self):
        try:
            banks = self.bank_service.get_all_banks()
            return jsonify(
                {
                    "banks":
                        [bank.__dict__ for bank in banks]
                        if banks else []
                }
            ), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def get_user_banks(self):
        try:
            user_id = g.get("user_id")
            banks = self.bank_service.get_user_banks(user_id)
            return jsonify(
                {
                    "banks": [bank.__dict__ for bank in banks] if banks else []
                }
            ), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def get_available_banks_for_user(self):
        try:
            user_id = g.get("user_id")
            banks = self.bank_service.get_available_banks_for_user(user_id)
            return jsonify(
                {
                    "banks": [bank.__dict__ for bank in banks] if banks else []
                }
            ), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400


def create_bank_routes(bank_service: BankService):
    bank_routes_blueprint = Blueprint('bank_routes', __name__)
    bank_routes_blueprint.before_request(auth_middleware)

    bank_handler = BankHandler.create(bank_service)

    bank_routes_blueprint.add_url_rule(
        '',
        'all_banks',
        bank_handler.get_all_banks,
        methods=['GET']
    )

    bank_routes_blueprint.add_url_rule(
        '/me',
        'user_banks',
        bank_handler.get_user_banks,
        methods=['GET']
    )

    bank_routes_blueprint.add_url_rule(
        '/available',
        'available_banks',
        bank_handler.get_available_banks_for_user,
        methods=['GET']
    )

    bank_routes_blueprint.add_url_rule(
        '/<bank_id>',
        'delete_bank',
        bank_handler.delete_bank,
        methods=['DELETE']
    )

    bank_routes_blueprint.add_url_rule(
        '/<bank_id>',
        'update_bank',
        bank_handler.update_bank,
        methods=['PATCH']
    )

    bank_routes_blueprint.add_url_rule(
        '',
        'create_bank',
        bank_handler.create_bank,
        methods=['POST']
    )

    return bank_routes_blueprint
