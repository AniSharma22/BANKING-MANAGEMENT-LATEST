import uuid


class Bank:
    def __init__(self, name: str, id: str = None):
        self.id = id if id else str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return (
            f"Bank("
            f"id='{self.id}', "
            f"name='{self.name}', "
        )
