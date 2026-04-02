import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Precision Hardware", layout="centered")
st.title("Precision Hardware")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

users = []

json_path = Path("users.json")
if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)

#load data
inventory = []

json_path_inventory = Path("inventory.json")

#load the data from a json file
if json_path_inventory.exists():
    with json_path_inventory.open("r", encoding= "utf-8") as f:
        inventory = json.load(f)


if st.session_state["role"] == "Employee":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the employee dashboard")
        if st.button("Go to Dashboard", key= "dashboard_view_btn", type= "primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Dashboard")

        tab1, tab2, tab3 = st.tabs(["Catalog", "Daily Sales", "Inventory"])

        with tab1:

            tab_option = st.radio("View/Search", ["View", "Search"], horizontal=True)
            if tab_option == "View":
                st.dataframe(inventory)
            else:
                names = []
                for item in inventory:
                    names.append(inventory["name"])

                selected_name = st.selectbox("Select a title", names, key="selected_title")

                selected_item = {}

                for item in inventory:
                    if item['title'] == selected_name:
                        selected_item = item
                        break
                
                st.divider()
                selected_item = st.selectbox("Select Title", options=inventory, format_func=lambda x: f"{x['title']} ({x['type']})")

                if selected_item:
                    with st.expander("Assignment Details", expanded=True):
                        st.markdown(f"### Title: {selected_item['name']}")
                        st.markdown(f"Description: {selected_item['description']}")
                        st.markdown(f"Type: **{selected_item['type']}**")

        with tab2:
            #st.markdown("## Add New Assignment")
            #st.markdown("### Add New Assignment")

            #title = st.text_input("Title")
            #description = st.text_area("Description",placeholder="normalization is covered here",
                                    help="Here you are entering the assignment details")
            #points = st.number_input("Points")

            #assignment_type = st.text_input("Assignment Type")
            #assignment_type = st.radio("Type", ("Homework", "Lab"), horizontal=True)
            #testing = st.text("Homework Type")
            #assignment_type2 = st.selectbox("Type", ("Select an option","Homework", "Lab", "other"))
            #if assignment_type2 == "other":
                #assignment_type2 = st.text_input("Type", placeholder="Enter the assignment Type")

            #due_date = st.date_input("Due Date")

            #btn_save = st.button("Save", width="stretch", disabled=False)

            #if btn_save:
                #if not title:
                    #st.warning("Title needs to be provided!")
                #else:
                    #with st.spinner("Assignment is being reached....."):
                        #time.sleep(5)

                        #new_assignment_id = "HW" + str(next_assignment_id_number)
                        #next_assignment_id_number += 1

                        #assignments.append(
                            #{
                                #"id":str(uuid.uuid4()),
                                #"title": title,
                                #"description": description,
                                #"points": points,
                                #"type": assignment_type
                            #}
                        #)

                        #record into json file
                        #with json_path_assignment.open("w",encoding="utf-8") as f:
                            #json.dump(assignments,f)

                        #st.success("New Assignement is recorded!")
                        #st.info("This is a new assignment")
                        #time.sleep(4)
                        #st.dataframe(assignments)
                        #st.rerun()
            st.empty()

        with tab3:
            #st.markdown("## Update an Assignment")
            #titles = []

            #for assignment in assignments:
                #titles.append(assignment['title'])

            #selected_item = st.selectbox("Select an assignment", titles, key="selected_title_edit")

            #assignment_edit = {}
            #for assignment in assignments:
                #if assignment['title'] == selected_item:
                    #assignment_edit = assignment
                    #break

            #if assignment_edit:
                #edit_title = st.text_input("Title", key=f"edit_title_{assignment_edit['id']}", value= assignment_edit['title'])
                #edit_description = st.text_area("Description", key=f"edit_description_{assignment_edit['id']}", value= assignment_edit['description'])

                #type_options = ['Homework', 'Lab']
                #selected_index = type_options.index(assignment_edit["type"])

                #edit_type = st.radio("Type", type_options, key=f"edit_type_{assignment_edit['id']}", index= selected_index)

            #btn_update = st.button("Update", key="update_button", type="secondary", use_container_width=True)
            #if btn_update:
                #with st.spinner("Updating..."):
                    #time.sleep(5)
                    #assignment_edit["title"] = edit_title
                    #assignment_edit["description"] = edit_description

                    #with json_path.open("w") as f:
                        #json.dump(assignments,f)

                    #st.success("Assignment is updated!")
                    #time.sleep(5)
                    #st.rerun()
            st.empty()

elif st.session_state["role"] == "Admin":
    st.markdown("Welcome! This is the Admin dashboard")

    if st.button("Log out", type="primary", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "login"
        time.sleep(4)
        st.rerun()

else:
        # --- LOGIN ---
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email", key="email_login")
        password_input = st.text_input("Password", type="password", key="password_login")
    
        if st.button("Log In", type="primary", use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) # Fake backend delay
            
                # Find user
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break

                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user["role"]
                    st.session_state["page"] = "home"

                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    # --- REGISTRATION ---
    st.subheader("New Instructor Account")
    with st.container(border=True):
        new_email = st.text_input("Email", key="email_register")
        new_password = st.text_input("Password", type="password", key="password_edit")
    
        if st.button("Create Account", key= "register_btn"):
            with st.spinner("Creating account..."):
                time.sleep(2) # Fake backend delay
                # ... (Assume validation logic here) ...
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Instructor"
                })

                with open(json_path, "w") as f:
                    json.dump(users, f)

                st.success("Account created!")
                st.rerun()

    st.write("---")
    st.dataframe(users)



with st.sidebar:
    st.markdown("Course Manager Sidebar")
    if st.session_state["logged_in"] == True:
        user = st.session_state["user"]
        st.markdown(f"Logged User Email: {user["email"]}")