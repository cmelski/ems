from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect

from qa.pages.asset import AssetPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.asset_form_input
def test_add_asset_form_validation(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Assets')
    asset_panel = AssetPage(page_instance)
    asset_panel.fill_asset_form_invalid()
    expect(asset_panel.error_container).to_be_visible()
    expect(asset_panel.error_container).to_have_text('Please enter an asset name.')
    logger_utility().info(f'Error popup: "{asset_panel.error_container.inner_text()}" correctly displayed')
