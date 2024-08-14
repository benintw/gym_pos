"""Fitopia class definition"""

import streamlit as st
import pandas as pd
from fitopia.member import Member


class Fitopia:
    def __init__(self):
        self.members = []
        self.update_members_in_session()

    def update_members_in_session(self):
        members_data = Member.get_all_members()
        self.members = members_data
        st.session_state.members = members_data

    def add_new_member(self, member_details):

        existing_member = self.get_member_by_contact(member_details["contact_num"])
        if existing_member:
            st.error(
                f"A member with contact number {member_details['contact_num']} already exists."
            )
            return

        member = Member.add_member(
            member_details["name"],
            member_details["contact_num"],
            member_details["email"],
            member_details["membership_type"],
            member_details["membership_duration"],
            member_details.get("photo"),
        )
        self.members.append(member)
        self.update_members_in_session()

    def list_members(self):
        members_data = Member.get_all_members()

        # Convert the data to a DataFrame
        members_df = pd.DataFrame(
            members_data,
            columns=[
                "Member ID",
                "Name",
                "Contact Number",
                "Email",
                "Membership Type",
                "Membership Duration",
                "Current Balance",
                "Photo",
                "Creation DateTime",  # Add the creation datetime to the DataFrame
            ],
        )

        # Drop the "Photo" column from the DataFrame
        members_df = members_df.drop(columns=["Photo"])

        return members_data, members_df

    def update_member_balance(self, contact_num, amount):
        Member.update_member_balance(contact_num, amount)
        self.update_members_in_session()

    def get_member_by_contact(self, contact_num):

        for member in st.session_state.members:
            if member[2] == contact_num:
                return member

    def show_members(self) -> None:
        """
        This method lists all members in the system.
        """
        members_data, _ = self.list_members()
        for member_data in members_data:
            (
                member_id,
                name,
                contact_num,
                email,
                membership_type,
                membership_duration,
                current_balance,
                photo,
                creation_datetime,
            ) = member_data

            member = Member(
                member_id=member_id,
                name=name,
                contact_num=contact_num,
                email=email,
                membership_type=membership_type,
                membership_duration=membership_duration,
                photo=photo,
                creation_datetime=creation_datetime,
            )

            member.current_balance = current_balance

            with st.container():
                cols = st.columns([1, 3])  # Adjust the column width ratios as needed
                if member.photo:
                    cols[0].image(
                        member.photo,
                        caption=f"Member ID: {member.member_id}",
                        use_column_width=True,
                    )
                else:
                    cols[0].text("No Photo Provided")

                # Display member info
                cols[1].markdown(
                    f"""
                    **Member ID:** {member.member_id}

                    **Name:** {member.name}

                    **Contact Number:** {member.contact_num}

                    **Email:** {member.email}

                    **Membership Type:** {member.membership_type}

                    **Membership Duration:** {member.membership_duration}

                    **Creation DateTime:** {member.creation_datetime}

                    **Current Balance:** ${member.current_balance}
                    """
                )
                st.text("-" * 20)


# Dialog function to add a new member
@st.dialog("新增會員", width="large")
def add_member_dialog():
    name = st.text_input("姓名")

    # contact_num input with validation
    contact_num = st.text_input("聯絡號碼 (例如: 0933-333-333)")

    if contact_num:
        existing_number = st.session_state.fitopia.get_member_by_contact(contact_num)
        if existing_number:
            st.warning("這個號碼已存在")
            return

    email = st.text_input("Email")
    membership_type = st.selectbox("會員資格", ["Pay-as-you-go", "Monthly", "Yearly"])

    membership_duration = "Forever"  # Default for Pay-as-you-go
    if membership_type in ["Monthly", "Yearly"]:
        duration_from = st.date_input("Duration FROM")
        duration_ends = st.date_input("Duration ENDS")
        if duration_from and duration_ends:
            membership_duration = f"{duration_from} to {duration_ends}"

    photo = st.file_uploader("上傳照片", type=["png", "jpg", "jpeg"])

    if st.button("Submit"):
        if name and contact_num and email and membership_type:
            # Convert the uploaded photo to binary
            photo_binary = None
            if photo is not None:
                photo_binary = photo.read()

            member_details = {
                "name": name,
                "contact_num": contact_num,
                "email": email,
                "membership_type": membership_type,
                "membership_duration": membership_duration,
                "photo": photo_binary,
            }
            st.session_state.fitopia.add_new_member(member_details)
            st.success(f"成功新增 {name} 為會員")
            st.rerun()  # Close the dialog after submission
