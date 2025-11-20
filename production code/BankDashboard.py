import tkinter as tk
from tkinter import messagebox, ttk
import time
import uuid
from budgetDB import BudgetDB
from budget import Budget, Category


SESSION_TIMEOUT = 300  # 5 minutes or 30 secs for testing. its set to 5 mins for now.

# Global session info
SESSION = {
    "token": None,
    "last_active": None
}

#Opening dashboard after login. 
def open_dashboard(root, first_name, last_name, user_id, logout_callback, settings_callback=None, db=None, cursor=None):
    # Hide login window
    root.withdraw()

    # Create session token
    SESSION["token"] = str(uuid.uuid4())
    SESSION["last_active"] = time.time()

    # Dashboard window
    dashboard = tk.Toplevel()
    dashboard.title("User Dashboard")
    dashboard.geometry("500x400")

    tk.Label(dashboard, text=f"Welcome, {first_name} {last_name}", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(dashboard, text="Account Overview", font=("Arial", 14)).pack(pady=5)

    balance_var = tk.StringVar()
    balance = get_user_balance(user_id, cursor)
    balance_var.set(f"${balance:,.2f}")
    tk.Label(dashboard, textvariable=balance_var, font=("Arial", 24, "bold"), fg="green").pack(pady=10)

    # Dashboard buttons
    tk.Button(dashboard,text="Deposit",width=20,command=lambda: deposit_money(user_id, db, cursor, balance_var)).pack(pady=5)
    tk.Button(dashboard, text="Withdraw", width=20).pack(pady=5)
    tk.Button(dashboard, text="Transfer Money", width=20).pack(pady=5)
    tk.Button(dashboard, text="View Transactions", width=20).pack(pady=5)
    tk.Button(dashboard, text="Manage Budgets", width=20,command=lambda: open_budget_manager(user_id, db, cursor)).pack(pady=5)
    # Account Settings button will call the provided settings_callback if present.
    tk.Button(dashboard, text="Account Settings", width=20,
              command=(lambda: settings_callback(dashboard) if settings_callback else None)).pack(pady=5)

    tk.Button(dashboard, text="Logout", width=15, fg="red",
              command=lambda: logout(dashboard, root, logout_callback)).pack(pady=20)

    # Bind activity tracking
    dashboard.bind_all("<Any-KeyPress>", lambda e: update_activity())
    dashboard.bind_all("<Any-ButtonPress>", lambda e: update_activity())
    dashboard.bind_all("<Motion>", lambda e: update_activity())

    # Start inactivity check
    check_inactivity(dashboard, root, logout_callback, user_id, cursor)

# Function for depositing money to the users balances.
def deposit_money(user_id, db, cursor, balance_var):
    """Popup window for depositing money."""
    deposit_win = tk.Toplevel()
    deposit_win.title("Deposit Funds")
    deposit_win.geometry("300x200")
    deposit_win.grab_set()

    tk.Label(deposit_win, text="Enter deposit amount:", font=("Arial", 12)).pack(pady=10)
    amount_entry = tk.Entry(deposit_win)
    amount_entry.pack(pady=5)

    def confirm_deposit():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showwarning("Invalid Amount", "Please enter a positive amount.")
                return

            # Update balance in database
            update_user_balance(user_id, amount, db, cursor)

            # Refresh displayed balance
            new_balance = get_user_balance(user_id, cursor)
            balance_var.set(f"${new_balance:,.2f}")

            messagebox.showinfo("Success", f"Deposited ${amount:,.2f} successfully!")
            deposit_win.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    tk.Button(deposit_win, text="Confirm", command=confirm_deposit).pack(pady=10)
    tk.Button(deposit_win, text="Cancel", command=deposit_win.destroy).pack()


def get_user_balance(user_id, cursor):
    """Fetch the user's balance from the database."""
    try:
        cursor.execute("SELECT userBalance FROM bankBalance WHERE userID = %s", (user_id,))
        result = cursor.fetchone()
        return float(result[0]) if result else 0.00
    except Exception as e:
        print("Database error while getting balance:", e)
        return 0.00


def update_user_balance(user_id, amount, db, cursor):
    """Deposit money — creates a balance record if one doesn't exist yet."""
    try:
        # Check if the record exists
        cursor.execute("SELECT userBalance FROM bankBalance WHERE userID = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            # User already has a record it'll just update it
            cursor.execute("""
                UPDATE bankBalance
                SET userBalance = userBalance + %s, lastUpdated = NOW()
                WHERE userID = %s
            """, (amount, user_id))
        else:
            # No record yet, it'll create one with the deposited amount
            cursor.execute("""
                INSERT INTO bankBalance (userID, userBalance, lastUpdated)
                VALUES (%s, %s, NOW())
            """, (user_id, amount))

        db.commit()

    except Exception as e:
        print("Error updating or creating balance record:", e)


def update_activity():
    SESSION["last_active"] = time.time()

def check_inactivity(window, root, logout_callback, user_id, cursor):
    """Check every few seconds if the user has been inactive."""
    if SESSION["last_active"] is not None:
        elapsed = time.time() - SESSION["last_active"]
        if elapsed > SESSION_TIMEOUT:
            from BankEmail import send_alert_email
            cursor.execute("SELECT email FROM bankUser WHERE idbankUser = %s", (user_id,))
            user_email = cursor.fetchone()[0]

            

            send_alert_email(
                to_email=user_email,
                subject="Logged Out Due to Inactivity",
                body="You were automatically logged out due to inactivity. If this was not you, please check your account immediately."
            )

            messagebox.showinfo("Session Expired", "You have been logged out due to inactivity.")
            logout(window, root, logout_callback)
            return
    window.after(2000, lambda: check_inactivity(window, root, logout_callback, user_id, cursor))


def logout(dashboard_window, root, logout_callback):
    """Logs out and returns to login."""
    SESSION["token"] = None
    SESSION["last_active"] = None
    dashboard_window.destroy()
    logout_callback(root)

"""function from here is used to budget/categeroies."""

#Function used to open up the budget manager window.
def open_budget_manager(user_id, db, cursor):
    budget_win = tk.Toplevel()
    budget_win.title("Budget Manager")
    budget_win.geometry("900x500")
    budget_win.grab_set()

    left_frame = tk.Frame(budget_win)
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right_frame = tk.Frame(budget_win)
    right_frame.pack(side="right", fill="y", padx=10, pady=10)

    # decided to use Treeview for budgets
    columns = ("id", "name", "month", "income", "total", "remaining")
    budget_tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="browse", height=20)

    headings = {
        "id": "ID",
        "name": "Name",
        "month": "Month",
        "income": "Income",
        "total": "Planned Total",
        "remaining": "Remaining"
    }
    for col in columns:
        budget_tree.heading(col, text=headings[col])
        budget_tree.column(col, width=120 if col != "name" else 200)

    budget_tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=budget_tree.yview)
    budget_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # linking the database.
    budget_db = BudgetDB(db)

    # Load and store loaded budgets
    def load_budget_entries(user_id, db, tree):
        tree.delete(*tree.get_children())

        budget_db = BudgetDB(db)
        budgets = budget_db.load_budgets_for_user(user_id)

        for b in budgets:
            income = float(b.income or 0)
            total = float(b.totalPlannedAmnt or 0)
            remaining = income - total

            tree.insert(
                "",
                "end",
                values=(
                    b.budgetID,
                    b.name,
                    b.month,
                    f"${income:,.2f}",
                    f"${total:,.2f}",
                    f"${remaining:,.2f}"
                )
            )

    # buttons that will be on the right side of the screen.
    tk.Button(right_frame, text="Add Budget", width=20, command=lambda: add_budget_popup(budget_db, load_budget_entries)).pack(pady=5)
    tk.Button(right_frame, text="Edit Budget", width=20, command=lambda: edit_budget_popup(budget_db, load_budget_entries, budget_tree)).pack(pady=5)
    tk.Button(right_frame, text="Delete Budget", width=20, command=lambda: delete_budget(budget_db, load_budget_entries, budget_tree)).pack(pady=5)
    tk.Button(right_frame, text="Manage Categories", width=20, command=lambda: open_category_manager(budget_db, budget_tree)).pack(pady=5)
    tk.Button(right_frame, text="Refresh", width=20, command=lambda: load_budget_entries(user_id, db, budget_tree)).pack(pady=5)
    tk.Button(right_frame, text="Close", width=20, command=budget_win.destroy).pack(pady=20)

    #Function used to add a new budget. 
    def add_budget_popup(budget_db_obj, refresh_cb):
        add_win = tk.Toplevel(budget_win)
        add_win.title("Create New Budget")
        add_win.geometry("350x260")
        add_win.grab_set()

        tk.Label(add_win, text="Budget Name:").pack()
        name_entry = tk.Entry(add_win)
        name_entry.pack()

        tk.Label(add_win, text="Month (YYYY-MM):").pack()
        month_entry = tk.Entry(add_win)
        month_entry.pack()

        tk.Label(add_win, text="Total Planned Amount:").pack()
        amount_entry = tk.Entry(add_win)
        amount_entry.pack()

        tk.Label(add_win, text="Income (optional):").pack()
        income_entry = tk.Entry(add_win)
        income_entry.pack()

        #Function used to save the budget to the database.
        def save_budget():
            try:
                name = name_entry.get().strip()
                month = month_entry.get().strip()
                total = float(amount_entry.get().strip() or 0.0)
                income = float(income_entry.get().strip() or 0.0)

                if not name:
                    messagebox.showwarning("Missing", "Please enter a budget name.")
                    return
                # make sure to use YYYY or YYYY-MM format for month.
                if not (len(month) == 7 and month[4] == '-') and not (len(month) == 4):
                    messagebox.showwarning("Invalid Month", "Please use YYYY or YYYY-MM format.")
                    return

                new_budget = Budget(
                    budgetID=None,
                    userID=user_id,
                    name=name,
                    totalPlannedAmnt=total,
                    month=month,
                    income=income
                )

                budget_id = budget_db_obj.create_budget(new_budget)
                messagebox.showinfo("Success", f"Budget '{name}' created with ID {budget_id}")
                add_win.destroy()
                refresh_cb()
            except ValueError:
                messagebox.showerror("Error", "Enter valid numeric values for amounts.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create budget: {e}")

        tk.Button(add_win, text="Create Budget", command=save_budget).pack(pady=10)

    #Function used to edit an existing budget.
    def edit_budget_popup(budget_db_obj, refresh_cb, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a budget to edit.")
            return

        vals = tree.item(sel, "values")
        budget_id = int(vals[0])
        current_name = vals[1]
        current_month = vals[2]
        current_income = vals[3]
        current_planned = vals[4]

        edit_win = tk.Toplevel(budget_win)
        edit_win.title("Edit Budget")
        edit_win.geometry("350x260")
        edit_win.grab_set()

        tk.Label(edit_win, text="Budget Name:").pack()
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, current_name)
        name_entry.pack()

        tk.Label(edit_win, text="Month (YYYY-MM):").pack()
        month_entry = tk.Entry(edit_win)
        month_entry.insert(0, current_month)
        month_entry.pack()

        tk.Label(edit_win, text="Planned Amount:").pack()
        planned_entry = tk.Entry(edit_win)
        planned_entry.insert(0, current_planned)
        planned_entry.pack()

        tk.Label(edit_win, text="Income:").pack()
        income_entry = tk.Entry(edit_win)
        income_entry.insert(0, current_income)
        income_entry.pack()

        #Same function like save_budget but for editing an existing budget.
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_month = month_entry.get().strip()
                new_planned = float(planned_entry.get().strip() or 0.0)
                new_income = float(income_entry.get().strip() or 0.0)

                if not new_name:
                    messagebox.showwarning("Missing", "Please enter a budget name.")
                    return

                # Update using BudgetDB.update_budget
                b = Budget(budgetID=budget_id, userID=user_id, name=new_name, totalPlannedAmnt=new_planned, month=new_month, income=new_income)
                budget_db_obj.update_budget(b)

                messagebox.showinfo("Saved", "Budget updated.")
                edit_win.destroy()
                refresh_cb()
            except ValueError:
                messagebox.showerror("Error", "Enter valid numeric values for amounts.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update budget: {e}")

        tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=10)

    #Function used to delete a budget.
    def delete_budget(budget_db_obj, refresh_cb, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("No Selection", "Select a budget to delete.")
            return

        vals = tree.item(sel, "values")
        budget_id = int(vals[0])
        name = vals[1]

        if not messagebox.askyesno("Delete Budget", f"Delete '{name}'? This cannot be undone."):
            return

        try:
            budget_db_obj.delete_budget(budget_id)
            refresh_cb()
            messagebox.showinfo("Deleted", f"Budget '{name}' deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete budget: {e}")

    """Below is where I start working on the category manager for budgets."""
    #Function used to open the category manager for a selected budget.
    def open_category_manager(budget_db_obj, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a budget first.")
            return

        budget_id = int(tree.item(sel, "values")[0])
        # Reload the selected budget to get categories
        budgets = budget_db_obj.load_budgets_for_user(user_id)
        budget = next((b for b in budgets if (b.budgetID == budget_id)), None)
        if not budget:
            messagebox.showerror("Error", "Could not load selected budget.")
            return

        cat_win = tk.Toplevel(budget_win)
        cat_win.title(f"Categories for {budget.name}")
        cat_win.geometry("600x400")
        cat_win.grab_set()

        tk.Label(cat_win, text=f"Budget: {budget.name}", font=("Arial", 14, "bold")).pack(pady=10)

        cat_frame = tk.Frame(cat_win)
        cat_frame.pack(fill="both", expand=True, padx=10, pady=5)

        cat_list = tk.Listbox(cat_frame, width=80, height=12)
        cat_list.pack(side="left", fill="both", expand=True)

        cat_scroll = ttk.Scrollbar(cat_frame, orient="vertical", command=cat_list.yview)
        cat_list.configure(yscroll=cat_scroll.set)
        cat_scroll.pack(side="right", fill="y")

        categories = budget_db_obj.load_categories_for_budget(budget.budgetID)
        for c in categories:
            cat_list.insert(tk.END, f"{c.categoryID} | {c.name} | {c.type} | ${c.plannedAmnt:.2f}")

        #Function used to add a new category to the selected budget.
        def add_category_popup():
            win = tk.Toplevel(cat_win)
            win.title("Add Category")
            win.geometry("350x300")
            win.grab_set()

            tk.Label(win, text="Category Name:").pack()
            name_entry = tk.Entry(win); name_entry.pack()

            tk.Label(win, text="Type:").pack()
            type_entry = tk.Entry(win); type_entry.pack()

            tk.Label(win, text="Planned Amount:").pack()
            amount_entry = tk.Entry(win); amount_entry.pack()

            tk.Label(win, text="Planned Percentage (optional):").pack()
            perc_entry = tk.Entry(win); perc_entry.pack()

            tk.Label(win, text="Limit:").pack()
            limit_entry = tk.Entry(win); limit_entry.pack()

            #its the same like with the budgets but for categories.
            def save_new_category():
                try:
                    new_cat = Category(
                        categoryID=None,
                        name=name_entry.get().strip(),
                        type_=type_entry.get().strip(),
                        plannedAmnt=float(amount_entry.get().strip() or 0.0),
                        plannedPercentage=(float(perc_entry.get().strip()) if perc_entry.get().strip() else None),
                        categoryLimit=float(limit_entry.get().strip() or 0.0)
                    )

                    cid = budget_db_obj.create_category(new_cat, budget.budgetID)
                    cat_list.insert(tk.END, f"{cid} | {new_cat.name} | {new_cat.type} | ${new_cat.plannedAmnt:.2f}")
                    refresh_cat_and_budget()
                    win.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Enter valid numeric values.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add category: {e}")

            tk.Button(win, text="Add Category", command=save_new_category).pack(pady=8)

        #Function used to delete a selected category from the budget.
        def delete_selected_category():
            sel_idx = cat_list.curselection()
            if not sel_idx:
                messagebox.showwarning("No Selection", "Select a category to delete.")
                return
            item_text = cat_list.get(sel_idx[0])
            cat_id = int(item_text.split("|")[0].strip())
            if not messagebox.askyesno("Confirm Delete", "Delete this category?"):
                return
            try:
                budget_db_obj.delete_category(cat_id)
                cat_list.delete(sel_idx[0])
                refresh_cat_and_budget()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete category: {e}")

        #Function used to edit a selected category from the budget.
        def edit_selected_category():
            sel_idx = cat_list.curselection()
            if not sel_idx:
                messagebox.showwarning("No Selection", "Select a category to edit.")
                return
            item_text = cat_list.get(sel_idx[0])
            cat_id = int(item_text.split("|")[0].strip())
            cat = next((c for c in categories if c.categoryID == cat_id), None)
            if not cat:
                messagebox.showerror("Error", "Category not found.")
                return

            win = tk.Toplevel(cat_win)
            win.title("Edit Category")
            win.geometry("350x300")
            win.grab_set()

            tk.Label(win, text="Category Name:").pack()
            name_entry = tk.Entry(win); name_entry.insert(0, cat.name); name_entry.pack()

            tk.Label(win, text="Type:").pack()
            type_entry = tk.Entry(win); type_entry.insert(0, cat.type); type_entry.pack()

            tk.Label(win, text="Planned Amount:").pack()
            amount_entry = tk.Entry(win); amount_entry.insert(0, str(cat.plannedAmnt)); amount_entry.pack()

            tk.Label(win, text="Planned Percentage:").pack()
            perc_entry = tk.Entry(win); perc_entry.insert(0, str(cat.plannedPercentage) if cat.plannedPercentage is not None else ""); perc_entry.pack()

            tk.Label(win, text="Limit:").pack()
            limit_entry = tk.Entry(win); limit_entry.insert(0, str(cat.categoryLimit)); limit_entry.pack()

            #simply saving the edited category.
            def save_edit():
                try:
                    cat.name = name_entry.get().strip()
                    cat.type = type_entry.get().strip()
                    cat.plannedAmnt = float(amount_entry.get().strip() or 0.0)
                    cat.plannedPercentage = (float(perc_entry.get().strip()) if perc_entry.get().strip() else None)
                    cat.categoryLimit = float(limit_entry.get().strip() or 0.0)

                    budget_db_obj.update_category(cat)
                    refresh_cat_and_budget()
                    win.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Enter valid numeric values.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save category: {e}")

            tk.Button(win, text="Save Category", command=save_edit).pack(pady=8)

        #Function used to refresh the category list and budget remaining/total values.
        def refresh_cat_and_budget():
            cat_list.delete(0, tk.END)
            new_cats = budget_db_obj.load_categories_for_budget(budget.budgetID)
            for c in new_cats:
                cat_list.insert(tk.END, f"{c.categoryID} | {c.name} | {c.type} | ${c.plannedAmnt:.2f}")
            load_budget_entries(user_id, db, tree)

        # Buttons used for the category manager.
        btn_frame = tk.Frame(cat_win)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Add Category", command=add_category_popup).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Edit Category", command=edit_selected_category).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Delete Category", command=delete_selected_category).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Close", command=cat_win.destroy).grid(row=0, column=3, padx=6)
