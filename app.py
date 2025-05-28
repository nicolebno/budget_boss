import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Set file paths
EXPENSES_FILE = "expenses.csv"
INCOME_FILE = "income.csv"
SUGGESTIONS_FILE = "suggestions.csv"

# Initialize files if they don't exist
def initialize_file(file_path, columns):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

initialize_file(EXPENSES_FILE, ["Date", "Description", "Expected", "Actual", "Recurring"])
initialize_file(INCOME_FILE, ["Date", "Source", "Expected", "Actual", "Notes"])
initialize_file(SUGGESTIONS_FILE, ["Date", "Name", "Suggestion"])

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# App layout
st.set_page_config(page_title="Bueno Budget Dashboard", layout="wide")
st.title("💸 Bueno Budget Dashboard")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "💵 Income Tracker", "💳 Expenses", "🏝 Vacation Fund", "💡 Suggestions"])

# --- Dashboard ---
with tab1:
    st.header("Overview: Expected vs. Actual")
    income_df = load_data(INCOME_FILE)
    expenses_df = load_data(EXPENSES_FILE)

    total_expected_income = income_df["Expected"].sum()
    total_actual_income = income_df["Actual"].sum()
    total_expected_expense = expenses_df["Expected"].sum()
    total_actual_expense = expenses_df["Actual"].sum()

    st.subheader("Income")
    st.metric("Expected Income", f"${total_expected_income:,.2f}")
    st.metric("Actual Income", f"${total_actual_income:,.2f}")
    if total_expected_income > 0:
        st.progress(min(total_actual_income / total_expected_income, 1.0))
    else:
        st.text("No expected income entered yet.")

    st.subheader("Expenses")
    st.metric("Expected Expenses", f"${total_expected_expense:,.2f}")
    st.metric("Actual Expenses", f"${total_actual_expense:,.2f}")
    if total_expected_expense > 0:
        st.progress(min(total_actual_expense / total_expected_expense, 1.0))
    else:
        st.text("No expected expenses entered yet.")

# --- Income Tracker ---
with tab2:
    st.header("Expected vs. Actual Income")
    income_df = load_data(INCOME_FILE)
    st.dataframe(income_df)

    with st.form("Add Income"):
        date = st.date_input("Date", key="idate")
        source = st.text_input("Source", key="isource")
        expected = st.number_input("Expected Amount", step=0.01, key="iexp")
        actual = st.number_input("Actual Amount", step=0.01, key="iact")
        notes = st.text_input("Notes", key="inote")
        submit_income = st.form_submit_button("Add Income")
        if submit_income:
            new_row = pd.DataFrame([[date, source, expected, actual, notes]], columns=income_df.columns)
            income_df = pd.concat([income_df, new_row], ignore_index=True)
            save_data(income_df, INCOME_FILE)
            st.success("Income entry added.")

# --- Expenses ---
with tab3:
    st.header("Expected vs. Actual Expenses")
    expenses_df = load_data(EXPENSES_FILE)
    st.dataframe(expenses_df)

    with st.form("Add Expense"):
        date = st.date_input("Date", key="edate")
        desc = st.text_input("Description", key="edesc")
        expected = st.number_input("Expected Amount", step=0.01, key="eexp")
        actual = st.number_input("Actual Amount", step=0.01, key="eact")
        rec = st.checkbox("Recurring", key="erec")
        submit_expense = st.form_submit_button("Add Expense")
        if submit_expense:
            new_row = pd.DataFrame([[date, desc, expected, actual, rec]], columns=expenses_df.columns)
            expenses_df = pd.concat([expenses_df, new_row], ignore_index=True)
            save_data(expenses_df, EXPENSES_FILE)
            st.success("Expense entry added.")

# --- Vacation Fund ---
with tab4:
    st.header("Vacation Fund Tracker")
    st.info("This section will track all vacation-related savings and expenses in the future. For now, use the Expenses tab to log those manually.")

# --- Suggestions ---
with tab5:
    st.header("Suggestions for Improvements")
    suggestions_df = load_data(SUGGESTIONS_FILE)
    st.dataframe(suggestions_df)

    with st.form("Add Suggestion"):
        date = datetime.today().strftime('%Y-%m-%d')
        name = st.text_input("Your Name", key="sname")
        suggestion = st.text_area("Suggestion", key="sug")
        submit_suggestion = st.form_submit_button("Submit Suggestion")
        if submit_suggestion:
            new_row = pd.DataFrame([[date, name, suggestion]], columns=suggestions_df.columns)
            suggestions_df = pd.concat([suggestions_df, new_row], ignore_index=True)
            save_data(suggestions_df, SUGGESTIONS_FILE)
            st.success("Suggestion submitted. Thank you!")
