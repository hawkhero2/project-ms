from sqlite.database import DatabaseManageer

# db = DatabaseManageer("users.db")
# db.connect()

with DatabaseManageer("users.db") as db:
    db.delete_table("users")