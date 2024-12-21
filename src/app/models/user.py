import uuid

from src.app.utils.types import Role
from typing import Dict


class User:

    def __init__(self, name: str, email: str, password: str, phone_no: str, address: str, id: str = None,
                 role: str = Role.USER.value):
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.address = address
        self.role = role

    def __repr__(self):
        return (
            f"User("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"email='{self.email}', "
            f"password='{self.password}')', "
            f"phone_no='{self.phone_no}', ')', "
            f"address='{self.address}', ')', "
            f"role='{self.role}'"
        )
