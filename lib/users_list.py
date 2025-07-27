from textual.containers import VerticalScroll
from textual.widgets import Static
from lib import RocketChatSV, LdapServer, WinServer, User
from sqlite.database import DatabaseManager

class Userslist(VerticalScroll):
    users = [
        ]

    def compose(self):
        with DatabaseManager() as db:
            while(self.number_users > 0):
                yield Static(f"user{self.number_users}")
                self.number_users = self.number_users-1
