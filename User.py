class User:
    def __init__(self, email, passwordHash, fname, lname, phoneNumber, dateCreated):
        self.email = email
        self.passwordHash = passwordHash
        self.fname = fname
        self.lname = lname
        self.phoneNumber = phoneNumber
        self.dateCreated = dateCreated

    # getters
    def get_email(self):
        return self.email
    def get_passwordHash(self):
        return self.passwordHash
    def get_fname(self):
        return self.fname
    def get_lname(self):
        return self.lname
    def get_phoneNumber(self):
        return self.phoneNumber
    def get_dateCreated(self):
        return self.dateCreated
    
    #setters
    def set_email (self, email):
        self.email = email
    def set_passwordHash (self, passwordHash):
        self.passwordHash = passwordHash
    def set_fname (self, fname):
        self.fname = fname
    def set_lname (self, lname):
        self.lname = lname
    def set_phoneNumber (self, phoneNumber):
        self.phoneNumber = phoneNumber
    def set_dateCreated (self, dateCreated):
        self.dateCreated = dateCreated
    
    def register (self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def delete (self) -> bool:
        #Future Implementation
        print("Success")
        return True
    def login (self, password):
       #Future Implementation
       self.passwordHash = self.hash_password(password)
    def change_password (self, old_password, new_password):
        if self.login(old_password):
            self.passwordHash = self.hash_password(new_password)
            return True
        return False
    def update_profile (self, email: str=None, fname: str=None, lname: str=None, phoneNumber: str=None):
        if email: self.email = email
        if fname: self.fname = fname
        if lname: self.lname = lname
        if phoneNumber: self.phoneNumber = phoneNumber
    def hash_password (password: str) -> str:
        #Future Implementation
        print("Hash Password")