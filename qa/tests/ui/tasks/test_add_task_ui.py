from playwright.sync_api import Page, expect
from qa.tests.actions.task_actions import TaskActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_task_ui
def test_add_task_ui(reset_db, task_data, page_instance: Page):
    new_task_info = []
    data = task_data['new_task']
    task_actions = TaskActions(page_instance)
    task_name = data['task_name']
    task_category = data['task_category']
    task_due_date = data['task_due_date']
    task_priority = data['task_priority']
    task_assignee_id = data['task_assignee_id']
    task_assignee_name = data['task_assignee_name']
    task_added_confirmation = data['expected_confirmation']
    new_task_info.extend([task_name, task_category, task_due_date, task_priority, task_assignee_id, task_assignee_name])
    logger_utility().info(f'Task details: {task_data}')
    # wait for init() to complete by checking state.contacts is populated
    page_instance.wait_for_function("() => state.contacts && state.contacts.length > 0")
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    # call add task function
    task_actions.add_task(task_name, task_category, task_due_date, task_priority, task_assignee_id)
    # verify confirmation message
    expect(task_actions.task_page.message_container).to_contain_text(task_added_confirmation)
    logger_utility().info(f'"{task_added_confirmation}" confirmation shown')
    # verify it exists in the UI table
    tasks_table = task_actions.task_page.task_table
    new_task_exists_in_ui_table = task_actions.base_page.verify_new_item_in_table(tasks_table, new_task_info, 'task')
    assert len(new_task_exists_in_ui_table) > 1, f'New task {new_task_info} not found in the UI tasks table'
    logger_utility().info('Navigate to Dashboard panel...')
    task_actions.dashboard_actions.navigate_to_panel('Dashboard')
    # verify activity log for the addition
    assert task_actions.dashboard_actions.dashboard_page.find_activity_log(new_task_exists_in_ui_table, 'added', 'task')
    # verify initial status is 'pending' by getting new task from DB
    status = task_actions.validate_task_status(new_task_exists_in_ui_table[0])
    assert status == 'pending'
    logger_utility().info(f'Initial status is {status}')
