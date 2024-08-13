# Fitopia class definition

import streamlit as st
import pandas as pd
from fitopia.member import Member


class Fitopia:
    def __init__(self):
        self.members = []
        self.initialize_default_members()

    def initialize_default_members(self) -> None:
        member_a_details = {
            "name": "Jack Ma",
            "contact_num": "0930-144-111",
            "email": "abcd@gmail.com",
            "membership_type": "Pay-as-you-go",
            "photo": "memberA.jpg",
        }
        member_a = Member(member_id=1, **member_a_details)
        self.add_member(member_a)

        member_b_details = {
            "name": "Samuel Cho",
            "contact_num": "0930-333-222",
            "email": "lklklk@gmail.com",
            "membership_type": "Pay-as-you-go",
            "photo": "memberB.png",
        }
        member_b = Member(member_id=2, **member_b_details)
        self.add_member(member_b)

    def add_member(self, member: Member) -> None:
        self.members.append(member)

    def add_new_member(self, member_details: dict) -> Member:
        member = Member.create_membership(member_details, len(self.members) + 1)
        self.add_member(member)
        return member

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {k: v for k, v in member.to_dict().items() if k != "Photo"}
                for member in self.members
            ]
        )

    def get_member_by_contact_number(self, contact_num) -> Member:
        for member in self.members:
            if member.contact_num == contact_num:
                return member
        return None

    def list_members(self) -> pd.DataFrame:
        return self.to_dataframe()

    def show_members(self) -> None:
        """
        This method lists all members in the system.
        """
        for member in self.members:
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

                    {"**Current Balance:** $" + str(member.current_balance) if member.membership_type == "Pay-as-you-go" else ""}
                    """
                )
                st.text("-" * 20)
