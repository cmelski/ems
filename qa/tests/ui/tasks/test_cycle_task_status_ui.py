
from qa.tests.actions.task_actions import TaskActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.cycle_task_status_ui
def test_cycle_task_status_ui(reset_db, add_task_via_db: tuple, page_instance):
    task_actions = TaskActions(page_instance)
    logger_utility().info('Navigate to Tasks panel')
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    # find row to delete
    task_table = task_actions.task_page.task_table
    task_row = task_actions.base_page.find_row_to_action(task_table, add_task_via_db, 'task')
    old_status = task_actions.base_page.find_table_cell_value(task_table, task_row, 'STATUS')
    logger_utility().info(f'Old status: {old_status}')
    logger_utility().info('Click cycle status...')
    task_actions.cycle_task_status(task_row)
    logger_utility().info('Navigate to Dashboard panel...')
    task_actions.dashboard_actions.navigate_to_panel('Dashboard')
    # verify activity log for the deletion
    assert task_actions.dashboard_actions.dashboard_page.find_activity_log(add_task_via_db, 'status updated',
                                            entity_text='task')
    logger_utility().info('Navigate back to Tasks panel...')
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    new_status = task_actions.base_page.find_table_cell_value(task_table, task_row, 'STATUS')
    logger_utility().info(f'New status: {new_status}')
    assert old_status != new_status




