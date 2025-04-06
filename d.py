from textual.app import App, ComposeResult
from textual.widgets import Welcome, Static, Header, Footer
from lib.users_list import Userslist

class App5(App):

    CSS_PATH = "styles\\d_layout.tcss"

    def compose(self) -> ComposeResult:
        # yield Placeholder()
        yield Header()
        yield Userslist()
        # yield Static("One", classes="box", id="two")
        # yield Static("User Info", classes="box")
        # yield RocketChatSV("User Info Rocket",classes="box")
        yield Static("Account Info", classes="box")
        yield Footer()

    def on_button_pressed(self) -> None:
        pass

    # def on_mount(self) -> None:
    #     self.theme = "tokyo-night"

if __name__ == "__main__":
    app = App5()
    app.run()