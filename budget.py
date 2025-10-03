from typing import List

class Budget:
    def __init__(self, budgetID: int, userID: str, name: str, totalPlannedAmnt: float, month: str):
        self.budgetID = budgetID
        self.userID = userID
        self.name = name
        self.totalPlannedAmnt = totalPlannedAmnt
        self.month = month
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


class Category:
    def __init__(self, categoryID: int, name: str, type_: str, categoryLimit: float, plannedAmnt: float):
        self.categoryID = categoryID
        self.name = name
        self.type = type_
        self.categoryLimit = categoryLimit
        self.plannedAmnt = plannedAmnt

    def addCategory(self):
        print(f"Category '{self.name}' added.")

    def editCategory(self, name: str = None, type_: str = None):
        self.name = name
        self.type = type_
        print(f"Category {self.categoryID} updated.")

    def deleteCategory(self):
        print(f"Category {self.categoryID} deleted.")

    def editLimit(self, newLimit: float):
        self.categoryLimit = newLimit
        print(f"Category {self.categoryID} limit updated to {newLimit}")

    def setPlannedAmnt(self, amount: float):
        self.plannedAmnt = amount
        print(f"Category {self.categoryID} planned amount set to {amount}")


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
