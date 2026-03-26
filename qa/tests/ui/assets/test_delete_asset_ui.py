
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.asset import AssetPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_asset_ui
def test_delete_asset_ui(reset_db, add_asset_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Assets panel')
    dashboard_page.click_sidebar_menu('Assets')
    asset_panel = AssetPage(page_instance)
    # find row to delete
    asset_row = asset_panel.find_asset_row_to_action(add_asset_via_api)
    asset_panel.delete_asset(asset_row)
    # verify confirmation popup
    expect(asset_panel.error_container).to_contain_text('Asset removed')
    # verify task no longer exists in the UI table
    deleted = asset_panel.verify_asset_not_in_asset_table(add_asset_via_api)
    assert deleted is True, f'Asset {add_asset_via_api} still exists in the UI assets table'
    logger_utility().info(f'Asset {add_asset_via_api} not found in the UI assets table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_asset_via_api, 'deleted', 'asset')
