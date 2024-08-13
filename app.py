"""Main streamlit app"""

import streamlit as st
from fitopia.fitopia import Fitopia
from fitopia.views import (
    edit_member_basic_info,
    add_member_balance,
    view_member_details,
)


def main():
    st.title("Welcome to FITOPIA")

    # Initialize Fitopia and member ID counter in session state if they don't exist
    if "fitopia" not in st.session_state:
        st.session_state.fitopia = Fitopia()
        st.session_state.member_id_counter = 3

    # New input
    st.sidebar.header("Add New Member")
    name = st.sidebar.text_input("Name")
    contact_num = st.sidebar.text_input("Contact Number")
    email = st.sidebar.text_input("Email")
    membership_type = st.sidebar.selectbox(
        "Membership Type", ["Pay-as-you-go", "Monthly", "Yearly"]
    )
    photo = st.sidebar.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])

    # Add member
    if st.sidebar.button("Add Member"):
        if name and contact_num and email and membership_type:
            member_details = {
                "name": name,
                "contact_num": contact_num,
                "email": email,
                "membership_type": membership_type,
                "photo": photo,
            }
            new_member = st.session_state.fitopia.add_new_member(member_details)
            st.session_state.member_id_counter += 1  # Increment the member ID counter
            st.sidebar.success(f"Member {name} added successfully!")
        else:
            st.sidebar.error("Please fill out all fields.")

    # Layout for editing member info, viewing member details, and adding balance
    col1, col2, col3 = st.columns(3)
    with col1:
        edit_member_basic_info()
    with col2:
        add_member_balance()
    with col3:
        view_member_details()

    # Show members
    if st.toggle("List Members"):
        st.header("Current Members")
        members_df = st.session_state.fitopia.list_members()
        st.dataframe(members_df)

    if st.toggle("Show Member Details"):
        st.session_state.fitopia.show_members()


if __name__ == "__main__":
    main()
