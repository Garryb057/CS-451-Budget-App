import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt

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
    first_name = entry_first.get()
    last_name = entry_last.get()

    cursor.execute("SELECT first_name, last_name, password_hash FROM bankUser WHERE email=%s", (email,))
    row = cursor.fetchone()

    if not row:
        messagebox.showerror("Login Failed", "Invalid email or password")
        return

    first_name, last_name, password_hash = row

    if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        messagebox.showinfo("Login", f"Welcome, {first_name} {last_name}!")
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

#starts with the login screen firstly
show_login_screen()

root.mainloop()
