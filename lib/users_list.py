from textual.containers import VerticalScroll
from textual.widgets import Static
from lib.ldap_sv import LdapServer
from lib.win_sv import WinServer
from lib.rocket_sv import RocketChatSV
from sqlite.database import DatabaseManager

class Userslist(VerticalScroll):
    
    number_users = 50
    with DatabaseManager() as db:
        db.create_table()

    def compose(self):
        while(self.number_users > 0):
            yield Static(f"user{self.number_users}")
            self.number_users=self.number_users-1
