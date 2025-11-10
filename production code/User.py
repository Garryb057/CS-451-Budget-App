import re
from typing import Optional, Tuple
from notificationSettings import NotificationSettings

class User:
    def __init__(self, email, passwordHash, fname, lname, phoneNumber, dateCreated):
        self.email = email
        self.passwordHash = passwordHash
        self.fname = fname
        self.lname = lname
        self.phoneNumber = phoneNumber
        self.dateCreated = dateCreated
        self.disputes = []
        self.balance = 0.0
        self.isActive = True
        self.notificationSettings = NotificationSettings(self.email)

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
    def get_notification_settings(self) -> NotificationSettings:
        return self.notificationSettings
    def get_notification_summary(self) -> dict:
        return self.notificationSettings.get_settings_summary()
    
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
    def delete (self) -> Tuple[bool, str]:
        prereqs_met, msg = self.validate_deletion_prereq()
        if not prereqs_met:
            return False, msg
        self.isActive = False
        return True, "Account successfully closed."
    def login (self, password):
       #Future Implementation
       self.passwordHash = self.hash_password(password)
    def change_password (self, old_password, new_password):
        if not self.login(old_password):
            return False, "Old Password is incorrect"
        strong_pass, msg = self.validate_strong_password(new_password)
        if not strong_pass:
            return False, msg
        self.set_passwordHash(self.hash_password(new_password))
        return True, "Password Updated Successfully"
    def update_profile (self, email: Optional[str] = None, fname: Optional[str] = None, lname: Optional[str] = None, phoneNumber: Optional[str] = None) -> Tuple[bool, str]:
        updates = {}
        validationErrors = []

        if email is not None:
            isValid, errorMsg = self.validate_email(email)
            if isValid:
                updates['email'] = email
            else:
                validationErrors.append(errorMsg)
        if fname is not None:
            isValid, errorMsg = self.validate_name(fname, "First Name")
            if isValid:
                updates['fname'] = fname
            else:
                validationErrors.append(errorMsg)
        if lname is not None:
            isValid, errorMsg = self.validate_name(lname, "Last Name")
            if isValid:
                updates['lname'] = lname
            else:
                validationErrors.append(errorMsg)
        if phoneNumber is not None:
            isValid, errorMsg = self.validate_phone_number(phoneNumber)
            if isValid:
                updates['phoneNumber'] = phoneNumber
            else:
                validationErrors.append(errorMsg)

        if validationErrors:
            return False, "; ".join(validationErrors)
        if not updates:
            return False, "No valid updates provided"
        
        try:
            if 'email' in updates:
                self.set_email(updates['email'])
            if 'fname' in updates:
                self.set_fname(updates['fname'])
            if 'lname' in updates:
                self.set_lname(updates['lname'])
            if 'phoneNumber' in updates:
                self.set_phoneNumber(updates['phoneNumber'])

            updatedFields = list(updates.keys())
            return True, f"Profle updated successfully: {', '.join(updatedFields)}"
        except Exception as e:
            return False, f"Error updating profile: {str(e)}"
    def validate_name(self, name: str, fieldName: str) -> Tuple[bool, str]:
        if not name or not name.strip():
            return False, f"{fieldName} cannot be empty"
        name = name.strip()

        if len(name) < 2:
            return False, f"{fieldName} must be at least 2 characters long"
        if len(name) > 50:
            return False, f"{fieldName} must be less than 50 characters"
        if not re.match(r"^[A-Za-zÀ-ÿ'\- ]+$", name):
            return False, f"{fieldName} contains invalid characters"
        
        return True, "Valid"
    def validate_phone_number(self, phoneNumber: str) -> Tuple[bool, str]:
        if not phoneNumber or not phoneNumber.strip():
            return False, "Phone number cannot be empty"
        phoneNumber = phoneNumber.strip()
        cleanedPhoneNumber = re.sub(r'[\s\-\(\)\+\.]', '', phoneNumber)

        if not cleanedPhoneNumber.isdigit():
            return False, "Phone number must contain only digits and common separators"
        if len(cleanedPhoneNumber) < 10:
            return False, "Phone number is too short"
        if len(cleanedPhoneNumber) > 15:
            return False, "Phone number is too long"
        
        return True, "Valid"
    def validate_email(self, email: str) -> Tuple[bool, str]:
        if not email or not email.strip():
            return False, "Email cannot be empty"
        email = email.strip()

        emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(emailPattern, email):
            return False, "Invalid email format"
        
        return True, "Valid"
    def get_profile_info(self) -> dict:
        return {
            'email': self.email,
            'fname': self.fname,
            'lname': self.lname,
            'phoneNumber': self.phoneNumber,
            'dateCreated': self.dateCreated,
            'isActive': self.isActive
        }
    def hash_password (password: str) -> str:
        #Future Implementation
        print("Hash Password")
    def validate_strong_password(password: str):
        if len(password) < 8:
            return False, "Password must be 8 characters long"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain a uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain a lowercase letter"
        if not re.search(r"\d", password):
            return False, "Password must contain a digit"
        if not re.search(r"[!@#$%^&*()_-+={};:,./<>?]", password):
            return False, "Password must contain a special character"
        return True, "Password is strong"
    def validate_deletion_prereq(self) -> Tuple[bool, str]:
        missing_prereq = []

        if self.has_pending_disputes():
            missing_prereq.append("pending disputes")
        if self.balance < 0:
            missing_prereq.append("negative balance")
        if missing_prereq:
            msg = f"Cannot close account due to: {', '.join(missing_prereq)}. Please resolve these issues before closing your account."
            return False, msg
        return True, "All prerequisities met. Account can be closed."
    def has_pending_disputes(self) -> bool:
        return any(dispute.get('status') == 'pending' for dispute in self.disputes)
    def add_dispute(self, disputeID: int, description: str, status: str = 'pending'):
        self.disputes.append({
            'id': disputeID,
            'description': description,
            'status': status
        })
    def update_dispute_status(self, disputeID: int, new_status: str):
        for dispute in self.disputes:
            if dispute['id'] == disputeID:
                dispute['status'] = new_status
                break
    def update_notification_preferences(self, category: str, channels: dict) -> Tuple[bool, str]:
        try:
            success = self.notification_settings.update_category_settings(
                category,
                push=channels.get('push'),
                email=channels.get('email'),
                sms=channels.get('sms')
            )
            if success:
                return True, f"Notification preferences updated for {category}"
            else:
                return False, f"Failed to update {category} notifications"
        except Exception as e:
            return False, f"Error updating notification preferences: {str(e)}"

    #Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 1.
    def find_user_by_email(email, users):
        for user in users:
            if user.get_email() == email:
                return user
        return None

    #Added by Temka, commenting to find my code later easier for debugging. Part of Sprint 1.
    def login_user(email: str, password: str, users):
        user = User.find_user_by_email(email, users)

        if not user or user.get_passwordHash() != password:
            return False, "Invalid email or password."
        
        return True, "Successful login."