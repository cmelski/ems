from playwright.sync_api import Page, expect
from qa.tests.actions.auth_actions import AuthActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.register
def test_register(page_instance_login_tests: Page, get_new_user_data) -> None:
    auth = AuthActions(page_instance_login_tests)
    auth.login_page.navigate_to_register()
    first_name = get_new_user_data['first_name']
    last_name = get_new_user_data['last_name']
    email = get_new_user_data['email']
    password = get_new_user_data['password']

    auth.register(first_name, last_name, email, password)

    page_body = auth.register_page.page_body
    expect(page_body).to_contain_text('Registration request successfully sent')
    logger_utility().info(f"'Registration request successfully sent' confirmation is displayed")


