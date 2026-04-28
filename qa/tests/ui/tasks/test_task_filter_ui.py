from qa.tests.actions.task_actions import TaskActions
from qa.utilities.logging_utils import logger_utility
import pytest

TASK_FILTER_DROPDOWN_VALUES = ['pending', 'in-progress', 'done', 'all']


@pytest.mark.flaky(reruns=3, delay=1)
@pytest.mark.parametrize('filter_dropdown', TASK_FILTER_DROPDOWN_VALUES,
                         ids=['filter_pending', 'filter_in-progress', 'filter_done', 'filter_all'])
@pytest.mark.task_filter_ui
def test_task_filter(reset_db, add_tasks_via_db, page_instance, filter_dropdown):
    task_actions = TaskActions(page_instance)
    if filter_dropdown == 'all':
        page_instance.wait_for_function("() => state.tasks && state.tasks.length > 0")
    logger_utility().info('Navigate to Tasks panel')
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    task_actions.filter_task(filter_dropdown)
    logger_utility().info(f'Filter selected: {page_instance.locator("#task-filter").input_value()}')
    task_table = task_actions.task_page.task_table
    task_table_ui_status_values = task_actions.base_page.find_table_cells_for_specific_column(task_table, 'STATUS')
    logger_utility().info(f'filter: "{filter_dropdown}" values: {task_table_ui_status_values}')
    if filter_dropdown == 'all':
        assert len(set(task_table_ui_status_values)) > 1
        logger_utility().info(f'filter: {filter_dropdown} displays all status values: {task_table_ui_status_values}')
    else:
        for value in task_table_ui_status_values:
            assert filter_dropdown == value.lower()
            logger_utility().info(
                f'filter: {filter_dropdown} displays only {filter_dropdown} values: {task_table_ui_status_values}')
