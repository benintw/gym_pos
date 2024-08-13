# Member class definition


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
