import sqlite3

class DatabaseManager():

    def __init__(self):
        """Initialize the database connection"""

        # path = "sqlite\\"+db_name
        self.db_name = "sqlite\\database.db" # TODO For the moment I hardcoded the db, ya I know
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
                self.cursor.execute(f"""UPDATE ldap_users
                                    SET ldap_fn = \'{ldap_fullname}\'
                                    WHERE ldap_usr = \'{ldap_username}\';""")
                self.conn.commit()
                

            if(ldap_fullname != ""):
                self.cursor.execute(f"""UPDATE ldap_users
                                    SET ldap_fn =\'{ldap_fullname}\'
                                    WHERE ldap_usr = \'{ldap_username}\';""")
                self.conn.commit()
            
        if(rocket_username != ""):
            if(rocket_fullname != ""): # TODO Need to update email address aswell, because you need unique email address when creating a user
                self.cursor.execute(f"""UPDATE rocket_users
                                    SET rc_fn = \'{rocket_fullname}\'
                                    WHERE rc_usr = \'{rocket_username}\';""")
                self.conn.commit()

        if(win_username != ""):
            if(win_fullname != ""):
                self.cursor.execute(f"""UPDATE win_users
                                    SET win_fn = \'{win_fullname}\'
                                    WHERE win_usr = \'{win_username};""")
                self.conn.commit()
            
    def get_users(self)->list: # TODO refactor to work with new database
        """Grabs all users from database"""

        query = f"""
        SELECT
          'ldap' AS source_table,
          ldap_usr,
          ldap_fn AS full_name,
          ldap_email AS email,
          date_added,
          date_modified
        FROM ldap_users
        WHERE ldap_usr = ?

        UNION ALL

        SELECT
          'rocket' AS source_table,
          rc_usr,
          rc_fn AS full_name,
          rc_email AS email,
          date_added,
          date_modified
        FROM rocket_users
        WHERE rc_usr = ?

        UNION ALL

        SELECT
          'win' AS source_table,
          win_usr,
          win_fn AS full_name,
          NULL AS email,
          date_added,
          date_modified
        FROM win_users
        WHERE win_usr = ?;
        """

        self.cursor.execute(query)
        users = []
        for row in self.cursor:
            user = {
                "id":row[0],
                "ldap_usr":row[1],
                "ldap_fn":row[2],
                "ldap_email":row[3],
                "rc_usr":row[4],
                "rc_fn":row[5],
                "rc_email":row[6],
                "win_usr":row[7],
                "win_fn":row[8],
                "date_added":row[9],
                "date_modified":row[10]
                }
            users.append(user)

        return users

    def add_user(self,
                 ldap_usr=None,
                 ldap_fn=None,
                 ldap_email=None,
                 rc_usr=None,
                 rc_fn=None,
                 rc_email=None,
                 win_usr=None,
                 win_fn=None): 
        """
        Add user to database in users table based on the params which are not empty\n
        I know, this is not the best way to handle it.\n
        TODO It will do for the moment ... will improve later
        """

        if(ldap_usr != None):
            if(ldap_usr !=None and ldap_email != None):
                self.cursor.execute(f"""INSERT INTO ldap_users (ldap_usr, ldap_fn, ldap_email)
                                    VALUES(?, ?, ?);""",(ldap_usr, ldap_fn, ldap_email))
                self.conn.commit()

        if(rc_usr != None):
            if(rc_fn!= None and rc_email != None):
                self.cursor.execute(f"""INSERT INTO users (rc_usr, rc_fn, rc_email)
                                    VALUES(?, ?, ?);""",(rc_usr, rc_fn, rc_email))
                self.conn.commit()

        if(win_usr != None):
            if(win_fn != None):
                self.cursor.execute(f"""INSERT INTO users (win_usr, win_fn)
                                    VALUES(?, ?);""", (win_usr, win_fn))
                self.conn.commit()


    def create_table(self):
        """Create table in database users.db"""
        # I hardcoded the table name aswell
        if not self.conn:
            raise Exception("Database connection is not established")


        create_ldap_table_query = """
        CREATE TABLE IF NOT EXISTS ldap_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ldap_usr TEXT,
            ldap_fn TEXT,
            ldap_email TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_modified DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_ldap_trigger_query = """
        CREATE TRIGGER IF NOT EXISTS update_ldap_date_modified
        AFTER UPDATE ON ldap_users
        FOR EACH ROW
        BEGIN
            UPDATE ldap_users
            SET date_modified = CURRENT_TIMESTAMP
            WHERE ID = OLD.id;
        END
        """

        create_rocket_table_query = """
        CREATE TABLE IF NOT EXISTS rocket_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rc_usr TEXT,
            rc_fn TEXT,
            rc_email TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_modified DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_rocket_trigger_query = """
        CREATE TRIGGER IF NOT EXISTS update_rocket_date_modified
        AFTER UPDATE ON rocket_users
        FOR EACH ROW
        BEGIN
            UPDATE rocket_users
            SET date_modified = CURRENT_TIMESTAMP
            WHERE ID = OLD.id;
        END
        """

        create_win_table_query = """
        CREATE TABLE IF NOT EXISTS win_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            win_usr TEXT,
            win_fn TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_modified DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """

        create_win_trigger_query = """
        CREATE TRIGGER IF NOT EXISTS update_win_date_modified
        AFTER UPDATE ON win_users
        FOR EACH ROW
        BEGIN
            UPDATE win_users
            SET date_modified = CURRENT_TIMESTAMP
            WHERE ID = OLD.id;
        END
        """

        self.cursor.execute(create_ldap_table_query)
        self.cursor.execute(create_rocket_table_query)
        self.cursor.execute(create_win_table_query)
        self.cursor.execute(create_ldap_trigger_query)
        self.cursor.execute(create_rocket_trigger_query)
        self.cursor.execute(create_win_trigger_query)
        self.conn.commit()

        query = f"""CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        initialized BOOLEAN CHECK (initialized IN (0,1)))"""

        self.cursor.execute(query)
        self.conn.commit()

    def empty_users_table(self):
        """
        Empties the users table so we can work with an empty canvas.\n
        Will probably use it mostly in dev
        """
        self.cursor.execute(f"DELETE FROM users;") # No error handling atm
        self.conn.commit()

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
