from datetime import date, datetime

class Transaction:
    def __init__ (self, transactionID: int, userID: str, total: float, date: date, 
                  payee: str, categoryID: int, notes: str = "", isRecurring: bool = False, 
                  dateRecurr: date = None):
        self.transactionID = transactionID
        self.userID = userID
        self.total = total
        self.date = date
        self.payee = payee
        self.categoryID = categoryID
        self.notes = notes
        self.isRecurring = isRecurring
        self.dateRecurr = dateRecurr

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
    
    def add_transaction(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def delete_transaction(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def edit_transaction(self, total: float = None, date: date = None, payee: str = None,
                         categoryID: int = None, notes: str = None):
        if total: self.total = total
        if date: self.date = date
        if payee: self.payee = payee
        if categoryID: self.categoryID = categoryID
        if notes: self.notes = notes

class Income:
    def __init__ (self, incomeID, userID, name, amount, payFrequency, datePaid):
        self.incomeID = incomeID
        self.userID = userID
        self.name = name
        self.amount = amount
        self.payFrequency = payFrequency
        self.datePaid = datePaid

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
    
    def add_income(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def update_income(self, name: str = None, amount: float = None, payFrequency: str = None,
                      datePaid: date = None):
        if name: self.name = name
        if amount: self.amount = amount
        if payFrequency: self.payFrequency = payFrequency
        if datePaid: self.datePaid = datePaid
    def delete_income(self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def calc_next_payday(self, date: date = None) -> date:
        #Remove date from parameters, current placeholder to not throw error
        print("Success")
        return date