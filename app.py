from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Static, Input, Button, DataTable

class Sidebar(VerticalScroll):
    def compose(self):
        # Replace with your user list from DB
        users = ["alice", "bob", "carol"]
        for user in users:
            yield Button(user, id=f"user-{user}")

class UserDetails(Vertical):
    def compose(self):
        yield Static("Username:")
        yield Input(placeholder="Username", id="username")
        yield Static("Full Name:")
        yield Input(placeholder="Full Name", id="fullname")
        yield Static("Email:")
        yield Input(placeholder="Email", id="email")
        yield Static("Password:")
        yield Input(password=True, placeholder="Password", id="password")
        yield Button("Set Password", id="set-password")

class MiscInfo(Vertical):
    def compose(self):
        yield Static("Created: ...")
        yield Static("Last Modified: ...")
        yield Static("Disabled: ...")

class MainPanel(Vertical):
    def compose(self):
        yield UserDetails()
        yield MiscInfo()

class UserManagerApp(App):
    CSS_PATH = "styles/d_layout.tcss"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Sidebar(),
            MainPanel()
        )

if __name__ == "__main__":
    app = UserManagerApp()
    app.run()