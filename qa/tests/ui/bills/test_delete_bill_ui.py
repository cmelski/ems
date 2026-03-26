
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.bill import BillPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_bill_ui
def test_delete_bill_ui(reset_db, add_bill_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Bills panel')
    dashboard_page.click_sidebar_menu('Bills')
    bill_panel = BillPage(page_instance)
    # find row to delete
    bill_row = bill_panel.find_bill_row_to_action(add_bill_via_api)
    bill_panel.delete_bill(bill_row)
    # verify confirmation popup
    expect(bill_panel.error_container).to_contain_text('Bill removed')
    # verify task no longer exists in the UI table
    deleted = bill_panel.verify_bill_not_in_bill_table(add_bill_via_api)
    assert deleted is True, f'Bill {add_bill_via_api} still exists in the UI bills table'
    logger_utility().info(f'Bill {add_bill_via_api} not found in the UI bills table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_bill_via_api, 'deleted', 'bill')
