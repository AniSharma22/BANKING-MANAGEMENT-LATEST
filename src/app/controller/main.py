import jwt
from flask import Flask, request, jsonify, g

from src.app.controller.account_urls.account_routes import create_account_routes
from src.app.controller.bank_urls.bank_routes import create_bank_routes
from src.app.controller.branch_urls.branch_routes import create_branch_routes
from src.app.controller.transaction_urls.transaction_routes import create_transaction_routes
from src.app.repositories.account_repository import AccountRepository
from src.app.repositories.bank_repository import BankRepository
from src.app.repositories.branch_repository import BranchRepository
from src.app.repositories.transaction_repository import TransactionRepository
from src.app.repositories.user_repository import UserRepository
from src.app.services.account_service import AccountService
from src.app.services.bank_service import BankService
from src.app.services.branch_service import BranchService
from src.app.services.transaction_service import TransactionService
from src.app.services.user_service import UserService
from src.app.controller.user_urls.user_routes import create_user_routes
from src.app.utils.db.db import DB


def create_app():
    app = Flask(__name__)

    db = DB()

    bank_repository = BankRepository(db)
    branch_repository = BranchRepository(db)
    account_repository = AccountRepository(db)
    transaction_repository = TransactionRepository(db)
    user_repository = UserRepository(db)

    bank_service = BankService(bank_repository)
    branch_service = BranchService(branch_repository, bank_service)
    account_service = AccountService(account_repository, branch_service)
    transaction_service = TransactionService(transaction_repository, account_service)
    user_service = UserService(user_repository)

    # Register blueprints
    app.register_blueprint(
        create_bank_routes(bank_service),
        url_prefix='/bank'
    )

    app.register_blueprint(
        create_branch_routes(branch_service),
        url_prefix='/branch'
    )

    app.register_blueprint(
        create_account_routes(account_service),
        url_prefix='/account'
    )

    app.register_blueprint(
        create_transaction_routes(transaction_service),
        url_prefix='/transaction'
    )

    app.register_blueprint(
        create_user_routes(user_service),
        url_prefix='/user'
    )

    @app.route('/')
    def index():
        return 'Hello World!'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
