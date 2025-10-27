import unittest
from datetime import date
from User import *
from Money import *
from budget import *
from Pages import *


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

#Sprint 4 tests start from here
class TestBudgetEditing(unittest.TestCase):
    
    def setUp(self):
        self.budget = Budget(1, "user123", "October Budget", 1000.0, "2025-10", 5000.0)
        
        self.cat1 = Category(1, "Groceries", "variable", 400.0, 300.0, None)
        self.cat2 = Category(2, "Entertainment", "variable", 200.0, 150.0, None)
        self.cat3 = Category(3, "Utilities", "fixed", 300.0, 250.0, None)
        
        self.budget.addCategory(self.cat1)
        self.budget.addCategory(self.cat2)
        self.budget.addCategory(self.cat3)
    
    def test_get_budget_data(self):
        data = self.budget.get_budget_data()
        
        self.assertEqual(data['budgetID'], 1)
        self.assertEqual(data['name'], "October Budget")
        self.assertEqual(len(data['categories']), 3)
        self.assertEqual(data['categories'][0]['name'], "Groceries")
    
    def test_update_category_amount(self):
        original_total = self.budget.totalPlannedAmnt
        
        success = self.budget.update_category_amount(1, 350.0)
        
        self.assertTrue(success)
        self.assertEqual(self.cat1.plannedAmnt, 350.0)
        self.assertNotEqual(self.budget.totalPlannedAmnt, original_total)
    
    def test_update_category_amount_invalid_id(self):
        success = self.budget.update_category_amount(999, 100.0)
        
        self.assertFalse(success)
    
    def test_total_updates_automatically(self):
        self.budget.update_category_amount(1, 400.0)
        self.budget.update_category_amount(2, 200.0)
        
        expected_total = 400.0 + 200.0 + 250.0
        self.assertEqual(self.budget.totalPlannedAmnt, expected_total)
    
    def test_validate_budget_changes(self):
        is_valid, message = self.budget.validate_budget_changes()
        
        self.assertTrue(is_valid)
        self.assertEqual(message, "Budget is valid")
    
    def test_validate_budget_negative_amount(self):
        self.cat1.plannedAmnt = -100.0
        
        is_valid, message = self.budget.validate_budget_changes()
        
        self.assertFalse(is_valid)
        self.assertIn("cannot have negative amount", message)
    
    def test_discard_changes(self):
        original_data = self.budget.get_budget_data()
        
        # Make changes
        self.budget.update_category_amount(1, 500.0)
        self.budget.name = "Modified Budget"
        
        # Discard changes
        self.budget.discard_changes(original_data)
        
        self.assertEqual(self.budget.name, "October Budget")
        self.assertEqual(self.cat1.plannedAmnt, 300.0)
    
    def test_save_budget_changes(self):
        self.budget.update_category_amount(1, 350.0)
        
        success, message = self.budget.save_budget_changes()
        
        self.assertTrue(success)
        self.assertEqual(message, "Budget saved successfully")


class TestSpendingCharts(unittest.TestCase):
    
    def setUp(self):
        self.manager = TransactionManager()
        
        # Add test transactions across different months
        self.manager.add_transaction(
            Transaction(1, "user1", 120.0, date(2025, 10, 5), "Grocery Store", 1, 
                       "Groceries", False, None, ExpenseType.VARIABLE)
        )
        self.manager.add_transaction(
            Transaction(2, "user1", 50.0, date(2025, 10, 15), "Cinema", 2, 
                       "Movie", False, None, ExpenseType.VARIABLE)
        )
        self.manager.add_transaction(
            Transaction(3, "user1", 200.0, date(2025, 9, 10), "Grocery Store", 1, 
                       "Groceries", False, None, ExpenseType.VARIABLE)
        )
    
    def test_get_transactions_by_date_range(self):
        start = date(2025, 10, 1)
        end = date(2025, 10, 31)
        
        transactions = self.manager.get_transactions_by_date_range(start, end)
        
        self.assertEqual(len(transactions), 2)
    
    def test_get_monthly_spending_chart_data(self):
        chart_data = self.manager.get_monthly_spending_chart_data(2025, 10)
        
        self.assertEqual(chart_data['period'], "2025-10")
        self.assertIn('spending', chart_data)
        self.assertIn(1, chart_data['spending'])  # Category 1 should have spending
    
    def test_get_yearly_spending_chart_data(self):
        chart_data = self.manager.get_yearly_spending_chart_data(2025)
        
        self.assertEqual(chart_data['period'], "2025")
        self.assertIn('total_spending', chart_data)
        self.assertIn('monthly_breakdown', chart_data)
        self.assertEqual(len(chart_data['monthly_breakdown']), 12)
    
    def test_get_category_transactions(self):
        transactions = self.manager.get_category_transactions(1)
        
        self.assertEqual(len(transactions), 2)
        for t in transactions:
            self.assertEqual(t.categoryID, 1)
    
    def test_get_category_detail_view(self):
        detail = self.manager.get_category_detail_view(1)
        
        self.assertEqual(detail['categoryID'], 1)
        self.assertEqual(detail['transaction_count'], 2)
        self.assertEqual(detail['total_spent'], 320.0)
        self.assertEqual(len(detail['transactions']), 2)
    
    def test_get_spending_by_category_period(self):
        start = date(2025, 10, 1)
        end = date(2025, 10, 31)
        
        spending = self.manager.get_spending_by_category_period(start, end)
        
        self.assertIn(1, spending)
        self.assertIn(2, spending)
        self.assertEqual(spending[1], 120.0)
        self.assertEqual(spending[2], 50.0)


class TestDashboardCharts(unittest.TestCase):
    
    def setUp(self):
        self.dashboard = Dashboard("user123")
    
    def test_get_spending_chart_data_monthly(self):
        chart_data = self.dashboard.get_spending_chart_data('monthly', 2025, 10)
        
        self.assertEqual(chart_data['view_type'], 'monthly')
        self.assertEqual(chart_data['year'], 2025)
        self.assertEqual(chart_data['month'], 10)
    
    def test_get_spending_chart_data_yearly(self):
        chart_data = self.dashboard.get_spending_chart_data('yearly', 2025)
        
        self.assertEqual(chart_data['view_type'], 'yearly')
        self.assertEqual(chart_data['year'], 2025)
        self.assertIsNone(chart_data['month'])
    
    def test_switch_chart_view(self):
        chart_data = self.dashboard.switch_chart_view('yearly', 2025)
        
        self.assertEqual(chart_data['view_type'], 'yearly')
    
    def test_switch_chart_view_invalid(self):
        with self.assertRaises(ValueError):
            self.dashboard.switch_chart_view('weekly')
    
    def test_persist_chart_preference(self):
        success = self.dashboard.persist_chart_preference('yearly')
        
        self.assertTrue(success)
    
    def test_get_user_chart_preference(self):
        preference = self.dashboard.get_user_chart_preference()
        
        self.assertIn(preference, ['monthly', 'yearly'])
    
    def test_get_category_drill_down(self):
        start = date(2025, 10, 1)
        end = date(2025, 10, 31)
        
        detail = self.dashboard.get_category_drill_down(1, start, end)
        
        self.assertEqual(detail['categoryID'], 1)
        self.assertEqual(detail['period_start'], start)
        self.assertEqual(detail['period_end'], end)


class TestBudgetManagerCharts(unittest.TestCase):
    
    def setUp(self):
        self.manager = BudgetManager()
        
        cat1 = Category(1, "Groceries", "variable", 300.0, 0.0, 0.0)
        cat2 = Category(2, "Entertainment", "variable", 150.0, 0.0, 0.0)
        
        self.manager.add_category(cat1)
        self.manager.add_category(cat2)
        
        t1 = Transaction(1, "user1", 120.0, date(2025, 10, 1), "Store", 1)
        t2 = Transaction(2, "user1", 75.0, date(2025, 10, 5), "Cinema", 2)
        
        self.manager.record_transaction(t1)
        self.manager.record_transaction(t2)
    
    def test_get_spending_by_category(self):
        spending = self.manager.get_spending_by_category()
        
        self.assertIn("Groceries", spending)
        self.assertIn("Entertainment", spending)
        self.assertEqual(spending["Groceries"]['amount'], 120.0)
        self.assertEqual(spending["Entertainment"]['amount'], 75.0)
    
    def test_get_chart_data(self):
        chart_data = self.manager.get_chart_data('current_month')
        
        self.assertIn('labels', chart_data)
        self.assertIn('amounts', chart_data)
        self.assertEqual(len(chart_data['labels']), 2)
        self.assertEqual(chart_data['period'], 'current_month')
    
    def test_get_chart_data_excludes_zero_spending(self):
        cat3 = Category(3, "Savings", "fixed", 500.0, 0.0, 0.0)
        self.manager.add_category(cat3)
        
        chart_data = self.manager.get_chart_data()
        
        self.assertEqual(len(chart_data['labels']), 2)

if __name__ == "__main__":
    unittest.main()