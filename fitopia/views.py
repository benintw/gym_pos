# Streamlit functions for UI (e.g., edit_member_basic_info, view_member_details)
import streamlit as st
from fitopia.fitopia import Fitopia
from fitopia.member import Member


def edit_member_basic_info():
    """
    A function to edit the basic info of an existing member.
    """
    with st.expander("Edit Member Info"):
        contact_num = st.text_input("Enter Contact Number of Member to Edit")
        if contact_num:  # Only process if the contact number is entered
            member = Fitopia().get_member_by_contact(contact_num)
            if member:
                st.write("Editing Member:", member[1])
                new_name = st.text_input("New Name", value=member[1])
                new_contact_num = st.text_input("New Contact Number", value=member[2])
                new_email = st.text_input("New Email", value=member[3])
                new_membership_type = st.selectbox("New Membership Type", ["Pay-as-you-go", "Monthly", "Yearly"], index=["Pay-as-you-go", "Monthly", "Yearly"].index(member[4]))

                # Handle membership duration
                new_membership_duration = member[6]  # Keep the existing duration
                if new_membership_type != "Pay-as-you-go":
                    new_membership_duration = st.text_input("New Membership Duration", value=member[6], placeholder="YYYY-MM-DD to YYYY-MM-DD")

                new_photo = st.file_uploader("Upload New Photo", type=["png", "jpg", "jpeg"])

                # Update the member with edited data
                if st.button("Save Changes"):
                    Member.update_member(contact_num, new_name, new_contact_num, new_email, new_membership_duration, new_photo)
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
            member = Fitopia().get_member_by_contact(contact_num)
            if member:
                st.write(f"Current Balance: ${member[7]}")
                amount_to_add = st.number_input("Enter amount to add", min_value=0)

                if st.button("Add Balance"):
                    Fitopia().update_member_balance(contact_num, amount_to_add)
                    st.success(
                        f"${amount_to_add} added. New Balance: ${member[7] + amount_to_add}"
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
            member = Fitopia().get_member_by_contact(contact_num)
            if member:
                st.write(f"**Member ID:** {member[0]}")
                st.write(f"**Name:** {member[1]}")
                st.write(f"**Contact Number:** {member[2]}")
                st.write(f"**Email:** {member[3]}")
                st.write(f"**Membership Type:** {member[4]}")
                st.write(f"**Membership Duration:** {member[6]}")
                st.write(f"**Current Balance:** ${member[7]}")
                if member[8]:
                    st.image(member[8], caption="Member Photo", use_column_width=True)
            else:
                st.error(f"No member found with Contact Number {contact_num}")
