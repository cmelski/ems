import os

from playwright.sync_api import Page, expect
from qa.pages.login import LoginPage
from qa.pages.dashboard import DashboardPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.valid_login
def test_valid_login(page_instance_login_tests: Page) -> None:
    login_page = LoginPage(page_instance_login_tests)
    login_page.login(os.environ.get('USER_EMAIL'), os.environ.get('USER_PASSWORD'))
    dashboard_page = DashboardPage(page_instance_login_tests)
    expect(dashboard_page.page_title).to_be_visible(timeout=3000)
    expect(dashboard_page.page_title).to_have_text('Dashboard')
