import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

# Adding_New_Product.py

inventory = []

json_path_inventory = Path("inventory.json")

if json_path_inventory.exists():
    with json_path_inventory.open("r", encoding= "utf-8") as f:
        inventory = json.load(f)

st.header("Add New Product")
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

