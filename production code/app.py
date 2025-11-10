from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date, datetime
import json

from budget import *
from Money import *
from Pages import *
from User import User

app = Flask(__name__)
CORS(app)

transactionManager = TransactionManager()
budgetManager = BudgetManager()

sampleBudget = Budget(
    budgetID = 1,
    userID='user1',
    name="Montly Budget",
    totalPlannedAmnt=3000.0,
    month='October',
    income=4500.0
)

sampleCategories = [
    Category(1, "Groceries", "Food", 300, 120, None),
    Category(2, "Rent", "Housing", 1200, 1200, None),
    Category(3, "Utilities", "Bills", 200, 150,  None),
    Category(4, "Entertainment", "Leisure", 150, 90, None)
]

for category in sampleCategories:
    sampleBudget.addCategory(category)
    budgetManager.add_category(category)

sampleTransactions = [
    Transaction(1, "user1", 5.0, date(2025, 10, 1), "Amazon", 1, "Sample note"),
    Transaction(2, "user1", 12.5, date(2025, 10, 2), "Starbucks", 4, "Coffee"),
    Transaction(3, "user1", 35.0, date(2025, 10, 3), "Walmart", 1, "Groceries"),
    Transaction(4, "user1", 18.0, date(2025, 10, 4), "Uber", 3, "Transportation"),
    Transaction(5, "user1", 9.99, date(2025, 10, 5), "Amazon", 4, "Entertainment"),
    Transaction(6, "user1", 27.5, date(2025, 10, 6), "Target", 1, "Household"),
    Transaction(7, "user1", 15.49, date(2025, 10, 7), "Netflix", 4, "Subscription"),
    Transaction(8, "user1", 20.0, date(2025, 10, 8), "Domino's", 1, "Food"),
    Transaction(9, "user1", 2.99, date(2025, 10, 9), "Apple", 4, "App Store")
]

for transaction in sampleTransactions:
    transactionManager.add_transaction(transaction)
    budgetManager.record_transaction(transaction)

dashboard = Dashboard("user1", transactionManager)

#API Calls
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        recentTransactions = dashboard.get_recent_transactions_widget_data(10)

        totalSpending = sum(transaction.total for transaction in transactionManager.transactions)

        return jsonify({
            'income': sampleBudget.income,
            'expenses': totalSpending,
            'recentTransactions': recentTransactions,
            'budgets': [{
                'id': cat.categoryID,
                'name': cat.name,
                'total': cat.categoryLimit,
                'spent': budgetManager.spending.get(cat.categoryID, 0.0)
            } for cat in sampleBudget.categories]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        sortBy = request.args.get('sort', 'date')
        transactions = dashboard.get_recent_transaction(50)
        
        transactionsData = []
        for transaction in transactions:
            transactionsData.append({
                'id': transaction.transactionID,
                'payee': transaction.payee,
                'amount': transaction.total,
                'date': transaction.date.isoformat(),
                'categoryID': transaction.categoryID,
                'notes': transaction.notes
            })
        
        return jsonify(transactionsData)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        
        # Create new transaction
        newTransaction = Transaction(
            transactionID=len(transactionManager.transactions) + 1,
            userID="user1",
            total=float(data['amount']),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            payee=data['payee'],
            categoryID=int(data.get('categoryID', 1)),
            notes=data.get('notes', ''),
            isRecurring=False,
            expenseType=ExpenseType.VARIABLE
        )
        
        transactionManager.add_transaction(newTransaction)
        budgetManager.record_transaction(newTransaction)
        
        return jsonify({'message': 'Transaction added successfully', 'id': newTransaction.transactionID})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    try:
        budgetData = sampleBudget.get_budget_data()
        
        # Add spending data from budget manager
        for category in budgetData['categories']:
            category['spent'] = budgetManager.spending.get(category['categoryID'], 0.0)
        
        return jsonify(budgetData)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spending-chart', methods=['GET'])
def get_spending_chart():
    try:
        chart_data = budgetManager.get_chart_data()
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expense-stats', methods=['GET'])
def get_expense_stats():
    try:
        stats = transactionManager.get_expense_type_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)