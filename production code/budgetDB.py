import mysql.connector
from budget import *

#entire class for budget database.
class BudgetDB:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    # Function used to create a new budget.
    def create_budget(self, budget: 'Budget'):
        sql = """
        INSERT INTO bankBudget (userID, Name, totalPlanned, month, income)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (budget.userID, budget.name, budget.totalPlannedAmnt, budget.month, budget.income)
        for category in budget.categories:
            self.create_category(category, budget.budgetID)

        self.cursor.execute(sql, values)
        self.db.commit()

        budget.budgetID = self.cursor.lastrowid
        return budget.budgetID

    # Function used to load budgets for a specific user.
    def load_budgets_for_user(self, userID: str):
        sql = """
        SELECT idbankBudget, Name, totalPlanned, month, income
        FROM bankBudget
        WHERE userID = %s
        """
        self.cursor.execute(sql, (userID,))
        results = self.cursor.fetchall()

        budgets = []
        for row in results:
            budget = Budget(
                budgetID=row[0],
                userID=userID,
                name=row[1],
                totalPlannedAmnt=row[2],
                month=row[3],
                income=row[4]
            )

            # Load categories for this budget
            categories = self.load_categories_for_budget(budget.budgetID)
            budget.categories.extend(categories)

            budgets.append(budget)

        return budgets

    # Function used to update a budgets.
    def update_budget(self, old_name, user_id, new_name, new_month, new_planned):
        cursor = self.db.cursor()
        query = """
            UPDATE bankBudget
            SET name=%s, month=%s, totalPlannedAmnt=%s
            WHERE userID=%s AND name=%s
        """
        cursor.execute(query, (new_name, new_month, new_planned, user_id, old_name))
        self.db.commit()

    # function used to delete a budget.
    def delete_budget(self, budgetID: int):
        sql = "DELETE FROM bankBudget WHERE idbankBudget = %s"
        self.cursor.execute(sql, (budgetID,))
        self.db.commit()

    #These functions will be used for category management for the budget.

    #function used to create a new category.
    def create_category(self, category: 'Category', budgetID: int):

        sql = """
        INSERT INTO bankCategory (budgetID, name, type, plannedAmnt, plannedPerc, categoryLimit)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            budgetID,
            category.name,
            category.type,
            category.plannedAmnt,
            category.plannedPercentage,
            category.categoryLimit
        )

        self.cursor.execute(sql, values)
        self.db.commit()

        category.categoryID = self.cursor.lastrowid
        return category.categoryID


    # function used to load categories for a specific budget.
    def load_categories_for_budget(self, budgetID: int):
        sql = """
        SELECT idbankCategory, name, type, plannedAmnt, plannedPerc, categoryLimit
        FROM bankCategory WHERE budgetID = %s
        """

        self.cursor.execute(sql, (budgetID,))
        results = self.cursor.fetchall()

        categories = []
        for row in results:
            category = Category(
                categoryID=row[0],
                name=row[1],
                type_=row[2],
                plannedAmnt=row[3],
                plannedPercentage=row[4],
                categoryLimit=row[5]
            )
            categories.append(category)
        return categories


    # Function used to update a category.
    def update_category(self, category: 'Category'):
        sql = """
        UPDATE bankCategory
        SET name=%s, type=%s, plannedAmnt=%s, plannedPerc=%s, categoryLimit=%s
        WHERE idbankCategory=%s
        """
        values = (
            category.name,
            category.type,
            category.plannedAmnt,
            category.plannedPercentage,
            category.categoryLimit,
            category.categoryID
        )

        self.cursor.execute(sql, values)
        self.db.commit()


    # Delete a category
    def delete_category(self, categoryID: int):
        sql = "DELETE FROM bankCategory WHERE idbankCategory=%s"
        self.cursor.execute(sql, (categoryID,))
        self.db.commit()