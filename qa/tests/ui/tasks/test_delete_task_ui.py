
from playwright.sync_api import expect
from qa.tests.actions.task_actions import TaskActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_task_ui
def test_delete_task_ui(reset_db, add_task_via_db: tuple, page_instance):
    task_actions = TaskActions(page_instance)
    logger_utility().info('Navigate to Tasks panel')
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    # find row to delete
    task_table = task_actions.task_page.task_table
    task_row = task_actions.base_page.find_row_to_action(task_table, add_task_via_db, 'task')
    task_actions.delete_task(task_row)
    # verify confirmation popup
    expect(task_actions.task_page.message_container).to_contain_text('Task removed')
    # verify task no longer exists in the UI table
    deleted = task_actions.base_page.verify_item_not_in_table(add_task_via_db, task_table, 'task')
    assert deleted is True, f'Task {add_task_via_db} still exists in the UI tasks table'
    logger_utility().info(f'Task {add_task_via_db} not found in the UI tasks table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    task_actions.dashboard_actions.navigate_to_panel('Dashboard')
    # verify activity log for the deletion
    assert task_actions.dashboard_actions.dashboard_page.find_activity_log(add_task_via_db, 'deleted', 'task')
