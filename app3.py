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

orders = [
    {
    "order_id": "Order_101", 
    "customer": "John", 
    "item": "Cold Brew", 
    "total": 8.50, 
    "status": "Placed"
    }
]

if "orders" not in st.session_state:
    st.session_state["orders"] = orders

# Section 1: Place Order (Create)
if st.header("Place Order"):
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
        Customer_Name = st.text_input("Customer Name", placeholder= "Name")

        btn_order = st.button("Submit Order")
        if btn_order:
            if not Customer_Name:
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

                new_order_id = f"Order_{len(st.session_state['orders']) + 101}"

                new_order = {
                    "order_id":new_order_id,
                    "customer":Customer_Name,
                    "item":selected_name["name"],
                    "total":("{:.2f}".format(total_price)),
                    "status":"Placed"
                }
                orders.append(new_order)

                st.session_state["orders"].append(new_order)

                st.success("Order Placed")

                with st.expander("View Receipt"):
                    st.write(f"Order ID: {new_order['order_id']}")
                    st.write(f"Customer: {new_order['customer']}")
                    st.write(f"Item: {new_order['item']}")
                    st.write(f"Total: {new_order['total']}")
                    st.write(f"Status: {new_order['status']}")


# Section 2: View & Search Inventory (Read)
st.header("View & Search Inventory")
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
        
        matching_orders = []
        for order in st.session_state["orders"]:
            for item in filtered_inventory:
                if order["item"] == item["name"]:
                    matching_orders.append(order)        
                    break

        if matching_orders:
            st.subheader("Order(s) for matching item(s)")
            st.dataframe(matching_orders, use_container_width= True)
        else:
            st.info("No order found for the matching item(s).")

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

# Section 4: Manage Orders (Delete/Cancel)
st.header("Manage Orders")
with st.container(border=True):
    orders = st.session_state.get("orders", [])

    if len(orders) == 0:
        st.info("No orders found")

    else:
        order_id = []
        for order in orders:
            if order["status"] == "Placed":
                order_id.append(order["order_id"])

        if len(order_id) == 0:
            st.info("No active orders to cancel")

        else:
            selected_order = st.selectbox("Select Order", order_id, key="cancel_order")
            btn_cancel = st.button("Cancel Order")

            if btn_cancel:
                cancelled = False

                for order in orders:
                    if order["order_id"] == selected_order and order["status"] == "Placed":
                        order["status"] = "Cancelled"

                        for item in inventory:
                            if item["name"] == order["item"]:
                                item["stock"] += 1
                                break

                        cancelled = True
                        break

                if cancelled:
                    with json_file.open("w", encoding="utf-8") as f:
                        json.dump(inventory, f, indent=4)

                    st.session_state["orders"] = orders
                    st.success(f"Order {selected_order} cancelled and stock refunded")
                else:
                    st.warning("Order was already cancelled or not found")
