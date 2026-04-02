import streamlit as st
from datetime import datetime
import json
from pathlib import Path
import uuid
import time

#st.set_page_config(page_title="Smart Coffee Kiosk Application")
st.title("Precision Hardware")

#=============================
# A. User Registration & Login
#=============================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

users = [
    {
    "id":"1",
    "email":"admin@school.edu",
    "full_name":"System Admin",
    "password":"123ssag@43AE",
    "role":"Admin",
    "registerd_at":"..."
    }
]

json_path = Path("users.json")
if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)

# Login
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

# Registration
st.subheader("Create a New account")
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

#=============================
# B. Session State Management
#=============================

#=============================
# C. Role-Based Routing
#=============================

#=============================
# D. JSON-Based Data Storage
#=============================

#=============================
# E. CRUD System
#=============================


#hi im luke
