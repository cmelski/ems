from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class LoginPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.login_button = page.get_by_role("button", name="Login")
        self.email_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.error_container = page.locator('#toasts')

    def login(self, user_email, user_password):
        self.email_input.fill(user_email)
        self.password_input.fill(user_password)
        self.login_button.click()

