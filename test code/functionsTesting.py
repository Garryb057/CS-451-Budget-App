from datetime import date
from loginFail import login_user
from Money import Income
from incomeManagement import calculate_total_monthly_income, add_one_time_income

#Needs security implementation, for now it is just a simple checking function.
def test_login():
    print("=== LOGIN TEST ===\n" 
    "Correct credentials are\n" 
    "email: user@example.com\n"
    "password: 123\n")
    email = input("Email: ")
    password = input("Password: ")
    success, message = login_user(email, password)
    print(message)
    print()

#Come back to this again after project is more fleshed out, 
#previousIncome call should be gone, and the current income_Sources is only for testing.
def test_total_monthly_income():
    print("=== MONTHLY INCOME CALCULATION TEST ===")
    print("Previous Monthly Income: $5000")
    previousIncome = 5000
    income_sources = []

    income_sources.append(Income(1, 1, "Part-time Job", 500, "weekly", date(2025, 10, 1)))
    income_sources.append(Income(2, 1, "Main Job", 2000, "biweekly", date(2025, 10, 3)))
    income_sources.append(Income(3, 1, "Freelance Work", 800, "monthly", date(2025, 10, 5)))
    income_sources.append(Income(4, 1, "Stock Dividends", 2400, "annual", date(2025, 10, 6)))

    total_income = calculate_total_monthly_income(income_sources, previousIncome)


    print("Added Income Sources:\n")
    print(f"{'Income Name':<20} {'Frequency':<10} {'Amount':>10}")
    print("-" * 45)

    for income in income_sources:
        print(f"{income.name:<20} {income.payFrequency:<10} ${income.amount:>9.2f}")

    print("-" * 45)
    print(f"{'Total Monthly Income:':<30} ${total_income:>9.2f}")


#Adds a one-time income entry for the user.
#This income does not have a recurring schedule.
def test_one_time_income():
    print("=== ONE TIME INCOME CALCULATION TEST ===")
    print("Current Monthly Income: $5000")
    userID = 1
    totalIncome = 5000

    income1 = add_one_time_income(userID, "Freelance Project", 1200, date(2025, 10, 10))
    income2 = add_one_time_income(userID, "Money Transfer", 300, date(2025, 10, 15))

    totalIncome += income1.amount + income2.amount

    print(f"{'Total Monthly Income:':<30} ${totalIncome:>9.2f}")

def main():

    test_login()
    test_total_monthly_income()
    test_one_time_income()

if __name__ == "__main__":
    main()