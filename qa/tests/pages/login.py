from qa.tests.pages.base import BasePage


class LoginPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.login_button = page.get_by_role("button", name="Login")
        self.email_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.error_container = page.locator('#toasts')
        self.page_text = page.locator('.auth-sub')
        self.page_body = page.locator('body')

    def enter_username(self, username: str):
        self.email_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

