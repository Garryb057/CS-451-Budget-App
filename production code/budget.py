from typing import List, Optional
from Money import *

class Budget:
    def __init__(self, budgetID: int, userID: str, name: str, totalPlannedAmnt: float, month: str, income: float):
        self.budgetID = budgetID
        self.userID = userID
        self.name = name
        self.totalPlannedAmnt = totalPlannedAmnt
        self.month = month
        self.income = income
        self.categories = []

    def createBudget(self):
        print(f"Budget '{self.name}' created with id {self.budgetID}")

    def editBudget(self, name: str = None, totalPlannedAmnt: float = None, month: str = None):
        if name: self.name = name
        if totalPlannedAmnt: self.totalPlannedAmnt = totalPlannedAmnt
        if month: self.month = month
        print(f"Budget {self.name} updated.")

    def deleteBudget(self):
        #Future implementation
        print(f"Budget {self.name} deleted.")
        self.remove(self.budgetID)

    def calculateTotalPlannedAmnt(self):
        self.totalPlannedAmnt = sum(cat.plannedAmnt for cat in self.categories)
        return self.totalPlannedAmnt

    def budgetTracking(self):
        print(f"{self.name} total planned = {self.totalPlannedAmnt}")

    def addCategory(self, category: 'Category'):
        self.categories.append(category)
        self.calculateTotalPlannedAmnt()
        print(f"Category '{category.name}' added to budget '{self.name}'")

    def editCategory(self, categoryID: int, name: str = None, type: str = None, 
                     plannedAmnt: float = None, plannedPercentage: float = None):
        category = self.getCategoryByID(categoryID)
        if category:
            if name: category.name = name
            if type: category.type = type
            if plannedAmnt is not None:
                category.plannedAmnt = plannedAmnt
                category.plannedPercentage = None
            if plannedPercentage is not None and self.income > 0.0:
                category.plannedAmnt = (plannedPercentage / 100) * self.income
                category.plannedPercentage = plannedPercentage
            
            self.calculateTotalPlannedAmnt()
            print(f"Category {categoryID} updated")
        else:
            print(f"Category with ID {categoryID} not found.")

    def deleteCategory(self, categoryID: int):
        category = self.getCategoryByID
        if category:
            self.categories.remove(category)
            self.calculateTotalPlannedAmnt()
            print(f"Category {categoryID} deleted.")
        else:
            print(f"Category with ID {categoryID} not found.")
    
    def getCategoryByID(self, categoryID: int) -> Optional['Category']:
        return next((cat for cat in self.categories if cat.categoryID == categoryID), None)
    
    def setIncome(self, income: float):
        self.income = income
        for category in self.categories:
            if category.plannedPercentage is not None:
                category.plannedAmnt = (category.plannedPercentage / 100) * income
            self.calculateTotalPlannedAmnt()
    
    def get_budget_data(self) -> dict:
        return {
        'budgetID': self.budgetID,
        'name': self.name,
        'totalPlannedAmnt': self.totalPlannedAmnt,
        'month': self.month,
        'income': self.income,
        'categories': [
            {
                'categoryID': cat.categoryID,
                'name': cat.name,
                'type': cat.type,
                'plannedAmnt': cat.plannedAmnt,
                'plannedPercentage': cat.plannedPercentage
            } for cat in self.categories
        ]
    }

    #==========Part of sprint 4 by Temka, for the Budget user story.============
    def update_category_amount(self, categoryID: int, newAmount: float) -> bool:
        category = self.getCategoryByID(categoryID)
        if category:
            category.plannedAmnt = newAmount
            category.plannedPercentage = None
            self.calculateTotalPlannedAmnt()
            print(f"Category '{category.name}' amount updated to ${newAmount:.2f}")
            return True
        else:
            print(f"Category with ID {categoryID} not found.")
            return False

    def validate_budget_changes(self) -> tuple[bool, str]:
        if self.totalPlannedAmnt < 0:
            return False, "Total planned amount cannot be negative"
        if not self.categories:
            return False, "Budget must have at least one category"
        for cat in self.categories:
            if cat.plannedAmnt < 0:
                return False, f"Category '{cat.name}' cannot have negative amount"
        return True, "Budget is valid"

    def save_budget_changes(self) -> tuple[bool, str]:
        is_valid, message = self.validate_budget_changes()
        if not is_valid:
            return False, message
        # Future implementation: save to database
        print(f"Budget '{self.name}' changes saved successfully")
        return True, "Budget saved successfully"

    def discard_changes(self, original_data: dict):
        self.name = original_data['name']
        self.totalPlannedAmnt = original_data['totalPlannedAmnt']
        self.month = original_data['month']
        self.income = original_data['income']
        for cat_data in original_data['categories']:
            category = self.getCategoryByID(cat_data['categoryID'])
            if category:
                category.plannedAmnt = cat_data['plannedAmnt']
                category.plannedPercentage = cat_data['plannedPercentage']
        print(f"Budget '{self.name}' changes discarded")
    #==========End of part of sprint 4 by Temka, for the Budget user story.============
    
class Category:
    def __init__(self, categoryID: int, name: str, type_: str, categoryLimit: float, plannedAmnt: float, plannedPercentage: float):
        self.categoryID = categoryID
        self.name = name
        self.type = type_
        self.categoryLimit = categoryLimit
        self.plannedAmnt = plannedAmnt
        self.plannedPercentage = plannedPercentage

    def addCategory(self):
        print(f"Category '{self.name}' added.")

    def editCategory(self, name: str = None, type_: str = None, plannedAmnt: float = None, plannedPercentage: float = None):
        if name: self.name = name
        if type_: self.type = type_
        if plannedAmnt is not None:
            self.plannedAmnt = plannedAmnt
            self.plannedPercentage = None
        if plannedPercentage is not None:
            self.plannedPercentage = plannedPercentage
        print(f"Category {self.categoryID} updated.")

    def deleteCategory(self):
        print(f"Category {self.categoryID} deleted.")

    def editLimit(self, newLimit: float):
        self.categoryLimit = newLimit
        print(f"Category {self.categoryID} limit updated to {newLimit}")

    def setPlannedAmnt(self, amount: float):
        self.plannedAmnt = amount
        self.plannedPercentage = None
        print(f"Category {self.categoryID} planned amount set to {amount}")

    def setPlannedPercentage(self, percentage: float, budgetIncome: float):
        self.plannedPercentage = percentage
        self.plannedAmnt = (percentage / 100) * budgetIncome
        print(f"Category {self.categoryID} planned percentage set to {percentage}% (${self.plannedAmnt:.2f})")

#Part of sprint 1 by Temka
class BudgetTemplate:
    def __init__(self, templateID: int, name: str, description: str, categories: List[Category] = None):
        self.templateID = templateID
        self.name = name
        self.description = description
        self.categories = categories if categories else []

    def createBudgetFromTemplate(self, budgetID: int, userID: str, month: str):
        #Future implementation
        new_budget = Budget(budgetID, userID, self.name, 0.0, month)
        new_budget.categories = [Category(cat.categoryID, cat.name, cat.type, cat.categoryLimit, cat.plannedAmnt) 
                                 for cat in self.categories]
        new_budget.calculateTotalPlannedAmnt()
        print(f"Budget created from template '{self.name}' for user {userID}")
        return new_budget

#Part of sprint 3 by Temka
class BudgetManager:
    def __init__(self):
        self.categories: dict[int, Category] = {}      
        self.spending: dict[int, float] = {}           

    def add_category(self, category: Category):
        if category.categoryID not in self.categories:
            self.categories[category.categoryID] = category
            self.spending[category.categoryID] = 0.0
            print(f"Category '{category.name}' added with limit ${category.categoryLimit:.2f}")
        else:
            print(f"Category '{category.name}' already exists.")

    def record_transaction(self, transaction: Transaction):
        cat_id = transaction.categoryID

        if cat_id not in self.categories:
            print(f"Transaction {transaction.transactionID} uses an unknown category (ID {cat_id}).")
            return

        amount = transaction.total
        self.spending[cat_id] += amount
        category = self.categories[cat_id]

        print(f"Added ${amount:.2f} to '{category.name}'. "
              f"Total spent: ${self.spending[cat_id]:.2f} / ${category.categoryLimit:.2f}")

        if self.spending[cat_id] > category.categoryLimit:
            print(f"WARNING: You’ve exceeded your monthly limit for '{category.name}'!\n")

    def get_summary(self):
        print("\nBudget Summary:")
        for cat_id, category in self.categories.items():
            spent = self.spending.get(cat_id, 0.0)
            status = "Over Limit!" if spent > category.categoryLimit else "Within Limit"
            print(f"  - {category.name}: ${spent:.2f} / ${category.categoryLimit:.2f} ({status})")

    #==Part of sprint 4 by Temka==
    def get_spending_by_category(self, start_date: date = None, end_date: date = None) -> dict:
        category_totals = {}
        
        for cat_id, category in self.categories.items():
            spent = self.spending.get(cat_id, 0.0)
            category_totals[category.name] = {
                'amount': spent,
                'categoryID': cat_id,
                'limit': category.categoryLimit
            }
        
        return category_totals

    def get_chart_data(self, period: str = 'current_month') -> dict:
        spending_data = self.get_spending_by_category()
        
        chart_data = {
            'labels': [],
            'amounts': [],
            'colors': [],
            'period': period
        }
        
        for category_name, data in spending_data.items():
            if data['amount'] > 0:  # Only include categories with spending
                chart_data['labels'].append(category_name)
                chart_data['amounts'].append(data['amount'])
        
        return chart_data
    #==Part of sprint 4 by Temka==


    