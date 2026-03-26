from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.tasks import TasksPage, TASK_FILTER_DROPDOWN_VALUES
from qa.utilities.logging_utils import logger_utility
import pytest

@pytest.mark.flaky(reruns=3, delay=1)
@pytest.mark.parametrize('filter_dropdown', TASK_FILTER_DROPDOWN_VALUES,
                         ids=['filter_pending', 'filter_in-progress', 'filter_done', 'filter_all'])
@pytest.mark.task_filter_ui
def test_task_filter(reset_db, add_tasks_via_api, page_instance, filter_dropdown):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Tasks panel')
    dashboard_page.click_sidebar_menu('Tasks')
    task_panel = TasksPage(page_instance)
    task_panel.select_task_filter(filter_dropdown)
    logger_utility().info(f'Filter selected: {page_instance.locator("#task-filter").input_value()}')
    task_table_ui_status_values = task_panel.find_table_cells_for_specific_column(column_text='STATUS')
    logger_utility().info(f'filter: "{filter_dropdown}" values: {task_table_ui_status_values}')
    if filter_dropdown == 'all':
        assert len(set(task_table_ui_status_values)) > 1
        logger_utility().info(f'filter: {filter_dropdown} displays all status values: {task_table_ui_status_values}')
    else:
        for value in task_table_ui_status_values:
            assert filter_dropdown == value.lower()
            logger_utility().info(
                f'filter: {filter_dropdown} displays only {filter_dropdown} values: {task_table_ui_status_values}')
