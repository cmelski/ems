from qa.tests.pages.base import BasePage


class RegisterPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.register_button = page.get_by_role("button", name="Register")
        self.fname_input = page.locator('input[name="first-name"]')
        self.lname_input = page.locator('input[name="last-name"]')
        self.email_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.error_container = page.locator('#toasts')
        self.page_title = page.locator('.auth-title')
        self.page_body = page.locator('body')

    def enter_first_name(self, first_name: str):
        self.fname_input.fill(first_name)

    def enter_last_name(self, last_name: str):
        self.lname_input.fill(last_name)

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_register(self):
        self.register_button.click()

