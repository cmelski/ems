

from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.bill import BillPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_bill_ui
def test_add_bill_ui(reset_db, page_instance: Page, get_new_bill_data: dict):
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Bills')
    bill_panel = BillPage(page_instance)
    # convert data to list
    bill_to_add_list = [v for v in get_new_bill_data.values()]
    # call add task function
    bill_panel.click_add_bill(bill_to_add_list)
    formatted_amount = f"${float(bill_to_add_list[1]):,.2f}"
    bill_to_add_list[1] = formatted_amount
    # verify it exists in the UI table
    new_bill_exists = bill_panel.verify_new_bill_in_bill_table(bill_to_add_list)
    assert len(new_bill_exists) > 1, f'New bill {get_new_bill_data} not found in the UI bills table'
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the addition
    assert dashboard_page.find_activity_log(new_bill_exists, 'added', 'bill')
