from dataclasses import dataclass
from flask import Blueprint, request, jsonify

from src.app.middleware.middleware import auth_middleware
from src.app.models.branch import Branch
from src.app.services.branch_service import BranchService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.utils import Utils
from src.app.utils.logger.logger import Logger


@dataclass
class BranchHandler:
    branch_service: BranchService
    logger = Logger()

    @classmethod
    def create(cls, branch_service: BranchService) -> 'BranchHandler':
        return cls(branch_service)

    @Utils.admin
    @api_logger(logger)
    def create_branch(self):
        request_body = request.get_json()
        try:
            branch_name = request_body['branch_name']
            if not branch_name:
                raise ValueError("branch name cannot be empty")
            branch_address = request_body['branch_address']
            if not branch_address:
                raise ValueError("branch address cannot be empty")
            bank_id = request_body['bank_id']
            if not bank_id:
                raise ValueError("bank id cannot be empty")

            new_branch = Branch(
                name=branch_name,
                address=branch_address,
                bank_id=bank_id
            )

            self.branch_service.create_new_branch(new_branch)
            return jsonify({"message": "Branch created successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @Utils.admin
    @api_logger(logger)
    def update_branch(self, branch_id):
        request_body = request.get_json()
        try:
            new_branch_name = request_body['new_branch_name']
            new_branch_address = request_body['new_branch_address']
            if not new_branch_name and not new_branch_address:
                raise ValueError("branch name and address both cannot be empty")

            self.branch_service.update_branch_details(branch_id, new_branch_name, new_branch_address)
            return jsonify({"message": "Branch details updated successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @Utils.admin
    @api_logger(logger)
    def delete_branch(self, branch_id):
        try:
            if branch_id is None:
                raise ValueError("branch id cannot be empty")

            self.branch_service.remove_branch(branch_id)
            return jsonify({"message": "Branch deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def get_bank_branches(self, bank_id):
        try:
            if bank_id is None:
                raise ValueError("bank id cannot be empty")

            branches = self.branch_service.get_bank_branches(bank_id)
            return jsonify({"bank_branches": [branch.__dict__ for branch in branches] if branches else []}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400


def create_branch_routes(branch_service: BranchService):
    branch_routes_blueprint = Blueprint('branch_routes', __name__)
    branch_routes_blueprint.before_request(auth_middleware)

    branch_handler = BranchHandler.create(branch_service)

    branch_routes_blueprint.add_url_rule(
        '',
        'create_branch',
        branch_handler.create_branch,
        methods=['POST']
    )

    branch_routes_blueprint.add_url_rule(
        '/<branch_id>',
        'update_branch',
        branch_handler.update_branch,
        methods=['PUT']
    )

    branch_routes_blueprint.add_url_rule(
        '/<branch_id>',
        'delete_branch',
        branch_handler.delete_branch,
        methods=['DELETE']
    )

    branch_routes_blueprint.add_url_rule(
        '/bank/<bank_id>',
        'get_bank_branches',
        branch_handler.get_bank_branches,
        methods=['GET']
    )

    return branch_routes_blueprint
