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

    # # Show members
    # if st.button("List Members"):
    #     st.header("Current Members")
    #     _, members_df = st.session_state.fitopia.list_members()
    #     st.dataframe(members_df)

    # if st.button("Show Member Details"):
    #     st.session_state.fitopia.show_members()

    # Create tabs for "List Members" and "Show Member Details"
    tabs = st.tabs(["場內會員", "List Members", "Show Member Details"])

    with tabs[0]:
        st.markdown("### 這邊會顯示目前場內會員資訊")
        st.write("=" * 30 )
        st.markdown("#### 誰誰誰A在場內 - 入場時間 - 持續時間")
        st.markdown("#### 誰誰誰B在場內 - 入場時間 - 持續時間")
        st.write("="* 30 )
    with tabs[1]:
        st.header("All Members")
        _, members_df = st.session_state.fitopia.list_members()
        st.dataframe(members_df)

    with tabs[2]:
        st.header("All Members")
        st.session_state.fitopia.show_members()


    # New input
    st.sidebar.header("Add New Member")
    name = st.sidebar.text_input("Name")
    contact_num = st.sidebar.text_input("Contact Number")
    email = st.sidebar.text_input("Email")
    membership_type = st.sidebar.selectbox(
        "Membership Type", ["Pay-as-you-go", "Monthly", "Yearly"]
    )
    
    membership_duration = "Forever"  # Default for Pay-as-you-go
    # Show duration inputs only for Monthly or Yearly memberships
    if membership_type in ["Monthly", "Yearly"]:
        duration_from = st.sidebar.date_input("Duration FROM")
        duration_ends = st.sidebar.date_input("Duration ENDS")
        if duration_from and duration_ends:
            membership_duration = f"{duration_from} to {duration_ends}"
            
    photo = st.sidebar.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])

    # Add member
    if st.sidebar.button("Add Member"):
        if name and contact_num and email and membership_type:
            member_details = {
                "name": name,
                "contact_num": contact_num,
                "email": email,
                "membership_type": membership_type,
                "membership_duration": membership_duration,
                "photo": photo,
            }
            st.session_state.fitopia.add_new_member(member_details)
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

if __name__ == "__main__":
    main()
