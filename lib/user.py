
class User():
    # Construct the class structure for one user.
    # Then consume it in the UI classes.
    ldap_usr = ""
    ldap_name = ""
    rocket_usr = ""
    rocket_name = ""
    win_usr = ""
    win_name = ""
    
    def __init__(self, ldap_user, ldap_name, rocket_user, rocket_name, win_user, win_name):
        self.ldap_usr = ldap_user
        self.ldap_name = ldap_name
        self.rocket_usr = rocket_user
        self.rocket_name = rocket_name
        self.win_usr = win_user
        self.win_name = win_name

    def __str__(self):
        print(f"ldap username: {self.ldap_usr}, ldap name: {self.ldap_name}, "+
              f"rocket user: {self.rocket_usr}, rocket name: {self.rocket_name},"+
              f" windows user: {self.win_usr}, windows name: {self.win_name}")