"""Main streamlit app"""

import streamlit as st
from fitopia.fitopia import Fitopia, add_member_dialog
from fitopia.views import (
    edit_member_basic_info_dialog,
    add_member_balance_dialog,
    view_member_details_dialog,
)

from fitopia.inventory_management import inventory_management


def main():
    st.title("Welcome to FITOPIA")

    # Initialize Fitopia and member ID counter in session state if they don't exist
    if "fitopia" not in st.session_state:
        st.session_state.fitopia = Fitopia()

    ## SIDE BAR
    menu = ["會員管理", "庫存管理"]
    choice = st.sidebar.selectbox("選單", menu)

    if choice == "會員管理":

        ### Membership Management
        tabs = st.tabs(["場內會員", "會員清單", "Show Member Details"])

        with tabs[0]:
            st.markdown("### 這邊會顯示目前場內會員資訊")
            st.write("=" * 30)
            st.markdown("#### 誰誰誰A在場內 - 入場時間 - 持續時間")
            st.markdown("#### 誰誰誰B在場內 - 入場時間 - 持續時間")
            st.write("=" * 30)

        with tabs[1]:
            st.header("All Members")
            _, members_df = st.session_state.fitopia.list_members()
            st.dataframe(members_df)

        with tabs[2]:
            st.header("All Members")
            st.session_state.fitopia.show_members()

        # Sidebar buttons to open the dialogs

        # Button to open the dialog for adding a new member
        if st.sidebar.button("Add New Member"):
            add_member_dialog()

        if st.sidebar.button("Edit Member Info"):
            edit_member_basic_info_dialog()

        if st.sidebar.button("Add Member Balance"):
            add_member_balance_dialog()

        if st.sidebar.button("View Member Details"):
            view_member_details_dialog()

    elif choice == "庫存管理":
        inventory_management()


if __name__ == "__main__":
    main()
