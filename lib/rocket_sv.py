from rocketchat_API.rocketchat import RocketChat
from lib.globals_vars import LOGFILE, LOGS_FORMAT, ENV
from sqlite.database import DatabaseManageer
import logging

class RocketChatSV():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)
        self.env = ENV()
        self.rocketAPI = None

    def connect(self):
        """Connect to the RocketChat API"""
        try:
            self.rocketAPI = RocketChat(user=self.env.rocket_acc, password=self.env.rocket_pw, server_url=self.env.rocket_url)
            return self.rocketAPI
        except Exception as e:
            self.logger.error(f"Error attempting to connect to RocketChatSV : {self.env.rocket_url}")
            raise ValueError("Failed to connect to RocketChat API") from e

    def update_db(users: list):
        """
        Updates the user info in database based on the list of dicts received
        """

        username = users["username"]
        name = users["name"]
        email = users["email"]

        with DatabaseManageer() as db:
            db.update_user(rocket_username=username,
                           rocket_fullname=name,
                           email=email)
        pass

    def update_user(self, username, fullname=None, passw=None, email=None):
        """
        Updates the user info on the server
        Cannot receive empty username
        """
        # TODO Finish update users func

        if(fullname != ""):
            self.rocketAPI.users_update()
            pass

        if(passw != ""):
            pass

        if(email != ""):
            pass

        pass

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
            # print(users)
            for itm in users:
                if "emails" in itm.keys():
                    user_info["id"] = itm["_id"]
                    user_info["username"] = itm["username"]
                    user_info["name"] = itm["name"]
                    user_info["email"] = itm["emails"][0]["address"]
                    users_list.append(user_info)
                    user_info = {}
        else:
            self.logger.error(f"Error fetching users {response}")
        return users_list

    def __enter__(self):
        """Ensures the connection inside the with statement"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
