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

    def disconnect(self):
        """Closes the connection with the target host"""
        if self.ssh != None:
            self.ssh.close()

    def connect(self):
        """Connects to the target host machine through SSH"""
        if self.ssh == None:
            self.ssh = SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.connect(hostname=self.env.ssh_host,
                             username=self.env.ssh_user,
                             password=self.env.ssh_pw)

    def update_user_info():
        pass

    def get_user_info():
        pass

    def get_uid(self) -> int:
        """Grabs all the uids an returns the last uid, return 0 if none is found."""

        uid="0"
        cmd=""

        if (self.env.env == "PROD"):
            try:
                # For security the -ZZ paramenter is needed to establish a secure connection using StartTLS and require to succeed
                cmd = f"ldapsearch -ZZ -D \"uid={self.env.ldap_acc},cn=users,dc={self.env.dc1},dc={self.env.dc2}\" -w \"{self.env.ldap_pw}\" -b dc={self.env.dc1},dc={self.env.dc2} \"(uidNumber=*)\""
                print(f"Printing the command : {cmd}")
                _stdin, _stdout, _stderr = self.ssh.exec_command(cmd)

                resp = _stdout.read().decode().split("\n")
                for itm in resp:
                    if itm.__contains__("uidNumber"):
                        uid=itm.split(":")[1]
                
            except Exception as e:
                print(f"Failed: {e}\n{_stderr.read().decode()}")

        if (self.env.env == "DEV"):
            try:
                cmd = f"ldapsearch -ZZ -D \"uid={self.env.ldap_acc},cn=users,dc={self.env.dc1},dc={self.env.dc2}\" -w \"{self.env.ldap_pw}\" -b dc={self.env.dc1},dc={self.env.dc2} \"(uidNumber=*)\""
                print(f"Printing the command : {cmd}")

                _stdin, _stdout, _stderr = self.ssh.exec_command(cmd)

                print(f"Printing the stdin : {_stdin.read().decode()}")
                resp = _stdout.read().decode().split("\n")
                for itm in resp:
                    if itm.__contains__("uidNumber"):
                        uid=itm.split(":")[1]
                
                for line in resp:
                    print("Printing the _stdout")
                    print(f"{line}\n")
            
            except Exception as e:
                print(f"Failed: {e}\n{_stderr.read().decode()}")

        return int(uid)

    def get_all_users(self):
        """"""
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()