from paramiko import SSHClient
from sqlite.database import DatabaseManager
from lib.globals_vars import ENV

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

    def update_user_db(self, user, fullname="",email=""):
        """Updates the user info stored in the Database"""

        with DatabaseManager() as db:
            db.update_user(user=user,
                           fullname=fullname,
                           email = email)

    def update_user(self, user, fullname = "", email = ""):# TODO Needs testing
        """Updates existing user's fullname / mail on LDAP server"""

        file = f"""cat << EOF > /tmp/u_usr.ldif\ndn: uid={user},cn=users,dc={self.env.dc1},dc={self.env.dc2}\nchangetype: modify\n"""

        if(self.env.env == "DEV"):
            cmd = f"ldapmodify -x -c -V -H ldaps://{self.env.ssh_host} -D \"uid={self.env.ldap_acc},cn=users,dc={self.env.dc1},dc={self.env.dc2}\" -w \"{self.env.ldap_pw}\" -f /tmp/u_usr.ldif"
            if fullname:
                file += f"""replace: gecos\ngecos: {fullname}\n-\n"""

            if email:
                file += f"""replace: mail\nmail: {email}\n-\n"""
            
            self.ssh.exec_command(file)
            self.ssh.exec_command(cmd)

        if(self.env.env == "PROD"):
            cmd = f"ldapmodify -x -c -V -H ldaps://{self.env.ssh_host} -D \"uid={self.env.ldap_acc},cn=users,dc={self.env.dc1},dc={self.env.dc2}\" -w \"{self.env.ldap_pw}\" -f /tmp/u_usr.ldif"
            if fullname:
                file += f"""replace: gecos\ngecos: {fullname}\n-\n"""

            if email:
                file += f"""replace: mail\nmail: {email}\n-\n"""
            
            self.ssh.exec_command(file)
            self.ssh.exec_command(cmd)

    def add_user_db(self, user, email = "", fullname = ""):
        """Updates user into the database"""

        with DatabaseManager() as db:
            db.add_user(ldap_username=user,
                        ldap_fullname=fullname,
                        ldap_email=email)

    def get_uid(self) -> int:
        """Grabs all the uids an returns the last uid, return 0 if none is found."""

        uid = "0"
        cmd = ""

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
                print(f"Failed: {e}\n{_stderr.read().decode()}") # TODO Write proper try-catching

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
                print(f"Failed: {e}\n{_stderr.read().decode()}") # TODO Write proper try-catching

        return int(uid)

    def get_users(self) -> list: 
        """Grabs all users from the LDAP server and returns list of users dict"""

        objectClass = "objectclass=posixAccount"
        users = []
        cmd = ""

        if(self.env.env == "DEV"): # This is for my own convenience so I dont change some values
            try:
                cmd = f"ldapsearch -D \"uid={self.env.ldap_acc},cn=users,dc={self.env.dc1},dc={self.env.dc2}\" -w \"{self.env.ldap_pw}\" -b dc={self.env.dc1},dc={self.env.dc2} \"({objectClass})\""
                _stdin, _stdout, _stderr = self.ssh.exec_command(cmd)
                users_entries = _stdout.read().decode().split("\n\n")

                # TODO Will improve later, maybe extract into a func
                for entry in users_entries:
                    user = {}
                    for item in entry.split("\n"):
                        if ((not item.startswith("#")) and (not item.startswith("dn")) and (not item.startswith("search:")) and (not item.startswith("result:"))):
                            if item.startswith("uid:"):
                                print(f"Printing from inside the cn condition :{item} \n")
                                user["username"] = item.split(":")[1].strip()

                            if item.startswith("gecos:"):
                                print(f"Printing from inside the gecos condition :{item}\n")
                                user["fullname"] = item.split(":")[1].strip()

                            if item.startswith("mail:"):
                                print(f"Printing from inside the mail condition :{item} \n")
                                user["email"] = item.split(":")[1].strip()
                    if user:
                        users.append(user) 
                        print(user)

            except Exception as e: # TODO Write proper try-catching
                print(e) 

        if(self.env.env == "PROD"):
            try:
                # In production you want to have TLS enforced
                cmd = f"ldapsearch -ZZ -D \"uid={self.env.ldap_acc},cn=users,dc={self.env.dc1},dc={self.env.dc2}\" -w \"{self.env.ldap_pw}\" -b dc={self.env.dc1},dc={self.env.dc2} \"({objectClass})\""
                _stdin, _stdout, _stderr = self.ssh.exec_command(cmd)
                users_entries = _stdout.read().decode().split("\n\n")

                # TODO Will improve later, maybe extract into a func
                for entry in users_entries:
                    user = {}
                    for item in entry.split("\n"):
                        if ((not item.startswith("#")) and (not item.startswith("dn")) and (not item.startswith("search:")) and (not item.startswith("result:"))):
                            if item.startswith("uid:"):
                                print(f"Printing from inside the cn condition :{item} \n")
                                user["username"] = item.split(":")[1].strip()

                            if item.startswith("gecos:"):
                                print(f"Printing from inside the gecos condition :{item}\n")
                                user["fullname"] = item.split(":")[1].strip()

                            if item.startswith("mail:"):
                                print(f"Printing from inside the mail condition :{item} \n")
                                user["email"] = item.split(":")[1].strip()
                    if user:
                        users.append(user) 
                        print(user)
            
            except Exception as e: # TODO Write proper try-catching
                print(e)
        
        return users

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()