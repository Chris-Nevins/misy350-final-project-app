import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

#streamlit run Registration.py

users = []

json_path = Path("users.json")
if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)

# --- REGISTRATION ---
st.subheader("Register a New Account")
with st.container(border=True):
    new_email = st.text_input("Email", key="email_register")

    new_password = st.text_input("Password", type="password", key="password_edit")

    user_role = ["", "Owner", "Employee"]
    new_role = st.selectbox("Role", user_role)

    if st.button("Create Account", key= "register_btn"):
        reg_errors = []

        for user in users:
            if new_email.lower() == user["email"].lower():
                reg_errors.append("That email already exists, please login instead")
                break

        for user in users:
            if new_password.lower() == user["password"].lower():
                reg_errors.append("That password is already taken, please try again")
                break

        if new_email.lower() == "":
            reg_errors.append("Please enter your email")

        if new_role == "":
            reg_errors.append("Please enter a role")
        
        if reg_errors:
            for invalid in reg_errors:
                st.error(invalid)
        else:
            with st.spinner("Creating account..."):
                time.sleep(2) 

                for user in users:
                    new_id = int(user["id"]) + 1

                users.append({
                    "id": str(new_id),
                    "email": new_email,
                    "password": new_password,
                    "role": new_role
                })

                with open(json_path, "w") as f:
                    json.dump(users, f)

                st.success("Account created!")
                st.rerun()

st.write("---")
st.dataframe(users)