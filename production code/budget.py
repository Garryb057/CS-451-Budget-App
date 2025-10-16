from typing import List, Optional

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
