from globals_vars import LOGS_FORMAT,LOGFILE, ENV
from paramiko import SSHClient
from dotenv import dotenv_values
import logging
import os


class WinServer():

    script_path = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_path,"..",".env")
    config = dotenv_values(env_path)

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=LOGFILE,format=LOGS_FORMAT,level=logging.INFO)

    logger.info(f"Running : {__name__}")
    env = ENV()

    def update_user_info(self, username, fullname, passw):
        """
        Updates the user's info on Windows Server platform

        @fullname: Full name of the user
        @password: Password of the user

        """

        ssh = SSHClient()
        ssh.load_system_host_keys()

        try:
            ssh.connect(hostname=self.env.win_ssh_host, 
                        username=self.env.win_ssh_user, 
                        password=self.env.win_ssh_pw)
            self.logger.info(f"SSH sucessfully into : {self.env.win_ssh_host}")

            try:
                _stdin, _stdout, _stderr = ssh.exec_command(f"powershell net user {username} \"/fullname:{fullname}\"")
                self.logger.info(f"Updated fullname {fullname} for user : {username}")
            except:
                pass
        
        except:
            self.logger.log(f"Error attempting ssh.connect(): hostname {self.env.win_ssh_host}")
        pass

    def get_user_info(self, username, fullname, passw):
        pass