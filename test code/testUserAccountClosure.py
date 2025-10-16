import unittest
from User import User

class TestUserAccountClosure(unittest.TestCase):
    def setUp(self):
        self.baseUser = User(
            email="test@example.com",
            passwordHash="Passhash123",
            fname = "John",
            lname = "Doe",
            phoneNumber = "9135552929",
            dateCreated = "2025-10-01"
        )
    
    def test_successful_account_closure(self):
        user = self.baseUser
        user.balance = 0.0
        user.disputes = []

        success, msg = user.delete()

        self.assertTrue(success)
        self.assertEqual(msg, "Account successfully closed.")
        self.assertFalse(user.isActive)

    def test_account_closure_positive_balance(self):
        user = self.baseUser
        user.balance = 50.0
        user.disputes = []

        success, msg = user.delete()

        self.assertTrue(success)
        self.assertEqual(msg, "Account successfully closed.")
        self.assertFalse(user.isActive)

    def test_account_closure_negative_balance(self):
        user = self.baseUser
        user.balance = -50.0
        user.disputes = []

        success, msg = user.delete()

        self.assertFalse(success)
        self.assertIn("negative balance", msg)
        self.assertIn("Cannot close account due to", msg)
        self.assertTrue(user.isActive)
    
    def test_account_closure_pending_disputes(self):
        user = self.baseUser
        user.balance = 0.0
        user.add_dispute(1, "Test dispute", "pending")

        success, msg = user.delete()

        self.assertFalse(success)
        self.assertIn("pending disputes", msg)
        self.assertIn("Cannot close account due to", msg)
        self.assertTrue(user.isActive)

    def test_account_closure_negative_balance_pending_disputes(self):
        user = self.baseUser
        user.balance = -50.0
        user.add_dispute(1, "Test dispute", "pending")

        success, msg = user.delete()

        self.assertFalse(success)
        self.assertIn("negative balance", msg)
        self.assertIn("pending disputes", msg)
        self.assertIn("Cannot close account due to", msg)
        self.assertTrue(user.isActive)

    def test_account_closure_resolved_disputes(self):
        user = self.baseUser
        user.balance = 0.0
        user.add_dispute(1, "Resolved dispute", "resolved")

        success, msg = user.delete()

        self.assertTrue(success)
        self.assertEqual(msg, "Account successfully closed.")
        self.assertFalse(user.isActive)
    
    def test_account_closure_multiple_disputes(self):
        user = self.baseUser
        user.balance = 0.0
        user.add_dispute(1, "Test dispute", "pending")
        user.add_dispute(2, "Resolved dispute", "resolved")
        user.add_dispute(3, "Closed dispute", "closed")

        success, msg = user.delete()

        self.assertFalse(success)
        self.assertIn("pending disputes", msg)
        self.assertIn("Cannot close account due to", msg)
        self.assertTrue(user.isActive)

    def test_has_pending_disputes(self):
        user = self.baseUser
        user.add_dispute(1, "Test dispute", "pending")

        self.assertTrue(user.has_pending_disputes())

    def test_has_pending_dispute_resolved(self):
        user = self.baseUser
        user.add_dispute(1, "Test dispute", "resolved")

        self.assertFalse(user.has_pending_disputes())
    
    def test_has_pending_disputes_closed(self):
        user = self.baseUser
        user.add_dispute(1, "Test dispute", "closed")

        self.assertFalse(user.has_pending_disputes())

    def test_has_pending_disputes_none(self):
        user = self.baseUser
        user.disputes = []

        self.assertFalse(user.has_pending_disputes())

    def test_validate_deleteion_prereq(self):
        user = self.baseUser
        user.balance = 0.0
        user.disputes = []

        prereqsMet, msg = user.validate_deletion_prereq()

        self.assertTrue(prereqsMet)
        self.assertEqual(msg, "All prerequisities met. Account can be closed.")

    def test_validate_deletion_prereq_negative_balance(self):
        user = self.baseUser
        user.balance = -50.0
        user.disputes = []

        prereqsMet, msg = user.validate_deletion_prereq()

        self.assertFalse(prereqsMet)
        self.assertIn("negative balance", msg)
        self.assertNotIn("pending disputes", msg)

    def test_validate_deletion_prereq_pending_disputes(self):
        user = self.baseUser
        user.balance = 0.0
        user.add_dispute(1, "Test dispute", "pending")

        prereqsMet, msg = user.validate_deletion_prereq()

        self.assertFalse(prereqsMet)
        self.assertIn("pending disputes", msg)
        self.assertNotIn("negative balance", msg)

    def test_validate_deletion_prereq_pending_disputes_negative_balance(self):
        user = self.baseUser
        user.balance = -5.0
        user.add_dispute(1, "Test dispute", "pending")

        prereqsMet, msg = user.validate_deletion_prereq()

        self.assertFalse(prereqsMet)
        self.assertIn("pending disputes", msg)
        self.assertIn("negative balance", msg)

    def test_update_dispute_status(self):
        user = self.baseUser
        user.balance = 0.0
        user.add_dispute(1, "Test dispute", "pending")

        successBefore, _ = user.delete()

        user.update_dispute_status(1, "resolved")

        successAfter, msgAfter = user.delete()

        self.assertFalse(successBefore)
        self.assertTrue(successAfter)
        self.assertEqual(msgAfter, "Account successfully closed.")
        self.assertFalse(user.isActive)

if __name__ == '__main__':
    unittest.main()