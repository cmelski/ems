

from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.tasks import TasksPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_task_ui
def test_add_task_ui(reset_db, page_instance: Page, get_new_task_data: dict):
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Tasks')
    task_panel = TasksPage(page_instance)
    # convert data to list
    task_to_add_list = [v for v in get_new_task_data.values()]
    # call add task function
    task_panel.click_add_task(task_to_add_list)
    # verify it exists in the UI table
    new_task_exists = task_panel.verify_new_task_in_task_table(task_to_add_list)
    assert len(new_task_exists) > 1, f'New task {get_new_task_data} not found in the UI tasks table'
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the addition
    assert dashboard_page.find_activity_log(new_task_exists, 'added', 'task')
