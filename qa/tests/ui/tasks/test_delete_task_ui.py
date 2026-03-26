
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.tasks import TasksPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_task_ui
def test_delete_task_ui(reset_db, add_task_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Tasks panel')
    dashboard_page.click_sidebar_menu('Tasks')
    task_panel = TasksPage(page_instance)
    # find row to delete
    task_row = task_panel.find_task_row_to_action(add_task_via_api)
    task_panel.delete_task(task_row)
    # verify confirmation popup
    expect(task_panel.error_container).to_contain_text('Task removed')
    # verify task no longer exists in the UI table
    deleted = task_panel.verify_task_not_in_task_table(add_task_via_api)
    assert deleted is True, f'Task {add_task_via_api} still exists in the UI tasks table'
    logger_utility().info(f'Task {add_task_via_api} not found in the UI tasks table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_task_via_api, 'deleted', 'task')
