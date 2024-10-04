import sqlite3
import numpy as np

conn = sqlite3.connect('emails.db', check_same_thread=False)

cursor = conn.cursor()

def create():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_embeddings (
            sno INTEGER PRIMARY KEY AUTOINCREMENT,
            email_data TEXT NOT NULL
        )
    ''')

    conn.commit()

# Step 4: Function to insert email content and embeddings into the database
def insert_email_to_db(email_content):
    # Convert the embedding array to a binary format (BLOB)
    # embedding_blob = np.array(embedding).tobytes()

    if email_content=="" or email_content is None:
        print("Content is NULL")
        return False

    try:
        cursor.execute('''SELECT COUNT(*) FROM email_embeddings WHERE email_data = ?''', (email_content,))
        count = cursor.fetchone()[0]

        if count > 0:
            # If the email exists, return False
            print("Email already exists in the database.")
            return False
        cursor.execute('''INSERT INTO email_embeddings (email_data) VALUES (?)''', (email_content,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False


# Step 5: Function to retrieve email data and embeddings from the database
def retrieve_emails_from_db():
    cursor.execute('SELECT sno, email_data FROM email_embeddings')
    rows = cursor.fetchall()

    emails = []
    for row in rows:
        sno, email_content = row
        # Convert BLOB back to numpy array
        data = f"{sno}. {email_content}"
        emails.append(data)

    return emails

def clear_data():
    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='email_embeddings'")
    table_exists = cursor.fetchone() is not None  # Returns None if the table doesn't exist

    if table_exists:
        cursor.execute('DROP TABLE email_embeddings')
        conn.commit()



# Step 6: Close the database connection when done
def close_connection():
    cursor.close()
    conn.close()

# close_connection()
