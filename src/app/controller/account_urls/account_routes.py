from dataclasses import dataclass

from flask import Blueprint, jsonify, g, request

from src.app.middleware.middleware import auth_middleware
from src.app.models.account import Account
from src.app.services.account_service import AccountService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.logger.logger import Logger


@dataclass
class AccountHandler:
    account_service: AccountService
    logger: Logger = Logger()

    @classmethod
    def create(cls, account_service: AccountService) -> 'AccountHandler':
        return cls(account_service)

    @api_logger(logger)
    def create_account(self):
        request_body = request.get_json()
        try:
            user_id = g.get('user_id')
            bank_id = request_body['bank_id']
            if bank_id is None:
                raise ValueError('Bank ID cannot be None')
            branch_id = request_body['branch_id']
            if branch_id is None:
                raise ValueError('Branch ID cannot be None')

            account = Account(user_id, branch_id, bank_id)
            self.account_service.create_new_account(account)
            return jsonify({'message': 'Account created'}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def get_user_accounts(self):
        try:
            user_id = g.get('user_id')
            accounts = self.account_service.get_user_accounts(user_id)
            return jsonify(
                {
                    'accounts':
                        [account.__dict__ for account in accounts]
                        if accounts else []
                }
            ), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400


def create_account_routes(account_service: AccountService):
    account_routes_blueprint = Blueprint('account_routes', __name__)
    account_routes_blueprint.before_request(auth_middleware)

    account_handler = AccountHandler.create(account_service)

    account_routes_blueprint.add_url_rule(
        '',
        'create_account',
        account_handler.create_account,
        methods=['POST']
    )

    account_routes_blueprint.add_url_rule(
        '',
        'get_accounts',
        account_handler.get_user_accounts,
        methods=['GET']
    )

    return account_routes_blueprint
