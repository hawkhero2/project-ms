from rocketchat_API.rocketchat import RocketChat
from lib.globals_vars import LOGFILE, LOGS_FORMAT, ENV
from sqlite.database import DatabaseManager

class RocketChatSV():

    def __init__(self):
        self.env = ENV()
        self.rocketAPI = None

    def connect(self):
        "Connect to the RocketChat API"
        try:
            self.rocketAPI = RocketChat(user=self.env.rocket_acc, 
                                        password=self.env.rocket_pw, 
                                        server_url=self.env.rocket_url)
            return self.rocketAPI
        except Exception as e:
            raise ValueError("Failed to connect to RocketChat API") from e

    def update_db(users: list):
        """
        Updates the user info in database based on the list of dicts received
        """

        username = users["username"]
        name = users["name"]
        email = users["email"]

        with DatabaseManager() as db:
            db.update_user(rocket_username=username,
                           rocket_fullname=name,
                           email=email)

    def get_user_id(self, username:str):
        """Returns the id of the given username"""

        id = None

        users = self.get_users()
        for usr in users:
            if usr["username"] == username:
                id = usr["id"]

        return id

    def update_user(self, username, fullname=None, passw=None, email=None):
        """
        Updates the user info on the server
        Cannot receive empty username
        """

        if(fullname != ""):
            resp = self.rocketAPI.users_update(user_id=self.get_user_id(username=username),
                                                name=fullname)

        if(passw != ""):
            resp = self.rocketAPI.users_update(user_id=self.get_user_id(username=username),
                                                password=passw)
        # TODO Finish update logic
        if(email != ""):
            resp = self.rocketAPI.users_update(user_id=self.get_user_id(username=username),
                                                emails=email)

    def get_users(self) -> list:
        """
        Returns a list with info about all users.

        These are the keys in the returned dict:
        
        username, emails, name
        """
        response = self.rocketAPI.users_list()
        users_list = []
        user_info = {}

        if response.ok:
            resp:dict = response.json()
            users = resp.get("users",[])

            for itm in users:
                if "emails" in itm.keys():
                    user_info["id"] = itm["_id"]
                    user_info["username"] = itm["username"]
                    user_info["name"] = itm["name"]
                    user_info["email"] = itm["emails"][0]["address"]
                    users_list.append(user_info)
                    user_info = {}
        else:
            print(f"Error : {response.content.decode()}") 
        return users_list

    def __enter__(self):
        """Ensures the connection inside the with statement"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
