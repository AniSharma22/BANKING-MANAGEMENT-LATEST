from typing import Union, List

from src.app.models.branch import Branch
from src.app.utils.db.db import DB
from src.app.utils.db.query import GenericQueryBuilder
from src.app.utils.errors.error import DatabaseError


class BranchRepository:
    def __init__(self, database: DB):
        self.db = database

    def fetch_bank_branches(self, bank_id: str) -> Union[List[Branch], None]:
        conn = self.db.get_connection()
        with conn:
            cursor = conn.cursor()
            query, values = GenericQueryBuilder.select("branches", ["id", "bank_id", "name", "address"],
                                                       {"bank_id": bank_id})
            cursor.execute(query, values)

            result = cursor.fetchall()
            if result is None:
                return None
            else:
                return [Branch(id=branch[0], bank_id=branch[1], name=branch[2], address=branch[3]) for branch in result]

    def create_branch(self, branch: Branch):
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.insert("branches", {"id": branch.id, "bank_id": branch.bank_id,
                                                                        "name": branch.name, "address": branch.address})
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def update_branch(self, branch_id: str, new_branch_name: str, new_branch_address: str):
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.update("branches",
                                                           {"name": new_branch_name, "address": new_branch_address},
                                                           {"id": branch_id})
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def delete_branch(self, branch_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.delete("branches", {"id": branch_id})
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_branch_by_id(self, branch_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.select("branches", ["id", "bank_id", "name", "address"],
                                                           {"id": branch_id})
                cursor.execute(query, values)
                result = cursor.fetchone()

                return Branch(id=result[0], bank_id=result[1], name=result[2], address=result[3]) if result else None
        except Exception as e:
            raise DatabaseError(str(e))
