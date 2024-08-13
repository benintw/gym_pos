# Streamlit functions for UI (e.g., edit_member_basic_info, view_member_details)

import streamlit as st
import pandas as pd


def edit_member_basic_info():
    """
    A function to edit the basic info of an existing member.
    """
    with st.expander("Edit Member Info"):
        contact_num = st.text_input("Enter Contact Number of Member to Edit")
        if contact_num:  # Only process if the contact number is entered
            member = st.session_state.fitopia.get_member_by_contact_number(contact_num)
            if member:
                st.write("Editing Member:", member.name)

                # Use st.data_editor to edit the member's basic information
                member_df = pd.DataFrame([member.to_dict()])
                edited_member_df = st.data_editor(member_df, num_rows="fixed")

                # Update the member with edited data
                if st.button("Save Changes"):
                    edited_member_data = edited_member_df.iloc[0].to_dict()
                    member.name = edited_member_data["Name"]
                    member.contact_num = edited_member_data["Contact Number"]
                    member.email = edited_member_data["Email"]
                    member.photo = edited_member_data["Photo"]
                    st.success(f"Member {contact_num} info updated successfully!")
            else:
                st.error(f"No member found with Contact Number {contact_num}")


def add_member_balance():
    """
    This function edits the member's balance.
    """
    with st.expander("Add Member Balance"):
        contact_num = st.text_input("Enter Contact Number of Member to Add Balance")
        if contact_num:  # Only process if the contact number is entered
            member = st.session_state.fitopia.get_member_by_contact_number(contact_num)
            if member and member.membership_type == "Pay-as-you-go":
                st.write(f"Current Balance: ${member.current_balance}")
                amount_to_add = st.number_input("Enter amount to add", min_value=0)

                if st.button("Add Balance"):
                    member.current_balance += amount_to_add
                    st.success(
                        f"${amount_to_add} added. New Balance: ${member.current_balance}"
                    )
            elif member:
                st.error(
                    f"Member {member.name} does not have a Pay-as-you-go membership type."
                )
            else:
                st.error(f"No member found with Contact Number {contact_num}")


def view_member_details():
    """
    This function views the member's details, including their current balance if applicable.
    """
    with st.expander("View Member Details"):
        contact_num = st.text_input("Enter Contact Number of Member to View Details")
        if contact_num:  # Only process if the contact number is entered
            member = st.session_state.fitopia.get_member_by_contact_number(contact_num)
            if member:
                st.write(f"**Member ID:** {member.member_id}")
                st.write(f"**Name:** {member.name}")
                st.write(f"**Contact Number:** {member.contact_num}")
                st.write(f"**Email:** {member.email}")
                st.write(f"**Membership Type:** {member.membership_type}")
                if member.membership_type == "Pay-as-you-go":
                    st.write(f"**Current Balance:** ${member.current_balance}")
                if member.photo:
                    st.image(
                        member.photo, caption="Member Photo", use_column_width=True
                    )
            else:
                st.error(f"No member found with Contact Number {contact_num}")
