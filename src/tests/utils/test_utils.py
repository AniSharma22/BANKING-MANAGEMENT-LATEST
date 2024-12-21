import unittest
from src.app.utils.utils import Utils


class TestUtils(unittest.TestCase):
    def test_hash_password(self):
        password = "mypassword"
        hashed_password = Utils.hash_password(password)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(hashed_password.startswith("$2b$"))

    def test_check_password(self):
        password = "mypassword"
        hashed_password = Utils.hash_password(password)
        self.assertTrue(Utils.check_password(password, hashed_password))
        self.assertFalse(Utils.check_password("wrongpassword", hashed_password))

    def test_create_jwt_token(self):
        user_id = "12345"
        role = "admin"
        token = Utils.create_jwt_token(user_id, role)
        self.assertIsInstance(token, str)

    def test_decode_jwt_token(self):
        user_id = "12345"
        role = "admin"
        token = Utils.create_jwt_token(user_id, role)
        decoded_payload = Utils.decode_jwt_token(token)
        self.assertEqual(decoded_payload["user_id"], user_id)
        self.assertEqual(decoded_payload["role"], role)
