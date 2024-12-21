import uuid


class Branch:
    def __init__(self, name, bank_id: str, address, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.bank_id = bank_id
        self.name = name
        self.address = address

    def __eq__(self, other):
        if isinstance(other, Branch):
            return (
                    self.id == other.id and
                    self.bank_id == other.bank_id and
                    self.name == other.name and
                    self.address == other.address
            )
        return False

    def __repr__(self):
        return (
            f"Branch("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"bank_id='{self.bank_id}', "
            f"address='{self.address}')', "
        )
