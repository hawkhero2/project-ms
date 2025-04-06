import sqlite3

class DatabaseManageer():

    def __init__(self):
        """Initialize the database connection"""

        # path = "sqlite\\"+db_name
        self.db_name = "sqlite\\users.db" # TODO For the moment I hardcoded the db, ya I know
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

    def update_user(self,
                    ldap_username=None,
                    ldap_fullname=None,
                    ldap_email=None,
                    rocket_username=None,
                    rocket_fullname=None,
                    win_username=None,
                    win_fullname=None):
        """Updates users info in database based on the params which are not empty\n
        TODO Not ideal but will suffice for the moment. Will improve later"""
        
        if(ldap_username != ""):
            if(ldap_email != ""):
                self.cursor.execute(f"""UPDATE users
                                    SET ldap_fn = \'{ldap_fullname}\'
                                    WHERE ldap_usr = \'{ldap_username}\';""")
                self.conn.commit()

            if(ldap_fullname != ""):
                self.cursor.execute(f"""UPDATE users
                                    SET ldap_fn =\'{ldap_fullname}\'
                                    WHERE ldap_usr = \'{ldap_username}\';""")
                self.conn.commit()
            
        if(rocket_username != ""):
            if(rocket_fullname != ""):
                self.cursor.execute(f"""UPDATE users
                                    SET rc_fn = \'{rocket_fullname}\'
                                    WHERE rc_usr = \'{rocket_username}\';""")
                self.conn.commit()

        if(win_username != ""):
            if(win_fullname != ""):
                self.cursor.execute(f"""UPDATE users
                                    SET win_fn = \'{win_fullname}\'
                                    WHERE win_usr = \'{win_username};""")
                self.conn.commit()
            

    def add_user(self,
                 ldap_username=None,
                 ldap_fullname=None,
                 ldap_email=None,
                 rocket_username=None,
                 rocket_fullname=None,
                 rocket_email=None,
                 win_username=None,
                 win_fullname=None):
        """Add user to database in users table based on the params which are not empty\n
        I know, this is not the best way to handle it.\n
        TODO It will do for the moment ... will improve later
        """

        if(ldap_username != ""):
            if(ldap_fullname != ""):
                self.cursor.execute(f"""INSERT INTO users (ldap_usr, ldap_fn, ldap_email)
                                    VALUES(?, ?, ?)
                                    ON CONFLICT ({win_username})
                                    DO NOTHING;""",(ldap_username, ldap_fullname, ldap_email))
                self.conn.commit()

        if(rocket_username != ""):
            if(rocket_fullname != "" and rocket_email != ""):
                self.cursor.execute(f"""INSERT INTO users (rc_usr, rc_fn, rc_email)
                                    VALUES(?, ?, ?)
                                    ON CONFLICT ({win_username})
                                    DO NOTHING;""",(rocket_username,rocket_fullname,rocket_email))
            self.conn.commit()

        if(win_username != ""):
            if(win_fullname != ""):
                self.cursor.execute(f"""INSERT INTO users (win_usr, win_fn)
                                    VALUES(?, ?)
                                    ON CONFLICT ({win_username})
                                    DO NOTHING;""", (win_username,win_fullname))
                self.conn.commit()


    def create_table(self):
        """Create table in database users.db"""
        # I hardcoded the table name aswell
        if not self.conn:
            raise Exception("Database connection is not established")

        query = f"""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ldap_usr TEXT,
        ldap_fn TEXT,
        ldap_email TEXT,
        rc_usr TEXT,
        rc_fn TEXT,
        rc_email TEXT,
        win_usr TEXT,
        win_fn TEXT,
        date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
        date_modified DATETIME DEFAULT CURRENT_TIMESTAMP)"""

        create_trigger_query = f"""
        CREATE TRIGGER IF NOT EXISTS update_date_modified
        AFTER UPDATE ON users
        FOR EACH ROW
        BEGIN
            UPDATE users
            SET date_modified = CURRENT_TIMESTAMP
            WHERE ID = OLD.id;
        END
        """

        self.cursor.execute(query)
        self.cursor.execute(create_trigger_query)
        self.conn.commit()

    def fetch_all_users(self):
        """Fetches all users from the table users"""

        self.cursor.execute(f"SELECT * FROM users")
        users_list = self.cursor.fetchall()
        return users_list

    def delete_table(self, table_name):
        """Deletes table if it exists"""
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        
    def __enter__(self):
        """Ensure the use of the with statement"""

        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
