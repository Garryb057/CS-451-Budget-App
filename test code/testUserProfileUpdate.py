import unittest
import re
from typing import Optional, Tuple
from User import User

class TestUserProfileUpdate(unittest.TestCase):
    def setUp(self):
        self.baseUser = User(
            email="test@example.com",
            passwordHash="Passhash123",
            fname = "John",
            lname = "Doe",
            phoneNumber = "9135552929",
            dateCreated = "2025-10-01"
        )
    
    def test_successful_update_first_name(self):
        success, msg = self.baseUser.update_profile(fname = "Johnathan")

        self.assertTrue(success)
        self.assertIn("fname", msg)
        self.assertEqual(self.baseUser.get_fname(), "Johnathan")
        self.assertEqual(self.baseUser.get_lname(), "Doe")
        self.assertEqual(self.baseUser.get_phoneNumber(), "9135552929")

    def test_successful_update_last_name(self):
        success, msg = self.baseUser.update_profile(lname = "Smith")

        self.assertTrue(success)
        self.assertIn("lname", msg)
        self.assertEqual(self.baseUser.get_fname(), "John")
        self.assertEqual(self.baseUser.get_lname(), "Smith")
        self.assertEqual(self.baseUser.get_phoneNumber(), "9135552929")
    
    def test_successful_update_phone_number(self):
        success, msg = self.baseUser.update_profile(phoneNumber = "8165550000")

        self.assertTrue(success)
        self.assertIn("phoneNumber", msg)
        self.assertEqual(self.baseUser.get_fname(), "John")
        self.assertEqual(self.baseUser.get_lname(), "Doe")
        self.assertEqual(self.baseUser.get_phoneNumber(), "8165550000")

    def test_successful_all_fields(self):
        success, msg = self.baseUser.update_profile(
            fname = "Jane",
            lname = "Wednesday",
            phoneNumber = "2105556769"
        )

        self.assertTrue(success)
        self.assertEqual(self.baseUser.get_fname(), "Jane")
        self.assertEqual(self.baseUser.get_lname(), "Wednesday")
        self.assertEqual(self.baseUser.get_phoneNumber(), "2105556769")
    
    def test_successful_update_email(self):
        success, msg = self.baseUser.update_profile(
            fname = 'Jane',
            email = 'jane@example.com'
        )

        self.assertTrue(success)
        self.assertEqual(self.baseUser.get_fname(), "Jane")
        self.assertEqual(self.baseUser.get_email(), "jane@example.com")
    
    def test_successful_phone_number_format(self):
        validPhoneNumbers = [
            '1234567890',
            '(123) 456-7890',
            '123-456-7890',
            '123.456.7890',
            '+1 123 456 7890'
        ]

        for phone in validPhoneNumbers:
            with self.subTest(phoneNumber=phone):
                success, msg = self.baseUser.update_profile(phoneNumber=phone)
                self.assertTrue(success, f"Failed for phone: {phone}")
                self.assertEqual(self.baseUser.get_phoneNumber(), phone)
    
    def test_first_name_too_short(self):
        success, msg = self.baseUser.update_profile(fname = "J")

        self.assertFalse(success)
        self.assertIn("First Name must be at least 2 characters long", msg)
        self.assertEqual(self.baseUser.get_fname(), "John")
    
    def test_first_name_too_long(self):
        longName = "JJ" * 50
        success, msg = self.baseUser.update_profile(fname = longName)

        self.assertFalse(success)
        self.assertIn("First Name must be less than 50 characters", msg)

    def test_first_name_invalid_characters(self):
        invalidNames = ["JJ123", "John@Doe", "JJ_Olatunji"]

        for name in invalidNames:
            with self.subTest(name=name):
                success, msg = self.baseUser.update_profile(fname = name)
                self.assertFalse(success)
                self.assertIn("First Name contains invalid characters", msg)
    
    def test_last_name_too_short(self):
        success, msg = self.baseUser.update_profile(lname = "S")

        self.assertFalse(success)
        self.assertIn("Last Name must be at least 2 characters long", msg)
    
    def test_last_name_empty(self):
        success, msg = self.baseUser.update_profile(lname = '')

        self.assertFalse(success)
        self.assertIn("Last Name cannot be empty", msg)

    def test_last_name_whitespace_only(self):
        success, msg = self.baseUser.update_profile(lname = "     ")

        self.assertFalse(success)
        self.assertIn("Last Name cannot be empty", msg)

    def test_phone_number_too_short(self):
        success, msg = self.baseUser.update_profile(phoneNumber = "123")

        self.assertFalse(success)
        self.assertIn("Phone number is too short", msg)

    def test_phone_number_too_long(self):
        longPhone = "123" * 10
        success, msg = self.baseUser.update_profile(phoneNumber=longPhone)

        self.assertFalse(success)
        self.assertIn("Phone number is too long", msg)

    def test_phone_number_invalid_characters(self):
        invalidPhones = ['123-abc-7890', '123-a56.7890', 'my_phone_number']

        for phone in invalidPhones:
            with self.subTest(phone=phone):
                success, msg = self.baseUser.update_profile(phoneNumber=phone)
                self.assertFalse(success)
                self.assertIn("Phone number must contain only digits and common separators", msg)
    
    def test_phone_number_empty(self):
        success, msg = self.baseUser.update_profile(phoneNumber = '')

        self.assertFalse(success)
        self.assertIn("Phone number cannot be empty", msg)

    def test_email_invalid_format(self):
        invalidEmail = ['invalid-email', 'test@', "@gmail.com", 'test@gmail', 'test@.com']

        for email in invalidEmail:
            with self.subTest(email=email):
                success, msg = self.baseUser.update_profile(email = email)
                self.assertFalse(success)
                self.assertIn("Invalid email format", msg)
    
    def test_email_empty(self):
        success, msg = self.baseUser.update_profile(email = '')

        self.assertFalse(success)
        self.assertIn("Email cannot be empty", msg)
    
    def test_multiple_validation_errors(self):
        success, msg = self.baseUser.update_profile(
            fname = 'J',
            lname = '',
            phoneNumber = 'invalid'
        )

        self.assertFalse(success)
        self.assertIn("First Name must be at least 2 characters long", msg)
        self.assertIn("Last Name cannot be empty", msg)
        self.assertIn("Phone number must contain only digits and common separators", msg)

    def test_no_updates_provided(self):
        success, msg = self.baseUser.update_profile()

        self.assertFalse(success)
        self.assertEqual("No valid updates provided", msg)

if __name__ == '__main__':
    unittest.main()