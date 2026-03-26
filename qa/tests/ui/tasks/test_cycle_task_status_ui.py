
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.tasks import TasksPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.cycle_task_status_ui
def test_cycle_task_status_ui(reset_db, add_task_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Tasks panel')
    dashboard_page.click_sidebar_menu('Tasks')
    task_panel = TasksPage(page_instance)
    # find row to delete
    task_row = task_panel.find_task_row_to_action(add_task_via_api)
    old_status = task_panel.find_task_table_cell_value(task_row, 'STATUS')
    logger_utility().info(f'Old status: {old_status}')
    logger_utility().info('Click cycle status...')
    task_panel.cycle_task_status(task_row)
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_task_via_api, 'status updated',
                                            entity_text='task')
    logger_utility().info('Navigate back to Tasks panel...')
    dashboard_page.click_sidebar_menu('Tasks')
    new_status = task_panel.find_task_table_cell_value(task_row, 'STATUS')
    logger_utility().info(f'New status: {new_status}')
    assert old_status != new_status




