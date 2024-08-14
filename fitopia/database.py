"""database.py for database storage"""

import sqlite3


def get_connection():
    conn = sqlite3.connect("gym_membership.db")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_num TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        membership_type TEXT NOT NULL,
        membership_duration TEXT NOT NULL,
        current_balance INT DEFAULT 0,
        photo BLOB,
        creation_datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP -- Add this line to record the creation date and time
    );
    """

    cursor.execute(create_table_query)

    # Insert default members
    default_members = [
        (
            "Jack Ma",
            "0930-144-111",
            "abcd@gmail.com",
            "Pay-as-you-go",
            "Forever",
            "memberA.jpg",
        ),
        (
            "Samuel Cho",
            "0930-333-222",
            "lklklk@gmail.com",
            "Pay-as-you-go",
            "Forever",
            "memberB.png",
        ),
    ]

    insert_member_query = """
    INSERT INTO members (name, contact_num, email, membership_type, membership_duration, photo)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    # Only insert if not already in the database
    for member in default_members:
        cursor.execute("SELECT * FROM members WHERE contact_num = ?", (member[1],))
        if not cursor.fetchone():
            cursor.execute(insert_member_query, member)

    # Create table for inventory
    create_inventory_table_query = """
    CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER NOT NULL,
        last_maintenance_date DATE,
        status TEXT CHECK(status IN ('available', 'in maintenance', 'out of order')) NOT NULL
    );
    """

    cursor.execute(create_inventory_table_query)

    conn.commit()
    conn.close()


def add_member(
    name, contact_num, email, membership_type, membership_duration, photo=None
):
    conn = get_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO members (name, contact_num, email, membership_type, membership_duration, photo)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(
        insert_query,
        (name, contact_num, email, membership_type, membership_duration, photo),
    )
    conn.commit()
    conn.close()


def add_equipment(equipment_name, description, quantity, last_maintenance_date, status):
    conn = get_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO inventory (equipment_name, description, quantity, last_maintenance_date, status)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(
        insert_query,
        (equipment_name, description, quantity, last_maintenance_date, status),
    )
    conn.commit()
    conn.close()


def update_equipment_status(equipment_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    update_query = """
    UPDATE inventory
    SET status = ?
    WHERE id = ?
    """
    cursor.execute(update_query, (status, equipment_id))
    conn.commit()
    conn.close()


def get_all_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    conn.close()
    return inventory


# Initialize the database when this module is imported
create_tables()
