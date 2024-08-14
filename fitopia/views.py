""" Streamlit functions for UI (e.g., edit_member_basic_info, view_member_details)"""

import streamlit as st
from fitopia.fitopia import Fitopia
from fitopia.member import Member
import time


@st.dialog("Edit Member Info", width="large")
def edit_member_basic_info_dialog():
    """
    A function to edit the basic info of an existing member.
    """
    contact_num = st.text_input("Enter Contact Number of Member to Edit")
    if contact_num:  # Only process if the contact number is entered
        member = st.session_state.fitopia.get_member_by_contact(contact_num)
        if member:

            member_id = member[0]
            member_name = member[1]
            member_contact_num = member[2]
            member_email = member[3]
            member_type = member[4]
            member_duration = member[5]
            member_current_balance = member[6]
            member_photo = member[7]

            st.write("Editing Member:", member_name)
            new_name = st.text_input("New Name", value=member_name)
            new_contact_num = st.text_input(
                "New Contact Number", value=member_contact_num
            )
            new_email = st.text_input("New Email", value=member_email)
            new_membership_type = st.selectbox(
                "New Membership Type",
                ["Pay-as-you-go", "Monthly", "Yearly"],
                index=["Pay-as-you-go", "Monthly", "Yearly"].index(member_type),
            )

            # Handle membership duration
            new_membership_duration = member_duration  # Keep the existing duration
            if new_membership_type != "Pay-as-you-go":
                duration_from = st.date_input("Duration FROM")
                duration_ends = st.date_input("Duration ENDS")
                if duration_from and duration_ends:
                    new_membership_duration = f"{duration_from} to {duration_ends}"

            new_photo = st.file_uploader(
                "Upload New Photo", type=["png", "jpg", "jpeg"]
            )

            # Update the member with edited data
            if st.button("Save Changes"):
                Member.update_member(
                    contact_num,
                    new_name,
                    new_contact_num,
                    new_email,
                    new_membership_duration,
                    new_photo,
                )
                st.session_state.fitopia.update_members_in_session()
                st.success(f"Member {contact_num} info updated successfully!")
                st.rerun()
        else:
            st.error(f"No member found with Contact Number {contact_num}")


@st.dialog("Add Member Balance", width="large")
def add_member_balance_dialog():
    """
    This function edits the member's balance.
    """
    contact_num = st.text_input("輸入會員電話號碼")
    if contact_num:  # Only process if the contact number is entered
        member = st.session_state.fitopia.get_member_by_contact(contact_num)
        if member:

            member_id = member[0]
            member_name = member[1]
            member_contact_num = member[2]
            member_email = member[3]
            member_type = member[4]
            member_duration = member[5]
            member_current_balance = member[6]
            member_photo = member[7]

            st.write(f"會員: {member_name}")
            st.write(f"目前餘額: {member_current_balance} 分鐘")
            amount_to_add = st.number_input("輸入儲值分鐘", min_value=0)

            if st.button("確定儲值"):
                st.session_state.fitopia.update_member_balance(
                    contact_num, amount_to_add
                )
                st.success(f"已儲入 {amount_to_add} 分鐘.")
                st.success(f"最新剩餘分鐘: $ {member_current_balance + amount_to_add}")
                time.sleep(2)
                st.session_state.fitopia.update_members_in_session()
                st.rerun()

        else:
            st.error(f"No member found with Contact Number {contact_num}")


@st.dialog("View Member Details", width="large")
def view_member_details_dialog():
    """
    This function views the member's details, including their current balance if applicable.
    """
    contact_num = st.text_input("Enter Contact Number of Member to View Details")
    if contact_num:  # Only process if the contact number is entered
        member = Fitopia().get_member_by_contact(contact_num)
        if member:

            member_id = member[0]
            member_name = member[1]
            member_contact_num = member[2]
            member_email = member[3]
            member_type = member[4]
            member_duration = member[5]
            member_current_balance = member[6]
            member_photo = member[7]

            st.write(f"**Member ID:** {member_id}")
            st.write(f"**Name:** {member_name}")
            st.write(f"**Contact Number:** {member_contact_num}")
            st.write(f"**Email:** {member_email}")
            st.write(f"**Membership Type:** {member_type}")
            st.write(f"**Membership Duration:** {member_duration}")
            st.write(f"**Current Balance:** ${member_current_balance}")
            if member_photo is not None:
                st.image(member_photo, caption="Member Photo", use_column_width=True)
            else:
                st.write("會員尚未有照片")
        else:
            st.error(f"No member found with Contact Number {contact_num}")
