# Fitopia class definition

import streamlit as st
import pandas as pd
from fitopia.member import Member


class Fitopia:
    def __init__(self):
        self.members = []

    def add_new_member(self, member_details):
        member = Member.add_member(
            member_details["name"],
            member_details["contact_num"],
            member_details["email"],
            member_details["membership_type"],
            member_details["membership_duration"],
            member_details.get("photo")
        )
        self.members.append(member)
    
    def list_members(self):
        members_data = Member.get_all_members()
        
        # Convert the data to a DataFrame
        members_df = pd.DataFrame(members_data, columns=[
            "Member ID", "Name", "Contact Number", "Email",
            "Membership Type", "Membership Duration", "Current Balance", "Photo"
        ])
        
        return members_data, members_df
    
    def update_member_balance(self, contact_num, amount):
        Member.update_member_balance(contact_num, amount)
    
    def get_member_by_contact(self, contact_num):
        return Member.get_member_by_contact(contact_num)

    def show_members(self) -> None:
        """
        This method lists all members in the system.
        """
        members_data, _ = self.list_members()
        for member_data in members_data:
            member_id, name, contact_num, email, membership_type, membership_duration, current_balance, photo = member_data
            
            member = Member(
                member_id=member_id,
                name=name,
                contact_num=contact_num,
                email=email,
                membership_type=membership_type,
                membership_duration=membership_duration,
                photo=photo
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

                    {"**Current Balance:** $" + str(member.current_balance)}
                    """
                )
                st.text("-" * 20)
