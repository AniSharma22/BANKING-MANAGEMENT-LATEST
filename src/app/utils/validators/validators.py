import re
import uuid


class Validators:

    @staticmethod
    def is_name_valid(name: str) -> bool:
        """
        Validate if the given name is valid (2 < len < 16).
        :param name:
        :return:
        """
        return 2 < len(name) < 16

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """
        Validate if the given email is a valid Gmail account.
        :param email:
        :return:
        """
        gmail_regex = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        return bool(re.match(gmail_regex, email))

    @staticmethod
    def is_password_valid(password: str) -> bool:
        """
        Validate if the given password meets the required criteria:
        - Length between 8 and 16 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one special character
        """
        if not (8 <= len(password) <= 16):
            return False

        upper_case = False
        lower_case = False
        special_char = False

        # Define a set of special characters
        special_characters = set("!@#$%^&*()-_=+[]{}|;:',.<>?/")

        for char in password:
            if char.isupper():
                upper_case = True
            elif char.islower():
                lower_case = True
            elif char in special_characters:
                special_char = True

        return upper_case and lower_case and special_char

    @staticmethod
    def is_phone_number_valid(number: str) -> bool:
        """
        Validate if the given phone number is valid.
        - Must contain exactly 10 digits
        - Must start with 6, 7, 8, or 9
        """
        # Check if length is 10
        if len(number) != 10:
            return False

        # Check if starts with valid digits (6,7,8,9)
        if not number[0] in ('6', '7', '8', '9'):
            return False

        # Check if all characters are digits
        if not number.isdigit():
            return False

        return True

    @staticmethod
    def is_address_valid(address: str) -> bool:
        """
        Validate if the given address is valid.
        - should be more than 6 characters and less than 30 characters
        :param address:
        :return:
        """
        return 6 <= len(address) <= 30
