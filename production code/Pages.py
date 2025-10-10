from datetime import date

class Dashboard:
    def __init__ (self, userID):
        self.userID = userID

    #getters
    def get_userID (self):
        return self.userID
    
    #setters
    def set_userID (self):
        return self.userID
    
    def get_monthly_summary(self, month: date) -> bool:
        #Future Implementation
        return True
    def get_recent_transaction(self) -> bool:
        #Future Implementation
        return True
    def get_category_progress(self) -> bool:
        #Future Implementation
        return True
    def get_chart_data(self) -> bool:
        #Future Implementation
        return True