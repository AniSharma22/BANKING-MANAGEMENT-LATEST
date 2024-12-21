import uuid


class Transaction:
    # TODO FB: REMOVE UNREQUIRED FIELDS
    # TODO : SEPERATE DTOS AND REQUEST OBJECTS
    # TRANSACTION TYPE FIX
    def __init__(self, amount: int, transaction_type, sender_acc_id=None, receiver_acc_id=None, time_stamp=None,
                 id=None):
        self.id = id if id else str(uuid.uuid4())
        self.sender_acc_id = sender_acc_id
        self.receiver_acc_id = receiver_acc_id
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.amount = amount
        self.transaction_type = transaction_type
        self.time_stamp = time_stamp

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return (
                    self.id == other.id and
                    self.sender_acc_id == other.sender_acc_id and
                    self.receiver_acc_id == other.receiver_acc_id and
                    self.amount == other.amount and
                    self.time_stamp == other.time_stamp and
                    self.transaction_type == other.transaction_type
            )
        return False

    def __repr__(self):
        return (
            f"Transaction("
            f"id='{self.id}', "
            f"amount='{self.amount}', "
            f"transaction_type='{self.transaction_type}', "
            f"sender_acc_id='{self.sender_acc_id}')', "
            f"receiver_acc_id='{self.receiver_acc_id}')', "
            f"timestamp='{self.time_stamp}')', "
        )
