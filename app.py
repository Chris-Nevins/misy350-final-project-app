import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Precision Hardware", layout="centered")
st.title("Precision Hardware")

#=============================
# A. User Registration
#=============================

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


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

#Users
users = []

json_path = Path("users.json")

if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)

#Inventory
inventory = []

json_path_inventory = Path("inventory.json")

if json_path_inventory.exists():
    with json_path_inventory.open("r", encoding= "utf-8") as f:
        inventory = json.load(f)

#Product Log (might need to change the wordings)
product_log = []

json_path_product_log = Path("product_log.json")

if json_path_product_log.exists():
    with json_path_product_log.open("r", encoding= "utf-8") as f:
        product_log = json.load(f)


if "product_log" not in st.session_state:
   st.session_state["product_log"] = product_log

if st.session_state["role"] == "Employee":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the employee dashboard")
        if st.button("Go to Dashboard", key= "dashboard_view_btn", type= "primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Dashboard")

        if st.button("Log out", type="primary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            time.sleep(1)
            st.rerun()

        tab1, tab2, tab3 = st.tabs(["Catalog", "Inventory", "Daily Sales"])

        with tab1:
            st.header("Current Catalog")
            with st.container(border=True):
                search = st.text_input("Search", placeholder= "filter items by name")
                viewing_inventory = []
                if search:
                    for item in inventory:
                        if search.lower() in item["name"].lower():
                            viewing_inventory.append(item)
                else:
                    viewing_inventory = inventory

                if viewing_inventory:
                    st.subheader("Current Inventory")
                    st.dataframe(viewing_inventory, use_container_width= True)

                    total_stock = sum(i["stock"] for i in viewing_inventory)#
                    st.metric("Total Stock", total_stock)

                else:
                    st.error("No item(s) found please try again")

        with tab2:
            with st.container(border=True):
                st.header("Inventory")
                if viewing_inventory:
                    st.dataframe(viewing_inventory, use_container_width= True)

                    total_stock = sum(i["stock"] for i in viewing_inventory)#
                    st.metric("Total Stock", total_stock)

                low_stock_items = [i for i in viewing_inventory if i["stock"] < 5]
                if low_stock_items:
                    st.warning("Low stock on the following items:")
                    st.dataframe(low_stock_items, use_container_width= True)
                else:
                    st.success("All items are in sufficient stock")
                    time.sleep(3)
                    st.rerun()
                    
                matching_products = []
                for product in st.session_state["product_log"]:
                    for item in viewing_inventory:
                        if product["Item"] == item["name"]:
                            matching_products.append(product)        
                            break

        with tab3:
            with st.container(border=True):
                st.header("Daily Sales")
                if matching_products:
                    st.dataframe(matching_products, use_container_width= True)
                else:
                    st.info("No product found for the matching item(s).")

            with st.container(border=True):
                st.header("Deduct from Inventory")

                sold_items = []
                for sold in product_log:
                    sold_items.append(sold["Item"])

                Sel_Name = st.selectbox("Select sold item", sold_items)

                sel_sale = []
                for sale in product_log:
                    if sale["Item"] == Sel_Name:
                        sel_sale = sale
                        break

                sel_inv = []
                for item in inventory:
                    if item["name"] == Sel_Name:
                        sel_inv = item
                        break

                if sel_sale and sel_inv:
                    st.write(f"Quantity Sold: {sel_sale["Amount sold"]}")
                    st.write(f"Current Inventory: {sel_inv["stock"]}")

                    Deduct_btn = st.button("Edit Inventory")

                    if Deduct_btn:
                        sel_inv["stock"] -= sel_sale["Amount sold"]

                        with json_path_inventory.open("w", encoding= "utf-8") as f:
                            json.dump(inventory, f, indent=4)

                        st.success("Inventory Changed")
                        st.write(f"New Inventory: {sel_inv["stock"]}")
                        time.sleep(3)
                        st.rerun()

                else:
                    st.error("Unable to find an item that matches from Inventory or Product Log")
                                

elif st.session_state["role"] == "Owner":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the Owner dashboard")
        if st.button("Go to Dashboard", key= "dashboard_view_btn", type= "primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Dashboard")    

        if st.button("Log out", type="primary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            time.sleep(4)
            st.rerun()

        tab1, tab2 = st.tabs(["Add New Product/Update Prices", "Restocking/Deleting"])

        with tab1:
            # Section 1: Add New Product (Create)
            if st.header("Add New Product"):
                with st.container(border=True):
                    # Item ID
                    New_ID = st.number_input("Set an Unique Numerical ID", step = 1.0, format="%.f")

                    # Item Name
                    New_Item_Name = st.text_input("Name")

                    # Item Category
                    Current_Cat = ["","GPU", "Memory", "Motherboard", "Processor", "Power Supply", "Case", "Cooling", "Networking"]
                    New_Cat = st.selectbox("Category", Current_Cat)

                    # Item Price
                    New_Price = st.number_input("Insert Price", min_value=0.0, step=1.0, format="%.2f")

                    # Item Stock
                    New_Stock = st.number_input("Amount to inventory", min_value=0.0, step=1.0, format="%.f")


                    btn_add = st.button("Submit Change")

                    if btn_add:
                        errors = []

                        # duplicate ID
                        for item_id in inventory:
                            if New_ID == item_id["id"]:
                                errors.append("That ID has already been taken")
                                break

                        # duplicate name
                        for item_name in inventory:
                            if New_Item_Name.replace(" ", "").strip().lower() == item_name["name"].replace(" ", "").strip().lower():
                                errors.append("That Item already exists, please use restock inventory instead")
                                break
                        # Confirm empty name
                        if New_Item_Name.strip() == "":
                            errors.append("Please enter a name")

                        # Confirm Category
                        if New_Cat == "":
                            errors.append("Please select a category")
                            
                        # Confirm Price
                        if New_Price <= 0:
                            errors.append("Please enter a price")

                        # Confirm Stock
                        if New_Stock <= 0:
                            errors.append("Please enter a quantity")
                        
                        if errors:
                            for error in errors:
                                st.error(error)
                        else:
                            New_Inventory = {
                                "id": int(New_ID),
                                "name": New_Item_Name,
                                "category": New_Cat,
                                "price": float(New_Price),
                                "stock": int(New_Stock)
                                }

                            inventory.append(New_Inventory)

                            with json_path_inventory.open("w", encoding= "utf-8") as f:
                                json.dump(inventory, f, indent=4)

                            st.success("New Product Added")
                            time.sleep(1)
                            st.rerun()

            # Section 2: Update Prices (Read)
            st.header("Update Prices")
            with st.container(border=True):
                search = st.text_input("Search", placeholder= "filter items by name")
                filtered_inventory = []
                if search:
                    for item in inventory:
                        if search.lower() in item["name"].lower():
                            filtered_inventory.append(item)
                else:
                    filtered_inventory = inventory

                if len(filtered_inventory) == 1:
                    selected_item = filtered_inventory[0]

                    new_price = st.number_input(
                    f"Set new price for {selected_item['name']}",
                    min_value=0.0,value=float(selected_item["price"]),step=1.0)

                    if st.button("Update Price"):
                        selected_item["price"] = new_price

                        with json_path_inventory.open("w", encoding="utf-8") as f:
                            json.dump(inventory, f, indent=4)

                        st.success(f"Price for {selected_item['name']} updated to ${new_price:.2f}")
                        time.sleep(1)
                        st.rerun()

                if filtered_inventory:
                    st.subheader("Current Inventory")
                    st.dataframe(filtered_inventory, use_container_width= True)

                else:
                    st.error("No item(s) found please try again")

        with tab2:
            # Section 3: Restock (Update)
            st.header("Restock Inventory")
            with st.container(border=True):
                if not filtered_inventory:
                    st.warning("No inventory available to restock")

                else:
                    item_selected = [fi["name"] for fi in filtered_inventory]
                    Select_Name = st.selectbox("Select an item to restock", item_selected)
                    selected_item = None

                    for item in filtered_inventory:
                        if item["name"] == Select_Name:
                            selected_item = item
                            break

                    Restock_Quantity = st.number_input("Restock Quantity", min_value=1, step=1)

                    if selected_item:
                        st.write(f"Current stock: {selected_item["stock"]}")

                    if st.button("Restock"):
                        if selected_item is None:
                            st.error("Please select an item")
                        else:
                            selected_item["stock"] += Restock_Quantity

                            with open(json_path_inventory, "w") as f:
                                json.dump(inventory, f, indent=4)

                            st.success(f"{selected_item["name"]} is successfully restocked")
                            st.success(f"New Stock: {selected_item["stock"]}")
                            time.sleep(1)
                            st.rerun()

            # Section 4: Deleting Discontinued Items (Delete/Cancel)
            st.header("Delete Discontinued Item(s)")
            with st.container(border=True):
                with st.container(border=True):
                    product_names = []
                    for dis_item in inventory:
                        product_names.append(dis_item["name"])
                    Selected_dis_product = st.selectbox("Select the discontinued item", product_names)

                    discontinued_name = {}
                    for dis_item in inventory:
                        if dis_item["name"] == Selected_dis_product:
                            discontinued_name = dis_item
                            break
                    
                    if discontinued_name:
                        st.write("### Selected Item Details:")
                        st.write(f"**Item ID**: {discontinued_name["id"]}")
                        st.write(f"**Name**: {discontinued_name["name"]}")
                        st.write(f"**Category**: {discontinued_name["category"]}")
                        st.write(f"**Price**: {discontinued_name["price"]}")
                        st.write(f"**Stock**: {discontinued_name["stock"]}")

                        btn_delete = st.button("Delete Item")

                        if btn_delete:
                            updated_inv= []

                            for dis_item in inventory:
                                if dis_item["name"] != Selected_dis_product:
                                    updated_inv.append(dis_item)

                            inventory = updated_inv

                            with json_path_inventory.open("w", encoding="utf-8") as f:
                                json.dump(inventory, f, indent=4)

                            updated_products = []
                            for product in st.session_state["products"]:
                                if product["item"] != Selected_dis_product:
                                    updated_products.append(product)

                            st.session_state["products"] = updated_products

                            st.success(f"{Selected_dis_product} was deleted successfully")
                            time.sleep(1)
                            st.rerun()

else:
        # --- LOGIN ---
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email", key="email_login")
        password_input = st.text_input("Password", type="password", key="password_login")
    
        if st.button("Log In", type="primary", use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2)
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
                    time.sleep(1)
                    st.rerun()
        st.write("---")
        st.dataframe(users)



with st.sidebar:
    st.subheader("**Account Info**")
    if st.session_state["logged_in"] == True:
        user = st.session_state["user"]
        st.markdown(f"User Email: {user["email"]}")
        st.markdown(f"Logged In as: {user["role"]}")
