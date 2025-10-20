import unittest
from datetime import date
from User import *
from Money import *
from budget import *


class TestLogin(unittest.TestCase):

    def test_login_success(self):
        users = [
            User("user@example.com", "123", "John", "Doe", "555-1234", date(2025, 10, 20))
        ]

        success, message = User.login_user("user@example.com", "123", users)

        self.assertTrue(success)
        self.assertEqual(message, "Successful login.")

    def test_login_failure_wrong_password(self):
        users = [
            User("user@example.com", "123", "John", "Doe", "555-1234", date(2025, 10, 20))
        ]

        success, message = User.login_user("user@example.com", "wrongpass", users)

        self.assertFalse(success)
        self.assertEqual(message, "Invalid email or password.")

    def test_login_failure_no_user(self):
        users = []
        success, message = User.login_user("nonexistent@example.com", "123", users)

        self.assertFalse(success)
        self.assertEqual(message, "Invalid email or password.")


class TestIncomeManagement(unittest.TestCase):
    
    def test_total_monthly_income(self):
        previousIncome = 5000
        income_sources = []

        income_sources.append(Income(1, 1, "Part-time Job", 500, "weekly", date(2025, 10, 1)))
        income_sources.append(Income(2, 1, "Main Job", 2000, "biweekly", date(2025, 10, 3)))
        income_sources.append(Income(3, 1, "Freelance Work", 800, "monthly", date(2025, 10, 5)))
        income_sources.append(Income(4, 1, "Stock Dividends", 2400, "annual", date(2025, 10, 6)))

        total_income = Income.calculate_total_monthly_income(income_sources, previousIncome)
        
        self.assertIsNotNone(total_income)
        self.assertGreater(total_income, previousIncome)
    
    def test_add_one_time_income(self):
        new_income = Income.add_one_time_income(
            userID=1,
            name="Freelance Project",
            amount=750,
            datePaid=date(2025, 10, 15)
        )

        self.assertEqual(new_income.name, "Freelance Project")
        self.assertEqual(new_income.amount, 750)
        self.assertEqual(new_income.payFrequency, "one time")
    
    def test_one_time_income_multiple(self):
        userID = 1
        totalIncome = 5000

        income1 = Income.add_one_time_income(userID, "Freelance Project", 1200, date(2025, 10, 10))
        income2 = Income.add_one_time_income(userID, "Money Transfer", 300, date(2025, 10, 15))

        totalIncome += income1.amount + income2.amount

        self.assertEqual(totalIncome, 6500)
        self.assertEqual(income1.amount, 1200)
        self.assertEqual(income2.amount, 300)


class TestTransactions(unittest.TestCase):
    
    def test_add_manual_transaction_income(self):
        manager = TransactionManager()
        userID = "user123"

        Income.add_manual_transaction(
            manager, userID, 1200.00, date(2025, 10, 18), 
            payee="Freelance Client", categoryID=1, 
            notes="One-time project payment", expenseType=None
        )

        self.assertEqual(len(manager.transactions), 1)
        self.assertEqual(manager.transactions[0].total, 1200.00)
        self.assertEqual(manager.transactions[0].payee, "Freelance Client")
    
    def test_add_manual_transaction_expense(self):
        manager = TransactionManager()
        userID = "user123"

        transaction = Income.add_manual_transaction(
            manager, userID, 75.50, date(2025, 10, 19), 
            payee="Grocery Store", categoryID=2, 
            notes="Weekly groceries", expenseType=ExpenseType.VARIABLE
        )

        self.assertEqual(len(manager.transactions), 1)
        self.assertEqual(transaction.total, 75.50)
        self.assertEqual(transaction.expenseType, ExpenseType.VARIABLE)
        self.assertEqual(transaction.categoryID, 2)



class TestBudget(unittest.TestCase):
    
    def test_budget_limit_warning(self):
        manager = BudgetManager()

        groceries = Category(1, "Groceries", "variable", 300.0, 0.0, 0.0)
        entertainment = Category(2, "Entertainment", "variable", 150.0, 0.0, 0.0)

        manager.add_category(groceries)
        manager.add_category(entertainment)

        t1 = Transaction(101, "user1", 120.00, date(2025, 10, 1), "Grocery Store", 1, "Weekly groceries", False, None, ExpenseType.VARIABLE)
        t2 = Transaction(102, "user1", 200.00, date(2025, 10, 10), "Grocery Store", 1, "Extra shopping", False, None, ExpenseType.VARIABLE)
        t3 = Transaction(103, "user1", 100.00, date(2025, 10, 15), "Cinema", 2, "Movie night", False, None, ExpenseType.VARIABLE)
        t4 = Transaction(104, "user1", 80.00, date(2025, 10, 20), "Concert", 2, "Music event", False, None, ExpenseType.VARIABLE)

        manager.record_transaction(t1)
        manager.record_transaction(t2)
        manager.record_transaction(t3)
        manager.record_transaction(t4)

        self.assertEqual(len(manager.categories), 2)
    
    def test_category_spending_limit(self):
        category = Category(1, "Dining Out", "Expense", 200, 0, 0)
        
        self.assertEqual(category.name, "Dining Out")
        self.assertEqual(category.categoryLimit, 200)


class TestExpenses(unittest.TestCase):
    
    def test_transportation_expense(self):
        expenses = []
        userID = 1

        bus_pass = add_recurring_transportation_expense(
            expenses,
            userID,
            name="Bus Pass",
            amount=50.0,
            category="Transportation",
            payFrequency="monthly",
            startDate=date(2025, 10, 1)
        )

        expense_records = []
        bus_pass.post_expense(expense_records)
        bus_pass.post_expense(expense_records)

        self.assertEqual(len(expenses), 1)
        self.assertEqual(len(expense_records), 2)
        self.assertEqual(bus_pass.amount, 50.0)
        self.assertEqual(bus_pass.name, "Bus Pass")


if __name__ == "__main__":
    unittest.main()