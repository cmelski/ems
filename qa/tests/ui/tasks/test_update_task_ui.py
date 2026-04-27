
from playwright.sync_api import Page, expect
from qa.tests.actions.task_actions import TaskActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.update_task_ui
def test_update_task_ui(reset_db, add_task_via_db, get_updated_task_data, page_instance):
    task_actions = TaskActions(page_instance)
    logger_utility().info('Navigate to Tasks panel')
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    # find row to update
    task_table = task_actions.task_page.task_table
    task_row = task_actions.base_page.find_row_to_action(task_table, add_task_via_db, 'task')
    logger_utility().info('Row found')
    category = get_updated_task_data['category']
    due_date = get_updated_task_data['due_date']
    priority = get_updated_task_data['priority']
    assignee = get_updated_task_data['assignee_id']
    logger_utility().info(f'Updating task - {category}, {due_date}, {priority}, {assignee}')
    task_actions.update_task(task_row, category, due_date, priority, assignee)
    expect(task_actions.task_page.message_container).to_contain_text('Task updated')
    logger_utility().info(f'{task_actions.task_page.message_container.inner_text()} correctly displayed')

