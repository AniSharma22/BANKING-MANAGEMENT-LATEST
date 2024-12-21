from typing import Optional
from src.app.models.user import User
from src.app.utils.db.db import DB
from src.app.utils.errors.error import DatabaseError
from src.app.utils.db.query import GenericQueryBuilder


class UserRepository:

    def __init__(self, database: DB):
        self.db = database

    def save_user(self, user: User) -> None:
        """Saves a new user to the database."""
        try:
            conn = self.db.get_connection()
            with conn:
                query, values = GenericQueryBuilder.insert("users", {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "password": user.password,
                    "phone_no": user.phone_no,
                    "address": user.address,
                    "role": user.role,
                })
                conn.execute(query, values)
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_user_by_email(self, email: str) -> Optional[User]:
        """Fetches a user from the database by their email."""
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query, values = GenericQueryBuilder.select("users",
                                                           ["id", "name", "email", "password", "phone_no", "address",
                                                            "role"], {
                                                               "email": email,
                                                           })
                cursor.execute(query, values)
                result = cursor.fetchone()

            if result:
                return User(
                    id=result[0],
                    name=result[1],
                    email=result[2],
                    password=result[3],
                    phone_no=result[4],
                    address=result[5],
                    role=result[6]
                )
            return None
        except Exception as e:
            raise DatabaseError(str(e))
