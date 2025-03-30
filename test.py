from lib.rocket_sv import RocketChatSV
from sqlite.database import DatabaseManageer
from lib.win_sv import WinServer


with WinServer() as win:
    win.get_users()
