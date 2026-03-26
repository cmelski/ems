from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect

from qa.pages.expense import ExpensePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.expense_form_input
def test_add_expense_form_validation(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Expenses')
    expense_panel = ExpensePage(page_instance)
    expense_panel.fill_expense_form_invalid()
    expect(expense_panel.error_container).to_be_visible()
    expect(expense_panel.error_container).to_have_text('Please enter a description.')
    logger_utility().info(f'Error popup: "{expense_panel.error_container.inner_text()}" correctly displayed')
