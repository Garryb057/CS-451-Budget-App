from datetime import date
from typing import List
from Money import Transaction, TransactionManager

class Dashboard:
    def __init__ (self, userID, transactionManager: TransactionManager):
       self.userID = userID
       self.transactionManager = transactionManager

    #getters
    def get_userID (self):
        return self.userID
    
    #setters
    def set_userID (self):
        return self.userID
    
    def get_monthly_summary(self, month: date) -> bool:
        #Future Implementation
        return True
    def get_recent_transaction(self, limit: int = 10) -> List[Transaction]:
        return self.transactionManager.get_recent_transactions(self.userID, limit)
    def get_recent_transactions_widget_data(self, limit: int = 10) -> List[dict]:
        recentTransactions = self.get_recent_transaction(limit)
        widgetData = []


        for transaction in recentTransactions:
           widgetData.append({
               'transactionID': transaction.transactionID,
               'date': transaction.date,
               'payee': transaction.payee,
               'amount': transaction.total,
               'category': transaction.categoryID
           })
        return widgetData

    def get_category_progress(self) -> bool:
        #Future Implementation
        return True
    def get_chart_data(self) -> bool:
        #Future Implementation
        return True
    
 #==Part of sprint 4 by Temka, for later debugging==
    def get_spending_chart_data(self, view_type: str = 'monthly', 
                            year: int = None, month: int = None) -> dict:
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month
        
        #This would integrate with TransactionManager
        #For now, returning structure
        return {
            'view_type': view_type,
            'year': year,
            'month': month if view_type == 'monthly' else None,
            'data': {}  #Would be populated by TransactionManager
        }

    def switch_chart_view(self, view_type: str, year: int = None, 
                        month: int = None) -> dict:
        if view_type not in ['monthly', 'yearly']:
            raise ValueError("view_type must be 'monthly' or 'yearly'")
        
        chart_data = self.get_spending_chart_data(view_type, year, month)
        
        # Store user preference (Future implementation: save to database)
        print(f"Chart view switched to {view_type}")
        
        return chart_data

    def get_category_drill_down(self, categoryID: int, period_start: date, 
                            period_end: date) -> dict:
        # This would integrate with TransactionManager
        return {
            'categoryID': categoryID,
            'period_start': period_start,
            'period_end': period_end,
            'transactions': []  # Would be populated by TransactionManager
        }

    def persist_chart_preference(self, view_type: str) -> bool:
        # Future implementation: save to database
        print(f"Chart preference '{view_type}' saved for user {self.userID}")
        return True

    def get_user_chart_preference(self) -> str:
        # Future implementation: retrieve from database
        # Default to monthly
        return 'monthly'
 #==End of Part of sprint 4 by Temka, for later debugging==