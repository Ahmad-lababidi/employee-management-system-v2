import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import logging
from config import API_BASE_URL as API_URL

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Employee System", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Employee Management"])

def fetch_employees():
    try:
        response = requests.get(f"{API_URL}/employees", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        st.error("Failed to load employee data.")
        return []

if page == "Dashboard":
    st.title("Employee Dashboard")
    data = fetch_employees()

    if data:
        df = pd.DataFrame(data)
        st.subheader("Employee Data")
        st.dataframe(df)

        st.subheader("Analytics")
        avg_salary = df['salary'].mean()
        st.metric("Average Salary", f"${avg_salary:,.2f}")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Employees per Department")
            dept_counts = df['department'].value_counts()
            fig, ax = plt.subplots()
            dept_counts.plot(kind='bar', ax=ax, color='skyblue')
            st.pyplot(fig)

        with col2:
            st.write("Salary Distribution")
            fig2, ax2 = plt.subplots()
            df['salary'].plot(kind='hist', ax=ax2, bins=10, color='lightgreen')
            st.pyplot(fig2)
    else:
        st.info("No employee data available.")

elif page == "Employee Management":
    st.title("Employee Management")

    action = st.radio("Action", ["Add Employee", "Update Employee", "Delete Employee"])

    if action == "Add Employee":
        with st.form("add_form"):
            name = st.text_input("Name")
            dept = st.text_input("Department")
            salary = st.number_input("Salary", min_value=0.0)
            hire_date = st.date_input("Hire Date")
            submit = st.form_submit_button("Add")

            if submit:
                try:
                    payload = {"name": name, "department": dept, "salary": salary, "hire_date": str(hire_date)}
                    res = requests.post(f"{API_URL}/employees", json=payload, timeout=10)
                    if res.ok:
                        st.success("Employee added!")
                        st.rerun()
                    else:
                        st.error(f"Failed to add employee: {res.text}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Add error: {e}")
                    st.error("Network error occurred.")

    elif action == "Update Employee":
        emp_id = st.number_input("Employee ID to Update", min_value=1)
        with st.form("update_form"):
            name = st.text_input("New Name")
            dept = st.text_input("New Department")
            salary = st.number_input("New Salary", min_value=0.0)
            hire_date = st.date_input("New Hire Date")
            submit = st.form_submit_button("Update")

            if submit:
                try:
                    payload = {"name": name, "department": dept, "salary": salary, "hire_date": str(hire_date)}
                    res = requests.put(f"{API_URL}/employees/{emp_id}", json=payload, timeout=10)
                    if res.ok:
                        st.success("Employee updated!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update: {res.text}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Update error: {e}")
                    st.error("Network error occurred.")

    elif action == "Delete Employee":
        emp_id = st.number_input("Employee ID to Delete", min_value=1)
        if st.button("Delete"):
            try:
                res = requests.delete(f"{API_URL}/employees/{emp_id}", timeout=10)
                if res.ok:
                    st.success("Employee deleted!")
                    st.rerun()
                else:
                    st.error(f"Failed to delete: {res.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Delete error: {e}")
                st.error("Network error occurred.")
