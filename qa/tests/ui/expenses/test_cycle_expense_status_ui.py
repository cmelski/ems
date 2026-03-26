
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.expense import ExpensePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.cycle_expense_status_ui
def test_cycle_expense_status_ui(reset_db, add_expense_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Expenses panel')
    dashboard_page.click_sidebar_menu('Expenses')
    expense_panel = ExpensePage(page_instance)
    # find row to delete
    expense_row = expense_panel.find_expense_row_to_action(add_expense_via_api)
    old_status = expense_panel.find_expense_table_cell_value(expense_row, 'STATUS')
    logger_utility().info(f'Old status: {old_status}')
    logger_utility().info('Click cycle status...')
    expense_panel.cycle_expense_status(expense_row)
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_expense_via_api, 'status updated',
                                            entity_text='expense')
    logger_utility().info('Navigate back to Expenses panel...')
    dashboard_page.click_sidebar_menu('Expenses')
    new_status = expense_panel.find_expense_table_cell_value(expense_row, 'STATUS')
    logger_utility().info(f'New status: {new_status}')
    assert old_status != new_status




