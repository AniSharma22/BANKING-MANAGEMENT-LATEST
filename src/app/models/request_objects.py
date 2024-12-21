from dataclasses import field
from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4, constr, validator, field_validator, ValidationError, \
    model_validator

from src.app.utils.validators.validators import Validators


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email')
    def validate_email(cls, value):
        if not Validators.is_email_valid(value):
            raise ValidationError()
        return value


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_no: str
    address: str

    @field_validator('name')
    def validate_name(cls, value):
        if not Validators.is_name_valid(value):
            raise ValidationError()
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if not Validators.is_password_valid(value):
            raise ValidationError()
        return value

    @field_validator('phone_no')
    def validate_phone_no(cls, value):
        if not Validators.is_phone_number_valid(value):
            raise ValidationError()
        return value

    @field_validator('address')
    def validate_address(cls, value):
        if not Validators.is_address_valid(value):
            raise ValidationError()
        return value


class CreateAccountRequest(BaseModel):
    bank_id: UUID4
    branch_id: UUID4


class CreateBankRequest(BaseModel):
    bank_name: str


class UpdateBankRequest(BaseModel):
    new_bank_name: str


class CreateBranchRequest(BaseModel):
    branch_name: str
    branch_address: str
    bank_id: UUID4


class UpdateBranchRequest(BaseModel):
    new_branch_name: Optional[str] = None
    new_branch_address: Optional[str] = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not self.new_branch_name and not self.new_branch_address:
            raise ValueError("At least one of 'new_branch_name' or 'new_branch_address' must be provided.")
        return self


class CreateTransactionRequest(BaseModel):
    sender_acc_id: Optional[UUID4] = None
    receiver_acc_id: Optional[UUID4] = None
    amount: int

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not self.sender_acc_id and not self.receiver_acc_id:
            raise ValueError("At least one of 'sender_acc_id' or 'receiver_acc_id' must be provided.")

        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        return self
