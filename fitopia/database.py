import sqlite3
from datetime import datetime
import pytz


def get_connection():
    conn = sqlite3.connect("gym_membership.db")
    return conn


def create_members_table():
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
        creation_datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

    # Insert default members
    insert_default_members()


def insert_default_members():
    conn = get_connection()
    cursor = conn.cursor()

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

    for member in default_members:
        cursor.execute("SELECT * FROM members WHERE contact_num = ?", (member[1],))
        if not cursor.fetchone():
            cursor.execute(insert_member_query, member)

    conn.commit()
    conn.close()


def create_inventory_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER NOT NULL,
        last_maintenance_date DATE,
        status TEXT CHECK(status IN ('available', 'in maintenance', 'out of order')) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def create_gym_visits_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS gym_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        entry_time DATETIME NOT NULL,
        exit_time DATETIME,
        duration_minutes INTEGER,
        FOREIGN KEY (member_id) REFERENCES members(id)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def create_all_tables():
    create_members_table()
    create_inventory_table()
    create_gym_visits_table()


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


def record_entry(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    local_timezone = pytz.timezone("Asia/Taipei")
    entry_time = datetime.now(local_timezone)

    insert_query = """
    INSERT INTO gym_visits (member_id, entry_time)
    VALUES (?, ?)
    """
    cursor.execute(insert_query, (member_id, entry_time))
    conn.commit()
    conn.close()


def record_exit(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    local_timezone = pytz.timezone("Asia/Taipei")
    exit_time = datetime.now(local_timezone)

    cursor.execute(
        "SELECT id, entry_time FROM gym_visits WHERE member_id = ? AND exit_time IS NULL",
        (member_id,),
    )
    visit = cursor.fetchone()

    if visit:
        visit_id, entry_time = visit
        duration_minutes = (
            exit_time - datetime.fromisoformat(entry_time)
        ).seconds // 60

        update_query = """
        UPDATE gym_visits
        SET exit_time = ?, duration_minutes = ?
        WHERE id = ?
        """
        cursor.execute(update_query, (exit_time, duration_minutes, visit_id))

        cursor.execute(
            "SELECT membership_type, current_balance FROM members WHERE id = ?",
            (member_id,),
        )
        membership_type, current_balance = cursor.fetchone()

        if membership_type == "Pay-as-you-go" and current_balance is not None:
            new_balance = max(0, current_balance - duration_minutes)
            cursor.execute(
                "UPDATE members SET current_balance = ? WHERE id = ?",
                (new_balance, member_id),
            )

        conn.commit()

    conn.close()


# Initialize all tables when the module is imported
create_all_tables()
