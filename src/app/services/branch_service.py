from src.app.models.branch import Branch
from typing import List, Union

from src.app.utils.errors.error import NotExistsError, BankNotExistsError, BranchNotExistsError


class BranchService:
    def __init__(self, branch_repository, bank_service):
        self.branch_repository = branch_repository
        self.bank_service = bank_service

    def get_bank_branches(self, bank_id: str) -> Union[List[Branch], None]:
        if self.bank_service.get_bank_by_id(bank_id) is None:
            raise BankNotExistsError("Bank does not exist")

        return self.branch_repository.fetch_bank_branches(bank_id)

    def create_new_branch(self, branch: Branch):
        bank = self.bank_service.get_bank_by_id(branch.bank_id)
        if bank is None:
            raise BankNotExistsError("Bank does not exist")

        self.branch_repository.create_branch(branch)

    def update_branch_details(self, branch_id: str, new_branch_name, new_branch_address):
        # check if branch exists
        branch = self.get_branch_by_id(branch_id)
        if branch is None:
            raise BranchNotExistsError("Branch does not exist")

        new_branch_name = new_branch_name if new_branch_name else branch.name
        new_branch_address = new_branch_address if new_branch_address else branch.address

        self.branch_repository.update_branch(branch_id, new_branch_name, new_branch_address)

    def remove_branch(self, branch_id: str):
        # check if branch exists first
        if self.get_branch_by_id(branch_id) is None:
            raise BranchNotExistsError("Branch does not exist")

        self.branch_repository.delete_branch(branch_id)

    def get_branch_by_id(self, branch_id: str):
        return self.branch_repository.fetch_branch_by_id(branch_id)
