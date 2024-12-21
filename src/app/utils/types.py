from enum import Enum

class Role(Enum):
    USER = 'user'
    ADMIN = "admin"

class TransactionType(Enum):
    # SWAP
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"
