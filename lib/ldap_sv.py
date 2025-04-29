from paramiko import SSHClient
from lib.globals_vars import LOGFILE, LOGS_FORMAT, ENV
import logging


class LdapServer():
    """
    Class which manages the users on a LDAP
    Currently supports the following functionalities : 
    """

    def __init__(self):
        self.env = ENV()
        self.ssh = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    def disconnect(self):
        """Closes the connection with the target host"""
        if self.ssh:
            self.ssh.close()

    def connect(self):
        """Connects to the target host machine through SSH"""
        if self.ssh != None:
            self.ssh = SSHClient()
            self.ssh.load_system_host_keys()

    def update_user_info():
        pass

    def get_user_info():
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()