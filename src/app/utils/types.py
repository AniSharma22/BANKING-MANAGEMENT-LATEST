from enum import Enum

class Role(Enum):
    USER = 'user'
    ADMIN = "admin"

class TransactionType(Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"
    transfer = "TRANSFER"
