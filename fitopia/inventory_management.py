"""Inventory Management """

import streamlit as st
from fitopia.database import (
    add_equipment,
    update_equipment_status,
    get_all_inventory,
    add_member,
)


def inventory_management():
    st.header("Inventory Management")

    action = st.radio(
        "Action", ["Add New Equipment", "Update Equipment Status", "View Inventory"]
    )

    if action == "Add New Equipment":
        equipment_name = st.text_input("Equipment Name")
        description = st.text_area("Description")
        quantity = st.number_input("Quantity", min_value=1)
        last_maintenance_date = st.date_input("Last Maintenance Date")
        status = st.selectbox("Status", ["available", "in maintenance", "out of order"])

        if st.button("Add Equipment"):
            add_equipment(
                equipment_name, description, quantity, last_maintenance_date, status
            )
            st.success(f"{equipment_name} added successfully!")

    elif action == "Update Equipment Status":
        equipment_id = st.number_input("Equipment ID", min_value=1)
        new_status = st.selectbox(
            "New Status", ["available", "in maintenance", "out of order"]
        )

        if st.button("Update Status"):
            update_equipment_status(equipment_id, new_status)
            st.success(f"Equipment ID {equipment_id} status updated to {new_status}!")

    elif action == "View Inventory":
        inventory_data = get_all_inventory()
        st.table(inventory_data)
