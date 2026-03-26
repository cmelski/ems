from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect

from qa.pages.bill import BillPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.bill_form_input
def test_add_bill_form_validation(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Bills')
    bill_panel = BillPage(page_instance)
    bill_panel.fill_bill_form_invalid()
    expect(bill_panel.error_container).to_be_visible()
    expect(bill_panel.error_container).to_have_text('Please enter a creditor/description.')
    logger_utility().info(f'Error popup: "{bill_panel.error_container.inner_text()}" correctly displayed')
