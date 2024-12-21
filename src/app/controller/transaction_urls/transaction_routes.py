from dataclasses import dataclass

from flask import Blueprint, jsonify, g, request

from src.app.middleware.middleware import auth_middleware
from src.app.models.transaction import Transaction
from src.app.services.transaction_service import TransactionService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.logger.logger import Logger


@dataclass
class TransactionHandler:
    transaction_service: TransactionService
    logger = Logger()

    @classmethod
    def create(cls, transaction_service: TransactionService) -> 'TransactionHandler':
        return cls(transaction_service)

    @api_logger(logger)
    def create_transaction(self):
        request_body = request.get_json()
        try:
            #:Todo FB :- CONVERT TO AN OBJECT
            # fix value error (exception handling) custom exceptions
            user_id = g.get('user_id')
            sender_acc_id = request_body['sender_acc_id'] if request_body['sender_acc_id'] else None
            receiver_acc_id = request_body['receiver_acc_id'] if request_body['receiver_acc_id'] else None
            if not sender_acc_id and not receiver_acc_id:
                raise ValueError("Sender and receiver ids both cannot be None")
            amount = request_body['amount']
            if not isinstance(amount, int):
                raise ValueError("Amount must be an integer")
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            transaction_type = request.args.get('transaction_type')

            transaction = Transaction(amount, transaction_type, sender_acc_id, receiver_acc_id)
            self.transaction_service.create_transaction(transaction, user_id)

            return jsonify({'message': 'Transaction successful'}), 201


        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def view_transaction(self):
        try:
            user_id = g.get('user_id')
            account_id = request.args.get('account_id')
            if not account_id:
                raise ValueError("Account Id is required")

            transactions = self.transaction_service.view_transactions(user_id, account_id)
            return jsonify(
                {"transactions": [transaction.__dict__ for transaction in transactions] if transactions else []}), 200

        except Exception as e:
            return jsonify({"message": str(e)}), 400


def create_transaction_routes(transaction_service: TransactionService):
    transaction_routes_blueprint = Blueprint('transaction_routes', __name__)
    transaction_routes_blueprint.before_request(auth_middleware)

    transaction_handler = TransactionHandler.create(transaction_service)

    transaction_routes_blueprint.add_url_rule(
        '',
        'initiate_transaction',
        transaction_handler.create_transaction,
        methods=['POST']
    )

    transaction_routes_blueprint.add_url_rule(
        '',
        'view_transaction',
        transaction_handler.view_transaction,
        methods=['GET']
    )

    return transaction_routes_blueprint
