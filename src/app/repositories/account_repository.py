from operator import truediv

from src.app.models.account import Account
from src.app.models.transaction import Transaction
from src.app.utils.db.db import DB
from src.app.utils.db.query import GenericQueryBuilder
from src.app.utils.errors.error import DatabaseError


class AccountRepository:
    def __init__(self, database: DB):
        self.db = database

    def create_account(self, account: Account):
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.insert("accounts", {"id": account.id, "user_id": account.user_id,
                                                                        "branch_id": account.branch_id,
                                                                        "bank_id": account.bank_id})
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def delete_account(self, account_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.delete("accounts", {"id": account_id})
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_account_by_id(self, account_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.select("accounts",
                                                           ["id", "user_id", "branch_id", "bank_id", "balance"],
                                                           {"id": account_id})
                cursor.execute(query, values)
                result = cursor.fetchone()
                return Account(id=result[0], user_id=result[1], branch_id=result[2], bank_id=result[3],
                               balance=result[4]) if result else None
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_all_user_accounts(self, user_id):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.select("accounts",
                                                           ["id", "user_id", "branch_id", "bank_id", "balance"],
                                                           {"user_id": user_id})
                cursor.execute(query, values)
                result = cursor.fetchall()

                return [
                    Account(id=account[0], user_id=account[1], branch_id=account[2], bank_id=account[3],
                            balance=account[4])
                    for account in result] if result else []
        except Exception as e:
            raise DatabaseError(str(e))

    def user_account_exists(self, user_id, bank_id):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.select("accounts", where={"user_id": user_id, "bank_id": bank_id})
                cursor.execute(query, values)
                result = cursor.fetchone()

                if result is not None:
                    return True
                else:
                    return False
        except Exception as e:
            raise DatabaseError(str(e))
