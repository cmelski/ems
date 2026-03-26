

from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.asset import AssetPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_asset_ui
def test_add_asset_ui(reset_db, page_instance: Page, get_new_asset_data: dict):
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Assets')
    asset_panel = AssetPage(page_instance)
    # convert data to list
    asset_to_add_list = [v for v in get_new_asset_data.values()]
    # call add task function
    asset_panel.click_add_asset(asset_to_add_list)
    formatted_value = f"${float(asset_to_add_list[2]):,.2f}"
    asset_to_add_list[2] = formatted_value
    asset_to_add_list_formatted = [item.lower() if isinstance(item, str) else item for item in asset_to_add_list]
    # verify it exists in the UI table
    new_asset_exists = asset_panel.verify_new_asset_in_asset_table(asset_to_add_list_formatted)
    assert len(new_asset_exists) > 1, f'New asset {get_new_asset_data} not found in the UI assets table'
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the addition
    assert dashboard_page.find_activity_log(new_asset_exists, 'added', 'asset')
