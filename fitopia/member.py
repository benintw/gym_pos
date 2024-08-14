""" Member class definition"""

from fitopia.database import get_connection
import sqlite3
from datetime import datetime
import pytz


class Member:
    def __init__(
        self,
        member_id: int,
        name: str,
        contact_num: str,
        email: str,
        membership_type: str,
        membership_duration: str,
        current_balance: int = 0,
        photo=None,
        creation_datetime=None,
    ):
        self.member_id = member_id
        self.name = name
        self.contact_num = contact_num
        self.email = email
        self.membership_type = membership_type
        self.membership_duration = membership_duration
        self.current_balance = current_balance
        self.photo = photo
        self.creation_datetime = creation_datetime

    @classmethod
    def add_member(
        cls, name, contact_num, email, membership_type, membership_duration, photo=None
    ):
        conn = get_connection()
        cursor = conn.cursor()

        current_balance = 0

        # Get the current time in the desired timezone
        local_timezone = pytz.timezone(
            "Asia/Taipei"
        )  # Change this to your local timezone
        creation_datetime = datetime.now(tz=local_timezone).strftime("%Y-%m-%d")

        insert_query = """
        INSERT INTO members (name, contact_num, email, membership_type, membership_duration, current_balance, photo, creation_datetime)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            insert_query,
            (
                name,
                contact_num,
                email,
                membership_type,
                membership_duration,
                current_balance,
                photo,
                creation_datetime,  # Insert the creation datetime
            ),
        )
        conn.commit()
        member_id = cursor.lastrowid
        conn.close()

        return cls(
            member_id,
            name,
            contact_num,
            email,
            membership_type,
            membership_duration,
            current_balance,
            photo,
            creation_datetime,  # Return the creation datetime
        )

    @classmethod
    def get_all_members(cls) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        conn.close()
        return members

    @classmethod
    def update_member_balance(cls, contact_num, amount_to_add) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        # Ensure that current_balance is not None
        cursor.execute(
            "SELECT current_balance FROM members WHERE contact_num = ?", (contact_num,)
        )
        current_balance = cursor.fetchone()[0]

        if current_balance is None:
            current_balance = 0  # Default to 0 if current_balance is None

        update_query = """
        UPDATE members
        SET current_balance = ?
        WHERE contact_num = ?
        """

        new_balance = current_balance + amount_to_add

        cursor.execute(update_query, (new_balance, contact_num))
        conn.commit()
        conn.close()

    @classmethod
    def get_member_by_contact(cls, contact_num):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE contact_num = ?", (contact_num,))

        member = cursor.fetchone()
        conn.close()
        return member

    @classmethod
    def update_member(
        cls,
        contact_num,
        name=None,
        new_contact_num=None,
        email=None,
        membership_duration=None,
        photo=None,
    ):
        conn = get_connection()
        cursor = conn.cursor()

        update_fields = []
        values = []

        if name:
            update_fields.append("name = ?")
            values.append(name)
        if new_contact_num:
            update_fields.append("contact_num = ?")
            values.append(new_contact_num)
        if email:
            update_fields.append("email = ?")
            values.append(email)
        if membership_duration:
            update_fields.append("membership_duration = ?")
            values.append(membership_duration)
        if photo:
            update_fields.append("photo = ?")
            values.append(photo)

        values.append(contact_num)

        update_query = f"""
        UPDATE members
        SET {", ".join(update_fields)}
        WHERE contact_num = ?
        """

        cursor.execute(update_query, values)
        conn.commit()
        conn.close()
