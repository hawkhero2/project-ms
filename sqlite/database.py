import sqlite3

class DatabaseManageer():

    def __init__(self):
        """Initialize the database connection"""

        # path = "sqlite\\"+db_name
        self.db_name = "sqlite\\users.db" # For the moment I hardcoded the db, ya I know
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to database"""

        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Disconnect from database"""

        if self.conn:
            self.cursor.close()
            self.conn.close()

    def add_user(self, username, first_name, last_name, email):
        """Add user to database in users table"""

        if(username != "" and first_name != "" and last_name != "" and email !=""):
            self.cursor.execute(f"")
            self.conn.commit()

    def create_table(self):
        """Create table in database users.db"""
        # I hardcoded the table name aswell
        if not self.conn:
            raise Exception("Database connection is not established")

        query = f"""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL)"""

        self.cursor.execute(query)
        self.conn.commit()

    def fetch_all_users(self):
        """Fetches all users from the table users"""

        self.cursor.execute(f"SELECT * FROM users")
        users_list = self.cursor.fetchall()
        return users_list

    def delete_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        
    def __enter__(self):
        """Ensure the use of the with statement"""

        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
