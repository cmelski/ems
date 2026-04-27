from playwright.sync_api import Page, expect
from qa.tests.actions.auth_actions import AuthActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.valid_login
def test_valid_login(page_instance_login_tests: Page, login_data) -> None:
    data = login_data["valid_login"]
    auth = AuthActions(page_instance_login_tests)

    auth.login(data["username"], data["password"])

    dashboard_title = auth.dashboard_page.page_title.inner_text()

    assert dashboard_title == data["expected_page_title"], \
        f"Expected page title '{data['expected_page_title']}'"
    logger_utility().info(f"Expected page title '{data['expected_page_title']}'")
    #expect(dashboard_page.page_title).to_be_visible(timeout=3000)

