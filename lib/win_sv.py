from lib.globals_vars import ENV, LOGFILE, LOGS_FORMAT
from sqlite.database import DatabaseManageer
from paramiko import SSHClient
import logging


class WinServer():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=LOGFILE, level=logging.INFO)
        self.env = ENV()
        self.ssh = None


    def get_usernames(self):
        """
        Runs a "net user" command and formats the output received from the Win Server\n
        This function is mostly needed further down the line in grabbing the full info about each individual username\n
        Returns a list containing all usernames on the Windows Server
        """
        
        _stdin,_stdout,_stderr = self.ssh.exec_command(f"net user")
        resp = _stdout.read().decode().splitlines(True)
        usrs = []
        iterator = 0
        for i in resp:
            if(iterator > 3 and iterator < len(resp)-2):
                for item in i.split():
                    usrs.append(item.split()[0])
                iterator = iterator+1
            else:
                iterator= iterator+1
        
        return usrs


    def get_users(self):
        """
        Goes through the list of usernames present on the Windows Server\n
        Grabs the Fullname and packages it into a dict and returns it\n
        Returns dict
        """
        users_info = {}
        for username in self.get_usernames():
            _stdin,_stdout,_stderr = self.ssh.exec_command(f"net user {username}")
            
            resp = _stdout.read().decode().splitlines()

            usr = resp[0].split()
            fullname = resp[1].split()

            if(len(fullname) > 2):
                fn = ""
                for i  in fullname[2:]:
                    fn = f"{fn} {i}"
                users_info[usr[2]] = fn
            else:
                users_info[usr[2]] = "No fullname"
            
        return users_info


    def connect(self):
        """
        Connects to the Windows Server via ssh
        """
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()

        try:
            self.ssh.connect(hostname=self.env.win_ssh_host,
                             username=self.env.win_ssh_user,
                             password=self.env.win_ssh_pw)
        except:
            self.logger.error(f"Error connecting to {self.env.win_ssh_host} via SSH")

        return self


    def update_db(self, username, fullname):
        """Updates the database info for the given user with given parameters"""

        if(username != "" and fullname != ""):
            with DatabaseManageer() as db:
                db.update_user(win_username=username, win_fullname=fullname)
        # TODO Learn to log errors using builtin log lib of Textual


    def update_user(self, username, fullname=None, passw=None):
        """
        Updates the user's info on Windows Server platform

        @fullname: Full name of the user
        @password: Password of the user

        """

        try:
            self.ssh.connect(hostname=self.env.win_ssh_host,
                        username=self.env.win_ssh_user,
                        password=self.env.win_ssh_pw)
            self.logger.info(f"SSH sucessfully into : {self.env.win_ssh_host}")

            if(fullname != ""):
                try:
                    _stdin, _stdout, _stderr = self.ssh.exec_command(f"powershell net user {username} /fullname:\"{fullname}\"")
                    self.logger.info(f"{_stdout}")
                except:
                    self.logger.info(f"{_stderr}")

            if(passw != ""):
                try:
                    _stdin, _stdout, _stderr = self.ssh.exec_command(f"powershell net user {username} {passw} /expires:never")
                    self.logger.info(f"{_stdout}")
                except:
                    self.logger.info(f"{_stderr}")

        
        except:
            self.logger.log(f"Error attempting ssh.connect(): hostname {self.env.win_ssh_host}")


    def __enter__(self):
        self.connect()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
