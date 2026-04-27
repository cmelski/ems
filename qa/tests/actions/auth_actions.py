from qa.tests.pages.login import LoginPage
from qa.tests.pages.dashboard import DashboardPage


class AuthActions:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)

    def login(self, username: str, password: str):
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()

