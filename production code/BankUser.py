import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import time
import uuid
from BankDashboard import open_dashboard

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Melt1129",
    database="banking_db"
)

cursor = db.cursor()


# Functions
def register_user():
    first_name = entry_first.get()
    last_name = entry_last.get()
    email_reg = entry_email_reg.get()
    password_reg = entry_password_reg.get()
    phone_number = entry_phone.get()

    if not first_name or not last_name or not email_reg or not password_reg or not phone_number:
        messagebox.showwarning("Missing Fields", "Please fill in all fields")
        return

    hashed = bcrypt.hashpw(password_reg.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO bankUser (first_name, last_name, email, password_hash, phone_number) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, email_reg, hashed.decode(), phone_number)
        )
        db.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        clear_register_fields()
        show_login_screen()
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062:
            messagebox.showerror("Error", "That email/phone number is already in use.")
        else:
            messagebox.showerror("Error", f"Database error: {err}")

def login_user():
    email = entry_email.get()
    password = entry_password.get()

    cursor.execute("SELECT idbankUser, first_name, last_name, password_hash FROM bankUser WHERE email=%s", (email,))
    row = cursor.fetchone()

    if not row:
        messagebox.showerror("Login Failed", "Invalid email or password")
        return

    user_id, first_name, last_name, password_hash = row

    if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        messagebox.showinfo("Login", f"Welcome, {first_name} {last_name}!")

        # store current user's email for later settings lookups
        global current_user_email
        current_user_email = email

        # import here to avoid circular dependency
        from BankDashboard import open_dashboard

        # open dashboard and provide settings callback + pass db/cursor
        open_dashboard(root,first_name,last_name,user_id,logout_callback,settings_callback=show_account_settings,db=db,cursor=cursor)
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")


root = tk.Tk()
root.title("Login System")
root.geometry("350x400")

frame_login = tk.Frame(root)
frame_register = tk.Frame(root)

# Login screen
tk.Label(frame_login, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(frame_login, text="Email").pack(pady=2)
entry_email = tk.Entry(frame_login)
entry_email.pack(pady=2)

tk.Label(frame_login, text="Password").pack(pady=2)
entry_password = tk.Entry(frame_login, show="*")
entry_password.pack(pady=2)

tk.Button(frame_login, text="Login", command=login_user).pack(pady=10)

tk.Label(frame_login, text="Don't have an account?").pack(pady=5)
tk.Button(frame_login, text="Sign up here", command=lambda: show_register_screen()).pack()


# sign up screen
tk.Label(frame_register, text="Register", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(frame_register, text="First Name").pack(pady=2)
entry_first = tk.Entry(frame_register)
entry_first.pack(pady=2)

tk.Label(frame_register, text="Last Name").pack(pady=2)
entry_last = tk.Entry(frame_register)
entry_last.pack(pady=2)

tk.Label(frame_register, text="Email").pack(pady=2)
entry_email_reg = tk.Entry(frame_register)
entry_email_reg.pack(pady=2)

tk.Label(frame_register, text="Password").pack(pady=2)
entry_password_reg = tk.Entry(frame_register, show="*")
entry_password_reg.pack(pady=2)

tk.Label(frame_register, text="Phone Number").pack(pady=2)
entry_phone = tk.Entry(frame_register)
entry_phone.pack(pady=2)

tk.Button(frame_register, text="Register", command=register_user).pack(pady=10)
tk.Button(frame_register, text="Return", command=lambda: show_login_screen()).pack()

# switch between screens
def show_login_screen():
    frame_register.pack_forget()
    frame_login.pack(fill="both", expand=True)

#shows the register screen.
def show_register_screen():
    frame_login.pack_forget()
    frame_register.pack(fill="both", expand=True)

#used to clear out the fields once done.
def clear_register_fields():
    entry_first.delete(0, tk.END)
    entry_last.delete(0, tk.END)
    entry_email_reg.delete(0, tk.END)
    entry_password_reg.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

#once the user logs out, this function will be called and delete each filed of the entry email and password.
def logout_callback(root):
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    root.deiconify()

# This shows the infomation of the settings to the user.
def show_account_settings(parent_window):
    """Open a modal window showing account info and allow edits."""
    # fetch latest user info
    cursor.execute("SELECT first_name, last_name, email, phone_number FROM bankUser WHERE email=%s", (current_user_email,))
    row = cursor.fetchone()
    if not row:
        messagebox.showerror("Error", "Could not load user info.")
        return

    fname, lname, email, phone = row

    settings_win = tk.Toplevel(parent_window)
    settings_win.title("Account Settings")
    settings_win.geometry("350x350")
    settings_win.transient(parent_window)
    settings_win.grab_set()

    tk.Label(settings_win, text="Account Settings", font=("Arial", 14, "bold")).pack(pady=8)

    tk.Label(settings_win, text="First Name").pack(pady=2)
    e_fname = tk.Entry(settings_win)
    e_fname.insert(0, fname)
    e_fname.pack(pady=2)

    tk.Label(settings_win, text="Last Name").pack(pady=2)
    e_lname = tk.Entry(settings_win)
    e_lname.insert(0, lname)
    e_lname.pack(pady=2)

    tk.Label(settings_win, text="Email").pack(pady=2)
    e_email = tk.Entry(settings_win)
    e_email.insert(0, email)
    e_email.pack(pady=2)

    tk.Label(settings_win, text="Phone Number").pack(pady=2)
    e_phone = tk.Entry(settings_win)
    e_phone.insert(0, phone)
    e_phone.pack(pady=2)

    def save_changes():
        global current_user_email
        new_fname = e_fname.get().strip()
        new_lname = e_lname.get().strip()
        new_email = e_email.get().strip()
        new_phone = e_phone.get().strip()

        if not new_fname or not new_lname or not new_email or not new_phone:
            messagebox.showwarning("Missing Fields", "Please fill in all fields")
            return

        try:
            cursor.execute("UPDATE bankUser SET first_name=%s, last_name=%s, email=%s, phone_number=%s WHERE email=%s",
                           (new_fname, new_lname, new_email, new_phone, current_user_email))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            if err.errno == 1062:
                messagebox.showerror("Error", "That email or phone number is already in use.")
                return
            else:
                messagebox.showerror("Error", f"Database error: {err}")
                return

        # If email changed (compare normalized values), update session and prompt to re-login
        try:
            old_norm = (current_user_email or "").strip().lower()
        except Exception:
            old_norm = ""
        new_norm = new_email.strip().lower()

        if new_norm != old_norm:
            messagebox.showinfo("Email Changed", "Your email was changed. You will be logged out and need to login with the new email.")
            settings_win.destroy()
            # force logout: close parent dashboard and show login
            parent_window.destroy()
            logout_callback(root)
            return

        # No email change — success
        messagebox.showinfo("Success", "Account updated successfully.")
        settings_win.destroy()

    tk.Button(settings_win, text="Save Changes", command=save_changes).pack(pady=12)
    tk.Button(settings_win, text="Close", command=settings_win.destroy).pack()

#starts with the login screen firstly
show_login_screen()


root.mainloop()
