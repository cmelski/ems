
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.bill import BillPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.cycle_bill_status_ui
def test_cycle_bill_status_ui(reset_db, add_bill_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Bills panel')
    dashboard_page.click_sidebar_menu('Bills')
    bill_panel = BillPage(page_instance)
    # find row to delete
    bill_row = bill_panel.find_bill_row_to_action(add_bill_via_api)
    old_status = bill_panel.find_bill_table_cell_value(bill_row, 'STATUS')
    logger_utility().info(f'Old status: {old_status}')
    logger_utility().info('Click cycle status...')
    bill_panel.cycle_bill_status(bill_row)
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_bill_via_api, 'status updated',
                                            entity_text='bill')
    logger_utility().info('Navigate back to Bills panel...')
    dashboard_page.click_sidebar_menu('Bills')
    new_status = bill_panel.find_bill_table_cell_value(bill_row, 'STATUS')
    logger_utility().info(f'New status: {new_status}')
    assert old_status != new_status




