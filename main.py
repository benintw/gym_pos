import streamlit as st
import pandas as pd


# Define the Member class
class Member:
    def __init__(
        self,
        member_id: int,
        name: str,
        contact_num: str,
        email: str,
        membership_type: str,
        photo=None,
    ):
        self.member_id = member_id
        self.name = name
        self.contact_num = contact_num
        self.email = email
        self.membership_type = membership_type
        self.photo = photo

        # Initialize balance if membership_type is "Pay-as-you-go"
        if membership_type == "Pay-as-you-go":
            self.current_balance = 0
        else:
            self.current_balance = None

    def to_dict(self):
        return {
            "Member ID": self.member_id,
            "Name": self.name,
            "Contact Number": self.contact_num,
            "Email": self.email,
            "Membership Type": self.membership_type,
            "Current Balance": self.current_balance,
            "Photo": self.photo,
        }

    @classmethod
    def create_membership(cls, member_details: dict, member_id: int):
        """
        This is a class method. The user can use this to create an instance of Member.
        """
        return cls(
            member_id=member_id,
            name=member_details["name"],
            contact_num=member_details["contact_num"],
            email=member_details["email"],
            membership_type=member_details["membership_type"],
            photo=member_details.get("photo"),
        )

    def __str__(self):
        """
        This method returns a string representation of the Member object.
        """
        return (
            f"Member ID: {self.member_id}\n"
            f"Name: {self.name}\n"
            f"Contact Number: {self.contact_num}\n"
            f"Email: {self.email}\n"
            f"Membership Type: {self.membership_type}\n"
            f"Current Balance: {self.current_balance if self.current_balance is not None else 'N/A'}\n"
            f"Photo: {self.photo if self.photo else 'Not Provided'}"
        )


# Define the Fitopia class
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

        member_a = Member.create_membership(member_a_details, 1)
        self.add_member(member_a)

        member_b_details = {
            "name": "Samuel Cho",
            "contact_num": "0930-333-222",
            "email": "lklklk@gmail.com",
            "membership_type": "Pay-as-you-go",
            "photo": "memberB.png",
        }
        member_b = Member.create_membership(member_b_details, 2)
        self.add_member(member_b)

    def add_member(self, member: Member) -> None:
        self.members.append(member)

    @property
    def num_members(self) -> int:
        return len(self.members)

    def get_member_by_contact_number(self, contact_num) -> Member:
        for member in self.members:
            if member.contact_num == contact_num:
                return member
        return None

    def list_members(self) -> None:
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


def edit_member_basic_info():
    """
    A function to edit the basic info of an existing member.

    Basic info includes only: name, contact_num, email, photo
    """
    with st.expander("Edit Member Info"):
        contact_num = st.text_input("Enter Contact Number of Member to Edit")
        if contact_num:  # Only process if the contact number is entered
            member = st.session_state.fitopia.get_member_by_contact_number(contact_num)
            if member:
                st.write("Editing Member:", member.name)
                new_name = st.text_input("New Name", value=member.name)
                new_contact_num = st.text_input(
                    "New Contact Number", value=member.contact_num
                )
                new_email = st.text_input("New Email", value=member.email)
                new_photo = st.file_uploader(
                    "Upload New Photo", type=["png", "jpg", "jpeg"]
                )

                if st.button("Save Changes"):
                    member.name = new_name
                    member.contact_num = new_contact_num
                    member.email = new_email
                    member.photo = new_photo if new_photo else member.photo
                    st.success(f"Member {contact_num} info updated successfully!")
            else:
                st.error(f"No member found with Contact Number {contact_num}")


def add_member_balance():
    """
    This function edits the member's balance.

    member's can come to the staff and asks to deposit money to the balance.
    The gym charges $1 dolloar per minute.

    For example:
    Sam's current balance: $100. Sam deposits $500 to his account, so now he has $600 which is 600 minutes.

    This account balance can only be added, ie. a positive increment change.

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


# Main Streamlit app function
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
            new_member = Member.create_membership(
                member_details, st.session_state.member_id_counter
            )
            st.session_state.fitopia.add_member(new_member)
            st.session_state.member_id_counter += 1  # Increment the member ID counter
            st.sidebar.success(f"Member {name} added successfully!")
        else:
            st.sidebar.error("Please fill out all fields.")

    # Layout for editing member info and adding balance
    col1, col2 = st.columns(2)
    with col1:
        edit_member_basic_info()
    with col2:
        add_member_balance()

    # Show members
    if st.button("Show Members"):
        st.header("Current Members")
        st.session_state.fitopia.list_members()


if __name__ == "__main__":
    main()
