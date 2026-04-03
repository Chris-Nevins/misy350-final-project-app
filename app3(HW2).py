import streamlit as st
from datetime import datetime
import json
from pathlib import Path 

json_file = Path("inventory.json")

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    # Default data if file doesn't exist
    inventory = []
    with open(json_file, "w") as f:
        json.dump(inventory, f, indent=4) 

st.set_page_config(page_title="Smart Coffee Kiosk", layout="centered")
st.title("Smart Coffee Kiosk App")

products = [
    {
    "product_id": "product_101", 
    "item": "AMD Ryzen 7 7800X3D CPU",
    "category": "Processor", 
    "total": 1350,
    "user_type": "Owner",
    "status": "Changed"
    }
]

if "products" not in st.session_state:
    st.session_state["products"] = products

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
        User_Type = st.text_input("Type of User", placeholder= "Name")

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

                with open(json_file, "w") as f:
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

                with st.expander("View Receipt"):
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

    if filtered_inventory:
        st.subheader("Current Inventory")
        st.dataframe(filtered_inventory, use_container_width= True)

        total_stock = sum(i["stock"] for i in filtered_inventory)
        st.metric("Total Stock", total_stock)

        low_stock_items = [i for i in filtered_inventory if i["stock"] < 10]
        if low_stock_items:
            st.warning("Low stock on the following items:")
            st.dataframe(low_stock_items, use_container_width= True)
        else:
            st.success("All items are in sufficient stock")
        
        matching_products = []
        for product in st.session_state["products"]:
            for item in filtered_inventory:
                if product["item"] == item["name"]:
                    matching_products.append(product)        
                    break

        if matching_products:
            st.subheader("Product(s) for matching item(s)")
            st.dataframe(matching_products, use_container_width= True)
        else:
            st.info("No product found for the matching item(s).")

    else:
        st.error("No item(s) found please try again")

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

                with open(json_file, "w") as f:
                    json.dump(inventory, f, indent=4)

                st.success(f"{selected_item["name"]} is successfully restocked")
                st.success(f"New Stock: {selected_item["stock"]}")

# Section 4: Deleting Discontinued Items (Delete/Cancel)
st.header("Deleting Discontinued Items")
with st.container(border=True):
    products = st.session_state.get("products", [])

    if len(products) == 0:
        st.info("No products found")

    else:
        product_id = []
        for product in products:
            if product["status"] == "Placed":
                product_id.append(product["product_id"])

        if len(product_id) == 0:
            st.info("No active products to cancel")

        else:
            selected_product = st.selectbox("Select Product", product_id, key="cancel_change")
            btn_cancel = st.button("Cancel Change")

            if btn_cancel:
                cancelled = False

                for product in products:
                    if product["product_id"] == selected_product and product["status"] == "Placed":
                        product["status"] = "Cancelled"

                        for item in inventory:
                            if item["name"] == product["item"]:
                                item["stock"] += 1
                                break

                        cancelled = True
                        break

                if cancelled:
                    with json_file.open("w", encoding="utf-8") as f:
                        json.dump(inventory, f, indent=4)

                    st.session_state["products"] = products
                    st.success(f"Product {selected_product} cancelled and change is reversed")
                else:
                    st.warning("Product was already cancelled or not found")
