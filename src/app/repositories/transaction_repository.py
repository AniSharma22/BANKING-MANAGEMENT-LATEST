from src.app.models.transaction import Transaction
from src.app.utils.db.db import DB
from src.app.utils.db.query import GenericQueryBuilder
from src.app.utils.errors.error import DatabaseError


class TransactionRepository:
    def __init__(self, database: DB):
        self.db = database

    def make_transfer_transaction(self, transaction: Transaction):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION")

            # Step 1: Fetch sender's account balance
            query, values = GenericQueryBuilder.select("accounts", ["balance"], {"id": transaction.sender_acc_id})
            cursor.execute(query, values)
            sender_balance = cursor.fetchone()
            if not sender_balance:
                raise ValueError("Sender account does not exist.")
            sender_balance = sender_balance[0]

            # Step 2: Check if sender has enough balance
            if sender_balance < transaction.amount:
                raise ValueError("Insufficient funds in sender's account.")

            # Step 3: Get receiver's balance
            query, values = GenericQueryBuilder.select("accounts", ["balance"], {"id": transaction.receiver_acc_id})
            cursor.execute(query, values)
            receiver_balance = cursor.fetchone()
            if not receiver_balance:
                raise ValueError("Receiver account does not exist.")
            receiver_balance = receiver_balance[0]

            # Step 4: Update balances
            query, values = GenericQueryBuilder.update("accounts", {"balance": sender_balance - transaction.amount},
                                                       {"id": transaction.sender_acc_id})
            cursor.execute(query, values)
            query, values = GenericQueryBuilder.update("accounts", {"balance": receiver_balance + transaction.amount},
                                                       {"id": transaction.receiver_acc_id})
            cursor.execute(query, values)

            # Step 5: Insert transaction record
            query, values = GenericQueryBuilder.insert("transactions", {
                "id": transaction.id,
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "sender_acc_id": transaction.sender_acc_id,
                "receiver_acc_id": transaction.receiver_acc_id,
            })
            cursor.execute(query, values)

            # Commit the transaction
            conn.commit()
            print("Transaction completed successfully.")
        except Exception as e:
            conn.rollback()
            raise DatabaseError(str(e))

    def make_deposit_transaction(self, transaction: Transaction):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION")

            # Step 1: Get the receiver's balance
            query, values = GenericQueryBuilder.select("accounts", ["balance"], {"id": transaction.receiver_acc_id})
            cursor.execute(query, values)
            receiver_balance = cursor.fetchone()
            if not receiver_balance:
                raise ValueError("Receiver account does not exist.")
            receiver_balance = receiver_balance[0]

            # Step 2: Update the receiver's balance
            query, values = GenericQueryBuilder.update("accounts", {"balance": receiver_balance + transaction.amount},
                                                       {"id": transaction.receiver_acc_id})
            cursor.execute(query, values)

            # Step 3: Insert transaction record
            query, values = GenericQueryBuilder.insert("transactions", {
                "id": transaction.id,
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "sender_acc_id": transaction.sender_acc_id,
                "receiver_acc_id": transaction.receiver_acc_id,
            })
            cursor.execute(query, values)

            # Commit the transaction
            conn.commit()
            print("Transaction completed successfully.")
        except Exception as e:
            conn.rollback()
            raise DatabaseError(str(e))

    def make_withdraw_transaction(self, transaction: Transaction):
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION")

            # Step 1: Fetch sender's account balance
            query, values = GenericQueryBuilder.select("accounts", ["balance"], {"id": transaction.sender_acc_id})
            cursor.execute(query, values)
            sender_balance = cursor.fetchone()
            if not sender_balance:
                raise ValueError("Sender account does not exist.")
            sender_balance = sender_balance[0]

            # Step 2: Check if sender has enough balance
            if sender_balance < transaction.amount:
                raise ValueError("Insufficient funds in sender's account.")

            # Step 3: Update balances
            query, values = GenericQueryBuilder.update("accounts", {"balance": sender_balance - transaction.amount},
                                                       {"id": transaction.sender_acc_id})
            cursor.execute(query, values)

            # Step 4: Insert transaction record
            query, values = GenericQueryBuilder.insert("transactions", {
                "id": transaction.id,
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "sender_acc_id": transaction.sender_acc_id,
                "receiver_acc_id": transaction.receiver_acc_id,
            })
            cursor.execute(query, values)

            # Commit the transaction
            conn.commit()
            print("Transaction completed successfully.")
        except Exception as e:
            conn.rollback()
            raise DatabaseError(str(e))

    def fetch_user_transactions(self, account_id):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query, values = GenericQueryBuilder.select("transactions",
                                                       ["id", "amount", "transaction_type", "sender_acc_id",
                                                        "receiver_acc_id", "timestamp"],
                                                       {"sender_acc_id": account_id, "receiver_acc_id": account_id},
                                                       "timestamp")
            cursor.execute(query, values)

            transactions = cursor.fetchall()
            return [Transaction(id=transaction[0], amount=transaction[1], transaction_type=transaction[2],
                                sender_acc_id=transaction[3], receiver_acc_id=transaction[4], time_stamp=transaction[5])
                    for transaction in transactions] if transactions else []
        except Exception as e:
            raise DatabaseError(str(e))
