import uvicorn
from fastapi import FastAPI

from src.app.controller.account_controller.account_routes import create_account_router
from src.app.controller.bank_controller.bank_routes import create_bank_router
from src.app.controller.branch_controller.branch_routes import create_branch_router
from src.app.controller.transaction_controller.transaction_routes import create_transaction_router
from src.app.controller.user_controller.user_routes import create_user_router
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
from src.app.utils.db.db import DB
from src.app.utils.errors.error import register_validation_exception_handler


def create_app():
    app = FastAPI(
        title="Banking App",
        description="API for banking operations",
        version="1.0.0"
    )

    # Custom global exception handler (Validation errors)
    register_validation_exception_handler(app)

    # Initialize dependencies
    db = DB()

    user_repository = UserRepository(db)
    bank_repository = BankRepository(db)
    branch_repository = BranchRepository(db)
    account_repository = AccountRepository(db)
    transaction_repository = TransactionRepository(db)

    bank_service = BankService(bank_repository)
    branch_service = BranchService(branch_repository, bank_service)
    account_service = AccountService(account_repository, branch_service)
    transaction_service = TransactionService(transaction_repository, account_service)
    user_service = UserService(user_repository)

    # Include routers
    app.include_router(create_user_router(user_service))
    app.include_router(create_bank_router(bank_service))
    app.include_router(create_account_router(account_service))
    app.include_router(create_transaction_router(transaction_service))
    app.include_router(create_branch_router(branch_service))

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
