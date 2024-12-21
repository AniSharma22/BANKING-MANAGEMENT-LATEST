from src.app.models.bank import Bank
from src.app.utils.db.db import DB
from src.app.utils.db.query import GenericQueryBuilder
from src.app.utils.errors.error import DatabaseError


class BankRepository:
    def __init__(self, database: DB):
        self.db = database

    def create_bank(self, bank: Bank):
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.insert("banks", {"id": bank.id, "name": bank.name})
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def get_all_banks(self):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query = GenericQueryBuilder.select("banks", ["id", "name"])
                cursor.execute(query)
                results = cursor.fetchall()

            return [Bank(id=bank[0], name=bank[1]) for bank in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def get_new_banks_for_user(self, user_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT b.id, b.name 
                FROM banks b
                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM accounts a 
                    WHERE a.bank_id = b.id AND a.user_id = ?
                )
                ''', (user_id,))
                results = cursor.fetchall()

            return [Bank(id=bank[0], name=bank[1]) for bank in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def update_bank_name(self, bank_id: str, new_bank_name: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.update("banks", {"name": new_bank_name}, {"id": bank_id})
                cursor.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def remove_bank(self, bank_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.delete("banks", {"id": bank_id})
                cursor.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_user_banks(self, user_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT b.id, b.name
                    FROM banks b
                    INNER JOIN accounts a ON b.id = a.bank_id
                    WHERE a.user_id = ?;    
                ''', (user_id,))
                results = cursor.fetchall()
                return [Bank(id=row[0], name=row[1]) for row in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_bank_by_id(self, bank_id: str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.select("banks", ["id", "name"], {"id": bank_id})
                cursor.execute(query, values)
                results = cursor.fetchone()
                return Bank(id=results[0], name=results[1]) if results else None
        except Exception as e:
            raise DatabaseError(str(e))
