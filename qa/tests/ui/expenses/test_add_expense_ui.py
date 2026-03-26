

from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.expense import ExpensePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_expense_ui
def test_add_expense_ui(reset_db, page_instance: Page, get_new_expense_data: dict):
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Expenses')
    expense_panel = ExpensePage(page_instance)
    # convert data to list
    expense_to_add_list = [v for v in get_new_expense_data.values()]
    # call add task function
    expense_panel.click_add_expense(expense_to_add_list)
    formatted_amount = f"${float(expense_to_add_list[1]):,.2f}"
    expense_to_add_list[1] = formatted_amount
    expense_to_add_list_formatted = [item.lower() if isinstance(item, str) else item for item in expense_to_add_list]
    # verify it exists in the UI table
    new_expense_exists = expense_panel.verify_new_expense_in_expense_table(expense_to_add_list_formatted)
    assert len(new_expense_exists) > 1, f'New expense {get_new_expense_data} not found in the UI expenses table'
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the addition
    assert dashboard_page.find_activity_log(new_expense_exists, 'added', 'expense')
