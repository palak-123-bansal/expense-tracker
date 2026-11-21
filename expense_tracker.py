"""Simple Expense Tracker
Log expenses, save them to a CSV, view monthly totals,
and visualize spending by category with a pie chart.
"""

import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

FILE = "expenses.csv"
COLUMNS = ["date", "category", "amount", "note"]
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]


def load_data():
    """Load expenses from CSV, or return an empty table if no file yet."""
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=COLUMNS)


def save_data(df):
    df.to_csv(FILE, index=False)


def add_expense(df):
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")

    try:
        choice = int(input("Choose category number: "))
        category = CATEGORIES[choice - 1]
        amount = float(input("Amount: "))
    except (ValueError, IndexError):
        print("Invalid input. Expense not added.")
        return df

    note = input("Note (optional): ")
    date = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    new_row = pd.DataFrame(
        [{"date": date, "category": category, "amount": amount, "note": note}]
    )
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    print(f"Added: {category} - {amount:.2f}")
    return df


def view_expenses(df):
    if df.empty:
        print("\nNo expenses yet.")
        return
    print("\n--- All Expenses ---")
    print(df.to_string(index=False))
    print(f"\nTotal spent: {df['amount'].sum():.2f}")


def monthly_summary(df):
    if df.empty:
        print("\nNo expenses yet.")
        return
    data = df.copy()
    data["month"] = pd.to_datetime(data["date"]).dt.to_period("M")
    summary = data.groupby("month")["amount"].sum()
    print("\n--- Monthly Totals ---")
    print(summary.to_string())


def category_chart(df):
    if df.empty:
        print("\nNo expenses yet.")
        return
    totals = df.groupby("category")["amount"].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(totals, labels=totals.index, autopct="%1.1f%%", startangle=90)
    plt.title("Spending by Category")
    plt.savefig("spending_chart.png")
    print("Chart saved as spending_chart.png")
    plt.show()


def main():
    df = load_data()
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Monthly summary")
        print("4. Spending chart")
        print("5. Exit")
        option = input("Choose an option: ").strip()

        if option == "1":
            df = add_expense(df)
        elif option == "2":
            view_expenses(df)
        elif option == "3":
            monthly_summary(df)
        elif option == "4":
            category_chart(df)
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose 1-5.")


if __name__ == "__main__":
    main()
