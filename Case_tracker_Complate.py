import streamlit as st
import os
import pandas as pd

# Helper functions to read and write cases from a file
CASES_FILE = "cases.txt"

def add_case(case_id, case_name, client_name, status):
    with open(CASES_FILE, "a") as file:
        file.write(f"{case_id},{case_name},{client_name},{status}\n")
    st.success(f"Case {case_name} added successfully!")

def get_cases():
    if not os.path.exists(CASES_FILE):
        return []
    with open(CASES_FILE, "r") as file:
        cases = [line.strip().split(",") for line in file.readlines()]
    return cases

def search_case(case_name):
    cases = get_cases()
    for case in cases:
        if case[1].lower() == case_name.lower():
            return case
    return None

def delete_case(case_name):
    cases = get_cases()
    updated_cases = [case for case in cases if case[1].lower() != case_name.lower()]
    
    with open(CASES_FILE, "w") as file:
        for case in updated_cases:
            file.write(f"{case[0]},{case[1]},{case[2]},{case[3]}\n")
    
    if len(cases) != len(updated_cases):
        st.success(f"Case {case_name} deleted successfully!")
    else:
        st.error(f"Case {case_name} not found.")

def update_case(case_id, case_name, client_name, status):
    cases = get_cases()
    updated_cases = []
    case_found = False
    
    for case in cases:
        if case[0] == case_id:
            updated_cases.append([case_id, case_name, client_name, status])
            case_found = True
        else:
            updated_cases.append(case)
    
    with open(CASES_FILE, "w") as file:
        for case in updated_cases:
            file.write(f"{case[0]},{case[1]},{case[2]},{case[3]}\n")
    
    if case_found:
        st.success(f"Case {case_id} updated successfully!")
    else:
        st.error(f"Case {case_id} not found.")

# Streamlit app starts here
st.title("⚖️ Legal Case Tracker")

menu = ["Add Case", "View All Cases", "Search Case", "Update Case", "Delete Case", "Exit"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Add Case":
    st.subheader("Add a New Case")
    case_id = st.text_input("Enter case ID:")
    case_name = st.text_input("Enter case name:")
    client_name = st.text_input("Enter client name:")
    status = st.selectbox("Status", ["Open", "Closed", "Pending"])
    
    if st.button("Add Case"):
        if case_id and case_name and client_name:
            add_case(case_id, case_name, client_name, status)
        else:
            st.error("Please provide case ID, name, and client name.")

elif choice == "View All Cases":
    st.subheader("View All Cases")
    cases = get_cases()
    
    if cases:
        df = pd.DataFrame(cases, columns=["Case ID", "Case Name", "Client Name", "Status"])
        st.table(df)  # Display cases in table format
    else:
        st.info("No cases available.")

elif choice == "Search Case":
    st.subheader("Search for a Case")
    search_name = st.text_input("Enter the case name to search:")
    
    if st.button("Search"):
        case = search_case(search_name)
        if case:
            df = pd.DataFrame([case], columns=["Case ID", "Case Name", "Client Name", "Status"])
            st.table(df)  # Display search result in table format
        else:
            st.error(f"Case {search_name} not found.")

elif choice == "Update Case":
    st.subheader("Update a Case")
    update_id = st.text_input("Enter case ID to update:")
    
    if st.button("Load Case"):
        case = search_case(update_id)
        if case:
            case_name = st.text_input("Case Name", value=case[1])
            client_name = st.text_input("Client Name", value=case[2])
            status = st.selectbox("Status", ["Open", "Closed", "Pending"], index=["Open", "Closed", "Pending"].index(case[3]))
            
            if st.button("Update Case"):
                update_case(update_id, case_name, client_name, status)
        else:
            st.error(f"Case {update_id} not found.")

elif choice == "Delete Case":
    st.subheader("Delete a Case")
    delete_name = st.text_input("Enter the case name to delete:")
    
    if st.button("Delete"):
        if delete_name:
            delete_case(delete_name)
        else:
            st.error("Please provide a case name to delete.")

elif choice == "Exit":
    st.write("Thank you for using the Legal Case Tracker app!")
    st.stop()
