from dotenv import dotenv_values
from paramiko import SSHClient
from lib.globals_vars import LOGFILE, LOGS_FORMAT, ENV
import logging


class LdapServer():
    """
    
    """

    def __init__(self):
        self.env = ENV()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    def disconnect():
        pass

    def connect():
        pass

    def update_user_info():
        pass

    def get_user_info():
        pass