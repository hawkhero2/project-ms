from rocketchat_API.rocketchat import RocketChat
from textual.app import ComposeResult
from textual.widgets import Static, Input
from lib.globals_vars import LOGFILE, LOGS_FORMAT, ENV
import logging

class RocketChatSV():

    env = ENV()
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    def connect_rocket(self, url, acc, pw):
        try:
            rocketAPI = RocketChat(user=acc, password=pw, url=url)
            return rocketAPI
        except Exception as e:
            self.logger.error(f"Error attempting to connect to RocketChatSV : {url}")
            return ""

    def update_user_info(self, username, fullname, passw, email):
        pass

    def get_user_info():
        pass
