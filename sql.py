import sqlite3
import numpy as np

conn = sqlite3.connect('emails.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_embeddings (
        sno INTEGER PRIMARY KEY AUTOINCREMENT,
        email_data TEXT NOT NULL,
        embedding BLOB NOT NULL
    )
''')

conn.commit()

# Step 4: Function to insert email content and embeddings into the database
def insert_email_to_db(email_content, embedding):
    # Convert the embedding array to a binary format (BLOB)
    embedding_blob = np.array(embedding).tobytes()

    # Insert email content and embedding into the database
    cursor.execute('''
        INSERT INTO email_embeddings (email_data, embedding)
        VALUES (?, ?)
    ''', (email_content, embedding_blob))

    # Commit the transaction
    conn.commit()

# Step 5: Function to retrieve email data and embeddings from the database
def retrieve_emails_from_db():
    cursor.execute('SELECT sno, email_data, embedding FROM email_embeddings')
    rows = cursor.fetchall()

    emails = []
    for row in rows:
        sno, email_content, embedding_blob = row
        # Convert BLOB back to numpy array
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        emails.append((sno, email_content, embedding))

    return emails

# Step 6: Close the database connection when done
def close_connection():
    cursor.close()
    conn.close()

close_connection()
