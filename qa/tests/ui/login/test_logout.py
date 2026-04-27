from playwright.sync_api import Page
from qa.tests.pages.dashboard import DashboardPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.logout
def test_logout(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.logout()
    assert 'login' in page_instance.url
    logger_utility().info('Logged out successfully')