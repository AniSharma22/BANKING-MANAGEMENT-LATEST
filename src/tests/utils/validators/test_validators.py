import unittest

from src.app.utils.validators.validators import Validators


class TestValidators(unittest.TestCase):

    def test_is_name_valid(self):
        # Valid names
        self.assertTrue(Validators.is_name_valid("Alice"))
        self.assertTrue(Validators.is_name_valid("Bob"))
        # Invalid names
        self.assertFalse(Validators.is_name_valid("A"))  # Too short
        self.assertFalse(Validators.is_name_valid("ThisNameIsTooLong"))  # Too long

    def test_is_email_valid(self):
        # Valid emails
        self.assertTrue(Validators.is_email_valid("example@gmail.com"))
        self.assertTrue(Validators.is_email_valid("user123@gmail.com"))
        # Invalid emails
        self.assertFalse(Validators.is_email_valid("example@yahoo.com"))  # Non-Gmail
        self.assertFalse(Validators.is_email_valid("user@gmail"))  # Missing .com
        self.assertFalse(Validators.is_email_valid("user123@.com"))  # Invalid domain

    def test_is_password_valid(self):
        # Valid passwords
        self.assertTrue(Validators.is_password_valid("Password@123"))
        self.assertTrue(Validators.is_password_valid("Strong#Pass8"))
        # Invalid passwords
        self.assertFalse(Validators.is_password_valid("short"))  # Too short
        self.assertFalse(Validators.is_password_valid("nouppercase@123"))  # No uppercase
        self.assertFalse(Validators.is_password_valid("NOLOWERCASE@123"))  # No lowercase
        self.assertFalse(Validators.is_password_valid("NoSpecialChar123"))  # No special character

    def test_is_phone_number_valid(self):
        # Valid phone numbers
        self.assertTrue(Validators.is_phone_number_valid("9876543210"))
        self.assertTrue(Validators.is_phone_number_valid("6789012345"))
        # Invalid phone numbers
        self.assertFalse(Validators.is_phone_number_valid("1234567890"))  # Does not start with 6, 7, 8, or 9
        self.assertFalse(Validators.is_phone_number_valid("987654321"))  # Too short
        self.assertFalse(Validators.is_phone_number_valid("98765432101"))  # Too long
        self.assertFalse(Validators.is_phone_number_valid("98765432ab"))  # Contains non-digit characters

    def test_is_address_valid(self):
        # Valid addresses
        self.assertTrue(Validators.is_address_valid("123 Main St"))
        self.assertTrue(Validators.is_address_valid("456 Elm Street Apt 7"))
        # Invalid addresses
        self.assertFalse(Validators.is_address_valid("123"))  # Too short
        self.assertFalse(
            Validators.is_address_valid("This address is way too long to be considered valid."))  # Too long
