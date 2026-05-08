from qa.tests.pages.login import LoginPage
from qa.tests.pages.dashboard import DashboardPage
from qa.tests.pages.register import RegisterPage


class AuthActions:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.register_page = RegisterPage(page)

    def login(self, username: str, password: str):
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()

    def register(self, first_name: str, last_name: str, email: str, password: str):
        self.register_page.enter_first_name(first_name)
        self.register_page.enter_last_name(last_name)
        self.register_page.enter_email(email)
        self.register_page.enter_password(password)
        self.register_page.click_register()

