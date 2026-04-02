import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config("Orders Management App", layout="wide", initial_sidebar_state="expanded")


if "page" not in st.session_state:
    st.session_state["page"] = "home"

inventory = [
    {"id": 1, "name": "Espresso", "price": 2.50, "stock": 40},
    {"id": 2, "name": "Latte", "price": 4.25, "stock": 25},
    {"id": 3, "name": "Cold Brew", "price": 3.75, "stock": 30},
    {"id": 4, "name": "Mocha", "price": 4.50, "stock": 20},
    {"id": 5, "name": "Blueberry Muffin", "price": 2.95, "stock": 18}
]

with st.sidebar:
    if st.button("Home", key="home_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()
                
    if st.button("Orders", key="orders_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "orders"
        st.rerun()

json_path_inventory = Path("inventory.json")
if json_path_inventory.exists():
    with open(json_path_inventory, "r") as f:
        inventory = json.load(f)

json_path_orders = Path("orders.json")
if json_path_orders.exists():
    with open(json_path_orders, "r") as f:
        orders = json.load(f)
else:
    orders = []

if st.session_state["page"] == "home":
    st.markdown("# Orders Management Application = Home Page")
    col1, col2 = st.columns([4,2])
    with col1:
        selected_category = st.radio("Select a List", ["Inventory", "Orders"], horizontal=True)
        if selected_category == "Inventory":
            if len(inventory) > 0:
                st.dataframe(inventory)
            else:
                st.warning("No item in the inventory")
        else:
            if len(orders) > 0:
                st.dataframe(orders)
            else:
                st.warning("No order is recorded yet")
    with col2:
        if selected_category == "Inventory":
            st.metric("Total Inventory", f"{len(inventory)}")
        else:
            st.metric("Total Orders", f"{len(orders)}")


elif st.session_state["page"] == "orders":
    st.markdown("Under Development....")