
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.asset import AssetPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.cycle_asset_status_ui
def test_cycle_asset_status_ui(reset_db, add_asset_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Assets panel')
    dashboard_page.click_sidebar_menu('Assets')
    asset_panel = AssetPage(page_instance)
    # find row to delete
    asset_row = asset_panel.find_asset_row_to_action(add_asset_via_api)
    old_status = asset_panel.find_asset_table_cell_value(asset_row, 'STATUS')
    logger_utility().info(f'Old status: {old_status}')
    logger_utility().info('Click cycle status...')
    asset_panel.cycle_asset_status(asset_row)
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_asset_via_api, 'status updated',
                                            entity_text='asset')
    logger_utility().info('Navigate back to Assets panel...')
    dashboard_page.click_sidebar_menu('Assets')
    new_status = asset_panel.find_asset_table_cell_value(asset_row, 'STATUS')
    logger_utility().info(f'New status: {new_status}')
    assert old_status != new_status




