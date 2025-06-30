from textual.containers import VerticalScroll
from textual.widgets import Static
from lib.ldap_sv import LdapServer
from lib.win_sv import WinServer
from lib.rocket_sv import RocketChatSV
from sqlite.database import DatabaseManager

class Userslist(VerticalScroll):
    users = [
        ]

    def compose(self):
        with DatabaseManager() as db:
            while(self.number_users > 0):
                yield Static(f"user{self.number_users}")
                self.number_users = self.number_users-1
