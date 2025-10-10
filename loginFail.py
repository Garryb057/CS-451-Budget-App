from datetime import date
from User import User


#Needs security implementation, for now it is just a simple checking function.
USER_DATABASE = [
    User(
        email="user@example.com",
        passwordHash="123",
        fname="John",
        lname="Doe",
        phoneNumber="555-1234",
        dateCreated=date(2025, 10, 1)
    )
]

def find_user_by_email(email):
    for user in USER_DATABASE:
        if user.get_email() == email:
            return user
    return None

def login_user(email: str, password: str):
    user = find_user_by_email(email)

    if not user or user.get_passwordHash() != password:
        return False, "Invalid email or password."
    
    return True, f"Succesful login."

#Come back to this for future security hashing and other features.