from datetime import date
from Money import Income


#After adding multiple income sources, calculate the total monthly income.
#Recurring sources (weekly, biweekly, monthly, annual) are converted to monthly amounts.
#Come back to this again after project is more fleshed out, 
#previousIncome call should be gone, and the current income_sources is only for testing.
def calculate_total_monthly_income(income_sources, previousTotal):
    currentTotal = previousTotal

    for income_obj in income_sources:
        amount = income_obj.amount
        payFrequency = income_obj.payFrequency.lower()

        if payFrequency == "weekly":
            currentTotal += amount * 4
        elif payFrequency == "biweekly":
            currentTotal += amount * 2
        elif payFrequency == "monthly":
            currentTotal += amount
        elif payFrequency == "annual":
            currentTotal += amount / 12
    
    return currentTotal

#Adds a one-time income entry for the user.
#This income does not have a recurring schedule.
#Future consideration: Maybe instead of taking in class attributes as parameters it could be empty?
def add_one_time_income(userID, name, amount, datePaid):
    new_income = Income(
        incomeID = 1,
        userID = userID,
        name = name,
        amount = amount,
        payFrequency = "one time",
        datePaid = datePaid
    )
    print(f"Added one time income: {new_income.name} ${new_income.amount} on {new_income.datePaid}")
    return new_income