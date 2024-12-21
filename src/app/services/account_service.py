from src.app.models.account import Account
from src.app.repositories.account_repository import AccountRepository
from src.app.services.branch_service import BranchService
from src.app.utils.errors.error import NotExistsError, ExistsError


class AccountService:
    def __init__(self, account_repository: AccountRepository, branch_service: BranchService):
        self.account_repository = account_repository
        self.branch_service = branch_service

    def create_new_account(self, account: Account):
        if self.branch_service.get_branch_by_id(account.branch_id) is None:
            raise NotExistsError("Branch does not exist")

        if self.account_repository.user_account_exists(account.user_id, account.bank_id):
            raise ExistsError("User already has an account in this bank")

        self.account_repository.create_account(account)

    def get_account_by_id(self, account_id):
        return self.account_repository.fetch_account_by_id(account_id)

    def delete_account(self, user_id: str, account_id: str):
        # check if the account belongs to the user and exists then delete
        account = self.get_account_by_id(account_id)
        if account is None:
            raise NotExistsError('Account does not exist')
        if account.user_id != user_id:
            raise PermissionError('You do not have permission to delete this account')

        self.account_repository.delete_account(account)

    def get_user_accounts(self, user_id: str):
        return self.account_repository.fetch_all_user_accounts(user_id)
