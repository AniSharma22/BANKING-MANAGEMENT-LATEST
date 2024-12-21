import pytest

from src.app.models.account import Account
from src.app.models.branch import Branch
from src.app.models.transaction import Transaction


def test_transaction_model_negative_amount():
    with pytest.raises(ValueError):
        transaction = Transaction(amount=-10, transaction_type="withdraw")


def test_transaction_model_equality_check():
    transaction1 = Transaction(amount=10, transaction_type="withdraw", id="123", sender_acc_id="1", receiver_acc_id="2",
                               time_stamp="current")
    transaction2 = Transaction(amount=10, transaction_type="withdraw", id="123", sender_acc_id="1",
                               receiver_acc_id="2", time_stamp="current")

    transaction3 = {
        "amount": 10,
        "transaction_type": "withdraw",
        "id": "123",
        "sender_acc_id": "1",
        "receiver_acc_id": "2",
        "time_stamp": "current"
    }
    assert transaction1 == transaction2
    assert transaction1 != transaction3


def test_branch_model_equality_check():
    branch1 = Branch(name="Branch1", bank_id="123", address="supertech",id="123")
    branch2 = {
        "name": "Branch1",
        "bank_id": "123",
        "address": "supertech",
        "id": "123"
    }


    assert branch1 != branch2


def test_account_model_equality_check():
    account1 = Account(user_id="123", branch_id="123", bank_id="123",id="123",balance=100)
    account2 = {
        "user_id": "123",
        "branch_id": "123",
        "bank_id": "123",
        "id": "123",
        "balance": 100
    }

    assert account1 != account2
