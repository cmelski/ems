from qa.tests.actions.dashboard_actions import DashboardActions
from playwright.sync_api import expect
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.dashboard_loaded
def test_dashboard_loaded(page_instance):
    dashboard_actions = DashboardActions(page_instance)
    expected_heading_one_text = 'Executor'
    expect(dashboard_actions.dashboard_page.page_heading_1).to_contain_text(expected_heading_one_text)
    heading_one_text = dashboard_actions.dashboard_page.page_heading_1.text_content().strip()
    logger_utility().info(f'Dashboard page heading 1 text: {heading_one_text} correctly contains '
                          f'expected text string: {expected_heading_one_text}')


@pytest.mark.dashboard_stats
def test_dashboard_stats_panel(reset_db, add_tasks_via_db, page_instance):
    dashboard_actions = DashboardActions(page_instance)
    # get open tasks from DB
    open_tasks_db = 0
    for task in add_tasks_via_db:
        if task[5] == 'PENDING' or task[5] == 'IN-PROGRESS':
            open_tasks_db += 1
    logger_utility().info(f'DB open task count: {open_tasks_db}')
    # get open tasks on the dashboard UI panel
    logger_utility().info('Validating stats panel...')
    logger_utility().info('Open Tasks...')
    # open tasks (status == PENDING, IN-PROGRESS)
    # page_instance.wait_for_function("() => state.tasks && state.tasks.length > 0")
    expect(dashboard_actions.dashboard_page.open_tasks).to_have_text(str(open_tasks_db))
    open_task_count_stats_panel = int(dashboard_actions.dashboard_page.open_tasks.inner_text())
    logger_utility().info(f'Dashboard stats panel open task count: {open_task_count_stats_panel}')
    assert open_task_count_stats_panel == open_tasks_db




