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