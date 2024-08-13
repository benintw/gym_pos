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
        photo BLOB
    );
    """
    
    cursor.execute(create_table_query)

    # Insert default members
    default_members = [
        ("Jack Ma", "0930-144-111", "abcd@gmail.com", "Pay-as-you-go", "Forever", "memberA.jpg"),
        ("Samuel Cho", "0930-333-222", "lklklk@gmail.com", "Pay-as-you-go", "Forever", "memberB.png")
    ]

    insert_query = """
    INSERT INTO members (name, contact_num, email, membership_type, membership_duration, photo)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    # Only insert if not already in the database
    for member in default_members:
        cursor.execute("SELECT * FROM members WHERE contact_num = ?", (member[1],))
        if not cursor.fetchone():
            cursor.execute(insert_query, member)

    conn.commit()
    conn.close()

# Initialize the database when this module is imported
create_tables()
