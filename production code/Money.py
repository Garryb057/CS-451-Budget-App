from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional, Tuple

class ExpenseType(Enum):
    FIXED = "fixed"
    VARIABLE = "variable"

class Transaction:
    def __init__ (self, transactionID: int, userID: str, total: float, date: date, 
                  payee: str, categoryID: int, notes: str = "", isRecurring: bool = False, 
                  dateRecurr: date = None, expenseType: ExpenseType = None):
        self.transactionID = transactionID
        self.userID = userID
        self.total = total
        self.date = date
        self.payee = payee
        self.categoryID = categoryID
        self.notes = notes
        self.isRecurring = isRecurring
        self.dateRecurr = dateRecurr
        self.expenseType = expenseType

    #getters
    def get_transactionID(self):
        return self.transactionID
    def get_userID(self):
        return self.userID
    def get_total(self):
        return self.total
    def get_date(self):
        return self.date
    def get_payee(self):
        return self.payee
    def get_categoryID(self):
        return self.categoryID
    def get_notes(self):
        return self.notes
    def get_isRecurring(self):
        return self.isRecurring
    def get_dateRecurr(self):
        return self.dateRecurr
    def get_expenseType(self):
        return self.expenseType
    
    #setters
    def set_transactionID(self, transactionID):
        self.transactionID = transactionID
    def set_userID(self, userID):
        self.userID = userID
    def set_total (self, total):
        self.total = total
    def set_date (self, date):
        self.date = date
    def set_payee (self, payee):
        self.payee = payee
    def set_categoryID (self, categoryID):
        self.categoryID = categoryID
    def set_notes (self, notes):
        self.notes = notes
    def set_isRecurring (self, isRecurring):
        self.isRecurring = isRecurring
    def set_dateRecurr (self, dateRecurr):
        self.dateRecurr = dateRecurr
    def set_expenseType(self, expenseType: ExpenseType):
        self.expenseType = expenseType
    
    def add_transaction(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def delete_transaction(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def edit_transaction(self, total: float = None, date: date = None, payee: str = None,
                         categoryID: int = None, notes: str = None, expenseType: ExpenseType = None):
        if total: self.total = total
        if date: self.date = date
        if payee: self.payee = payee
        if categoryID: self.categoryID = categoryID
        if notes: self.notes = notes
        if expenseType: self.expenseType = expenseType
    def flag_expense_type(self, expenseType: ExpenseType):
        self.expenseType = expenseType
        print(f"Transaction {self.transactionID} tagged as {expenseType.value} expense")



class TransactionManager:
    def __init__(self):
        self.transactions: List[Transaction] = []
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
    def get_transactions_by_expense_type(self, expenseType: ExpenseType) -> List[Transaction]:
        return [t for t in self.transactions if t.expenseType == expenseType]
    def get_recent_transactions(self, userID: str, limit: int = 10) -> List[Transaction]:
        userTransactions = [t for t in self.transactions if t.userID == userID]

        userTransactions.sort(key=lambda t: t.date, reverse=True)
        return userTransactions[:limit]
    def get_transaction_by_id(self, transactionID: int) -> Optional[Transaction]:
        for transaction in self.transactions:
            if transaction.transactionID == transactionID:
                return transaction
            return None
    def get_expense_type_summary(self) -> dict:
        fixedTotal = sum(t.total for t in self.transactions if t.expenseType == ExpenseType.FIXED)
        variableTotal = sum(t.total for t in self.transactions if t.expenseType == ExpenseType.VARIABLE)
        untaggedTotal = sum(t.total for t in self.transactions if t.expenseType is None)

        return{
            ExpenseType.FIXED: fixedTotal,
            ExpenseType.VARIABLE: variableTotal,
            "untagged": untaggedTotal,
            "total_expenses": fixedTotal + variableTotal + untaggedTotal
        }
    def get_expense_type_breakdown(self, expenseType: ExpenseType = None) -> List[dict]:
        transactions = self.transactions
        if expenseType:
            transactions = self.get_transactions_by_expense_type(expenseType)
        
        breakdown = []
        for transaction in transactions:
            breakdown.append({
                'transactionID': transaction.transactionID,
                'date': transaction.date,
                'payee': transaction.payee,
                'total': transaction.total,
                'expenseType': transaction.expenseType.value if transaction.expenseType else 'untagged',
                'categoryID': transaction.categoryID,
                'notes': transaction.notes,
                'isRecurring': transaction.isRecurring
            })
        return breakdown
    def calculate_future_expenses(self, months: int = 3) -> dict:
        currentDate = date.today()
        futureExpenses = {}

        fixedExpenses = self.get_transactions_by_expense_type(ExpenseType.FIXED)
        monthlyFixed = sum(t.total for t in fixedExpenses if t.isRecurring)

        variableExpenses = self.get_transactions_by_expense_type(ExpenseType.VARIABLE)
        if variableExpenses:
            monthlyTotals = {}
            for transaction in variableExpenses:
                monthKey = (transaction.date.year, transaction.date.month)
                monthlyTotals[monthKey] = monthlyTotals.get(monthKey, 0) + transaction.total

            avgVariable = sum(monthlyTotals.values()) / len(monthlyTotals) if monthlyTotals else 0
        else:
            avgVariable = 0
        
        for i in range(months):
            nextMonth = currentDate.replace(month=currentDate.month + i)
            if nextMonth.month > 12:
                nextMonth = nextMonth.replace(year=nextMonth.year + 1, month=nextMonth.month - 12)
            futureExpenses[nextMonth.strftime("%Y-%m")] = {
                'fixed': monthlyFixed,
                'variable': avgVariable,
                'total': monthlyFixed + avgVariable
            }
        return futureExpenses
    def get_expense_type_stats(self) -> dict:
        summary = self.get_expense_type_summary()
        totalExpenses = summary['total_expenses']

        if totalExpenses > 0:
            fixedPercentage = (summary[ExpenseType.FIXED] / totalExpenses) * 100
            variablePercentage = (summary[ExpenseType.VARIABLE] / totalExpenses) * 100
        else:
            fixedPercentage = variablePercentage = 0
        
        return {
            'fixed_amount': summary[ExpenseType.FIXED],
            'variable_amount': summary[ExpenseType.VARIABLE],
            'fixed_percentage': round(fixedPercentage, 2),
            'variable_percentage': round(variablePercentage, 2),
            'total_expenses': totalExpenses,
            'fixed_count': len(self.get_transactions_by_expense_type(ExpenseType.FIXED)),
            'variable_count': len(self.get_transactions_by_expense_type(ExpenseType.VARIABLE))
        }
    
    #====Part of sprint 4 by Temka====
    def get_transactions_by_date_range(self, start_date: date, end_date: date) -> List[Transaction]:
        return [t for t in self.transactions 
                if start_date <= t.date <= end_date]

    def get_spending_by_category_period(self, start_date: date, end_date: date) -> dict:
        transactions = self.get_transactions_by_date_range(start_date, end_date)
        category_spending = {}
        
        for transaction in transactions:
            cat_id = transaction.categoryID
            if cat_id not in category_spending:
                category_spending[cat_id] = 0.0
            category_spending[cat_id] += transaction.total
        
        return category_spending

    def get_monthly_spending_chart_data(self, year: int, month: int) -> dict:
        from calendar import monthrange
        
        start_date = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        end_date = date(year, month, last_day)
        
        spending = self.get_spending_by_category_period(start_date, end_date)
        
        return {
            'period': f"{year}-{month:02d}",
            'spending': spending,
            'start_date': start_date,
            'end_date': end_date
        }

    def get_yearly_spending_chart_data(self, year: int) -> dict:
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        spending = self.get_spending_by_category_period(start_date, end_date)
        
        monthly_breakdown = {}
        for month in range(1, 13):
            month_data = self.get_monthly_spending_chart_data(year, month)
            monthly_breakdown[f"{year}-{month:02d}"] = month_data['spending']
        
        return {
            'period': str(year),
            'total_spending': spending,
            'monthly_breakdown': monthly_breakdown,
            'start_date': start_date,
            'end_date': end_date
        }

    def get_category_transactions(self, categoryID: int, start_date: date = None, 
                                end_date: date = None) -> List[Transaction]:
        transactions = [t for t in self.transactions if t.categoryID == categoryID]
        
        if start_date and end_date:
            transactions = [t for t in transactions 
                        if start_date <= t.date <= end_date]
        
        return transactions

    def get_category_detail_view(self, categoryID: int, start_date: date = None, 
                                end_date: date = None) -> dict:
        transactions = self.get_category_transactions(categoryID, start_date, end_date)
        
        total_spent = sum(t.total for t in transactions)
        
        return {
            'categoryID': categoryID,
            'total_spent': total_spent,
            'transaction_count': len(transactions),
            'transactions': [
                {
                    'transactionID': t.transactionID,
                    'date': t.date,
                    'payee': t.payee,
                    'amount': t.total,
                    'notes': t.notes,
                    'expenseType': t.expenseType.value if t.expenseType else 'untagged'
                } for t in transactions
            ]
        }
    #=====End of part of sprint 4 by Temka====
        


class PayFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "1 week"
    BI_WEEKLY = "bi-weekly"
    MONTHLY = "1 month"
    CUSTOM = "custom"
class Income:
    def __init__ (self, incomeID, userID, name, amount, payFrequency, datePaid, customDays: Optional[int] = None):
        self.incomeID = incomeID
        self.userID = userID
        self.name = name
        self.amount = amount
        self.payFrequency = payFrequency
        self.datePaid = datePaid
        self.isActive = True
        self.customDays = customDays
        self.date_created = date.today()

    #getters
    def get_incomeID(self):
        return self.incomeID
    def get_userID(self):
        return self.userID
    def get_name(self):
        return self.name
    def get_amount(self):
        return self.amount
    def get_payFrequency(self):
        return self.payFrequency
    def get_datePaid(self):
        return self.datePaid
    def get_isActive(self):
        return self.isActive
    def get_customDays(self):
        return self.customDays
    
    #setters
    def set_incomeID(self, incomeID):
        self.incomeID = incomeID
    def set_userID(self, userID):
        self.userID = userID
    def set_name(self, name):
        self.name = name
    def set_amount(self, amount):
        self.amount = amount
    def set_payFrequency(self, payFrequency):
        self.payFrequency = payFrequency
    def set_datePaid(self, datePaid):
        self.datePaid = datePaid
    def set_isActive(self, isActive):
        self.isActive = isActive
    def set_customDays(self, customDays):
        self.customDays = customDays

    def add_income(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def update_income(self, name: str = None, amount: float = None, payFrequency: str = None,
                      datePaid: date = None, customDays: Optional[int] = None):
        if name: self.name = name
        if amount: self.amount = amount
        if payFrequency: self.payFrequency = payFrequency
        if datePaid: self.datePaid = datePaid
        if customDays: self.customDays = customDays
    def delete_income(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def add_month(self, fromDate: date) -> date:
        nextMonth = fromDate.month + 1
        nextYear = fromDate.year
        if nextMonth > 12:
            nextMonth = 1
            nextYear += 1

            try:
                return date(nextYear, nextMonth, fromDate.day)
            except ValueError:
                if nextMonth == 12:
                    return date(nextYear + 1, 1, 1) - timedelta(days=1)
                else:
                    return date(nextYear, nextMonth + 1, 1)
    def calc_next_payday(self, startDate: date = None) -> Optional[date]:
        if not self.isActive:
            raise ValueError("Cannot calculate payday for inactive income")
        if startDate is None:
            startDate = date.today()

        lastPaid = self.datePaid

        if self.payFrequency == PayFrequency.DAILY.value:
            nextPayday = lastPaid + timedelta(days=1)
        elif self.payFrequency == PayFrequency.WEEKLY.value:
            nextPayday = lastPaid + timedelta(weeks=1)
        elif self.payFrequency == PayFrequency.BI_WEEKLY.value:
            nextPayday = lastPaid + timedelta(weeks=2)
        elif self.payFrequency == PayFrequency.MONTHLY.value:
            nextPayday = self.add_month(lastPaid)
        elif self.payFrequency == PayFrequency.CUSTOM.value and self.customDays:
            nextPayday = lastPaid + timedelta(days = self.customDays)
        else:
            raise ValueError(f"Unsupported pay frequency: {self.payFrequency}")
       
        while nextPayday <= startDate:
            if self.payFrequency == PayFrequency.DAILY.value:
                nextPayday += timedelta(days=1)
            elif self.payFrequency == PayFrequency.WEEKLY.value:
                nextPayday += timedelta(weeks=1)
            elif self.payFrequency == PayFrequency.BI_WEEKLY.value:
                nextPayday += timedelta(weeks=2)
            elif self.payFrequency == PayFrequency.MONTHLY.value:
                nextPayday = self.add_month(nextPayday)
            elif self.payFrequency == PayFrequency.CUSTOM.value and self.customDays:
                nextPayday += timedelta(days = self.customDays)
        return nextPayday
    def should_pay_today(self):
        try:
            nextPayday = self.calc_next_payday()
            return nextPayday == date.today() if nextPayday else False
        except ValueError:
            return False
    def get_upcoming_paydays(self, count: int = 5, startDate: Optional[date] = None) -> List[date]:
        if not self.isActive:
            return []
        if startDate is None:
            startDate = date.today()

        paydays = []
        currDate = self.datePaid

        nextPayday = self.calc_next_payday(startDate)
        if not nextPayday:
            return []
        
        paydays.append(nextPayday)

        for i in range(count - 1):
            if self.payFrequency == PayFrequency.DAILY.value:
                nextPayday += timedelta(days=1)
            elif self.payFrequency == PayFrequency.WEEKLY.value:
                nextPayday += timedelta(weeks=1)
            elif self.payFrequency == PayFrequency.BI_WEEKLY.value:
                nextPayday += timedelta(weeks=2)
            elif self.payFrequency == PayFrequency.MONTHLY.value:
                nextPayday = self.add_month(nextPayday)
            elif self.payFrequency == PayFrequency.CUSTOM.value and self.customDays:
                nextPayday += timedelta(days = self.customDays)
            paydays.append(nextPayday)
        return paydays
    
    #Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 2.
    def add_manual_transaction(transaction_manager: TransactionManager, userID: str, total: float, date_: date,
                           payee: str, categoryID: int, notes: str = "", expenseType: ExpenseType = None):

        new_transaction = Transaction(
            transactionID=len(transaction_manager.transactions) + 1,
            userID=userID,
            total=total,
            date=date_,
            payee=payee,
            categoryID=categoryID,
            notes=notes,
            isRecurring=False,
            expenseType=expenseType
        )

        transaction_manager.add_transaction(new_transaction)

        print(f"\nTransaction Added Successfully:")
        print(f"  ID: {new_transaction.transactionID}")
        print(f"  Payee: {new_transaction.payee}")
        print(f"  Amount: ${new_transaction.total:.2f}")
        print(f"  Category ID: {new_transaction.categoryID}")
        print(f"  Date: {new_transaction.date}")
        print(f"  Type: {new_transaction.expenseType.value if new_transaction.expenseType else 'Unspecified'}")
        print(f"  Notes: {new_transaction.notes}\n")

        return new_transaction
    
    #Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 1.
    def add_one_time_income(userID, name, amount, datePaid):
        new_income = Income(
            incomeID = 1,
            userID = userID,
            name = name,
            amount = amount,
            payFrequency = "one time",
            datePaid = datePaid
        )
        print(f"Added one time income: {new_income.name} ${new_income.amount} on {new_income.datePaid}")
        return new_income
    
    #Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 1.
    def calculate_total_monthly_income(income_sources, previousTotal):
        currentTotal = previousTotal

        for income_obj in income_sources:
            amount = income_obj.amount
            payFrequency = income_obj.payFrequency.lower()

            if payFrequency == "weekly":
                currentTotal += amount * 4
            elif payFrequency == "biweekly":
                currentTotal += amount * 2
            elif payFrequency == "monthly":
                currentTotal += amount
            elif payFrequency == "annual":
                currentTotal += amount / 12
        
        return currentTotal

#Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 2.
class Expense:
    def __init__(self, expenseID: int, userID: int, name: str, amount: float, category: str, payFrequency: str, startDate: date):
        self.expenseID = expenseID
        self.userID = userID
        self.name = name
        self.amount = amount
        self.category = category
        self.payFrequency = payFrequency.lower()
        self.startDate = startDate
        self.nextDate = startDate

    def __str__(self):
        return f"{self.name} ({self.category}) - ${self.amount:.2f} [{self.payFrequency.capitalize()}] Next: {self.nextDate}"

    def get_next_occurrence(self):
        if self.payFrequency == "weekly":
            self.nextDate += timedelta(weeks=1)
        elif self.payFrequency == "biweekly":
            self.nextDate += timedelta(weeks=2)
        elif self.payFrequency == "monthly":
            new_month = self.nextDate.month + 1 if self.nextDate.month < 12 else 1
            new_year = self.nextDate.year if self.nextDate.month < 12 else self.nextDate.year + 1
            self.nextDate = self.nextDate.replace(year=new_year, month=new_month)
        elif self.payFrequency == "annual":
            self.nextDate = self.nextDate.replace(year=self.nextDate.year + 1)
        return self.nextDate

    def post_expense(self, expenses_list):
        expenses_list.append({
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "date": self.nextDate
        })
        print(f"Recurring expense '{self.name}' posted for {self.nextDate}.")
        self.get_next_occurrence()

#Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 2.
def add_recurring_transportation_expense(expenses, userID, name, amount, category, payFrequency, startDate=None):
    if startDate is None:
        startDate = date.today()
    
    new_expense = Expense(
        expenseID=len(expenses),
        userID=userID,
        name=name,
        amount=amount,
        category=category,
        payFrequency=payFrequency,
        startDate=startDate
    )

    expenses.append(new_expense)
    print(f"Transportation expense '{name}' added as a recurring {payFrequency} cost under '{category}'.")
    return new_expense