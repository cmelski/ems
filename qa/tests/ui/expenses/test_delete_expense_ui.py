
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.expense import ExpensePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_expense_ui
def test_delete_expense_ui(reset_db, add_expense_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Expenses panel')
    dashboard_page.click_sidebar_menu('Expenses')
    expense_panel = ExpensePage(page_instance)
    # find row to delete
    expense_row = expense_panel.find_expense_row_to_action(add_expense_via_api)
    expense_panel.delete_expense(expense_row)
    # verify confirmation popup
    expect(expense_panel.error_container).to_contain_text('Expense removed')
    # verify task no longer exists in the UI table
    deleted = expense_panel.verify_expense_not_in_expense_table(add_expense_via_api)
    assert deleted is True, f'Expense {add_expense_via_api} still exists in the UI expenses table'
    logger_utility().info(f'Expense {add_expense_via_api} not found in the UI expenses table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_expense_via_api, 'deleted', 'expense')
