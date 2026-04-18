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

users = []

json_path = Path("users.json")
if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)

inventory = []

json_path_inventory = Path("inventory.json")

if json_path_inventory.exists():
    with json_path_inventory.open("r", encoding= "utf-8") as f:
        inventory = json.load(f)

products = [
   {
   "product_id": "Product_101",
   "item": "AMD Ryzen 7 7800X3D CPU",
   "category": "Processor",
   "total": 1350,
   "user_type": "Owner",
   "status": "Changed"
   }
]

if "products" not in st.session_state:
   st.session_state["products"] = products

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
            time.sleep(4)
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

                low_stock_items = [i for i in viewing_inventory if i["stock"] < 10]
                if low_stock_items:
                    st.warning("Low stock on the following items:")
                    st.dataframe(low_stock_items, use_container_width= True)
                else:
                    st.success("All items are in sufficient stock")
                    
                matching_products = []
                for product in st.session_state["products"]:
                    for item in viewing_inventory:
                        if product["item"] == item["name"]:
                            matching_products.append(product)        
                            break

        with tab3:
            with st.container(border=True):
                st.header("Daily Sales")
                if matching_products:
                    st.subheader("Product(s) sold/returned/restocked")
                    st.dataframe(matching_products, use_container_width= True)
                else:
                    st.info("No product found for the matching item(s).")

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
                    item_names = []
                    for item in inventory:
                        item_names.append(item["name"])
                    Selected_Item_Name = st.selectbox("Select", item_names)

                    selected_name = {}
                    for item in inventory:
                        if item["name"] == Selected_Item_Name:
                            selected_name = item
                            break

                    Quantity = st.number_input("Insert quantity", placeholder= "Please enter amount", step=1)
                    User_Type = st.text_input("Name", placeholder= "Name")

                    btn_change = st.button("Submit Change")
                    if btn_change:
                        if not User_Type:
                            st.error("Please enter your name")
                        elif selected_name is None:
                            st.error("Please select an item")
                        elif Quantity > selected_name["stock"]:
                            st.error("Out of Stock")
                        elif Quantity == 0:
                            st.error("Please enter the amount")                
                        else:
                            selected_name["stock"] -= Quantity

                            with open(json_path_inventory, "w") as f:
                                json.dump(inventory, f, indent=4)

                            total_price = selected_name["price"] * Quantity

                            new_product_id = f"Product_{len(st.session_state['products']) + 101}"

                            new_product = {
                                "product_id":new_product_id,
                                "item":selected_name["name"],
                                "user_type":User_Type,
                                "total":("{:.2f}".format(total_price)),
                                "status":"Changed"
                            }
                            products.append(new_product)

                            st.session_state["products"].append(new_product)

                            st.success("Product Changed")

                            with st.expander("View Item Record"):
                                st.write(f"Product ID: {new_product['product_id']}")
                                st.write(f"Item: {new_product['item']}")
                                st.write(f"Type of User: {new_product['user_type']}")
                                st.write(f"Total: {new_product['total']}")
                                st.write(f"Status: {new_product['status']}")


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

            # Section 4: Deleting Discontinued Items (Delete/Cancel)
            st.header("Cancel Request")
            with st.container(border=True):
                products = st.session_state.get("products", [])

                if len(products) == 0:
                    st.info("No products found")

                else:
                    product_id = []
                    for product in products:
                        if product["status"] == "Changed":
                            product_id.append(product["product_id"])

                    if len(product_id) == 0:
                        st.info("No active products to cancel")

                    else:
                        selected_product = st.selectbox("Select Product ID", product_id, key="cancel_change")
                        btn_cancel = st.button("Cancel Change")

                        if btn_cancel:
                            cancelled = False

                            for product in products:
                                if product["product_id"] == selected_product and product["status"] == "Changed":
                                    product["status"] = "Cancelled"

                                    for item in inventory:
                                        if item["name"] == product["item"]:
                                            item["stock"] += 1
                                            break

                                    cancelled = True
                                    break

                            if cancelled:
                                with json_path_inventory.open("w", encoding="utf-8") as f:
                                    json.dump(inventory, f, indent=4)

                                st.session_state["products"] = products
                                st.success(f"Product {selected_product} cancelled and change is reversed")
                            else:
                                st.warning("Product was already cancelled or not found")

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
    
        if st.button("Create Account", key= "register_btn"):
            with st.spinner("Creating account..."):
                time.sleep(2)
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Employee"
                })

                with open(json_path, "w") as f:
                    json.dump(users, f)

                st.success("Account created!")
                st.rerun()

        st.write("---")
        st.dataframe(users)



with st.sidebar:
    st.markdown("Inventory Manager Sidebar")
    if st.session_state["logged_in"] == True:
        user = st.session_state["user"]
        st.markdown(f"Logged User Email: {user["email"]}")
