from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.dashboard_loaded
def test_dashboard_loaded(page_instance):
    dashboard_page = DashboardPage(page_instance)
    expected_heading_one_text = 'Executor'
    expect(dashboard_page.page_heading_1).to_contain_text(expected_heading_one_text)
    heading_one_text = dashboard_page.page_heading_1.text_content().strip()
    logger_utility().info(f'Dashboard page heading 1 text: {heading_one_text} correctly contains '
                          f'expected text string: {expected_heading_one_text}')


@pytest.mark.dashboard_stats
def test_dashboard_stats_panel(reset_db, add_tasks_via_api, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Validating stats panel...')
    logger_utility().info('Open Tasks...')
    expect(dashboard_page.empty_activity_log).not_to_be_visible()
    # open tasks (status == PENDING, IN-PROGRESS)
    open_task_count_stats_panel = int(dashboard_page.open_tasks.inner_text())
    logger_utility().info(f'Dashboard stats panel open task count: {open_task_count_stats_panel}')
    # activity table open tasks count
    open_task_count_activity_table = dashboard_page.count_open_tasks_activity_table()
    logger_utility().info(f'Activity log table open task count: {open_task_count_activity_table}')
    assert open_task_count_stats_panel == open_task_count_activity_table




