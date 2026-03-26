from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.tasks import TasksPage
from qa.utilities.logging_utils import logger_utility
from qa.helpers.db_helper import DBHelper
from qa.helpers.api_helper import APIHelper
from qa.services.task_validation import TaskValidationService
import pytest


# page_instance, db_helper, api_helper are fixtures defined in
# conftest.py that yield their respective objects
# @pytest.mark.skip(reason="needs fixing")
@pytest.mark.verify_outstanding_tasks
def test_outstanding_tasks_consistency(
        reset_db,
        add_tasks_via_api,
        page_instance: Page,
        db_helper: DBHelper,
        api_helper: APIHelper
) -> None:
    dashboard = DashboardPage(page_instance)
    expect(dashboard.open_tasks).not_to_contain_text('0', timeout=2000)

    # Count of tasks that have status != done (dashboard panel)
    tasks_count_dashboard = int(dashboard.open_tasks.inner_text())
    logger_utility().info(f'Dashboard outstanding tasks count: {tasks_count_dashboard}')

    # click Tasks in the sidebar to load the Tasks panel
    dashboard.click_sidebar_menu('Tasks')

    # initialize the TaskValidationService to get outstanding tasks count from
    # the UI, DB, and API to compare

    service = TaskValidationService(
        TasksPage(page_instance),
        db_helper,
        api_helper
    )

    ui, db, api = service.get_outstanding_task_counts()

    # assertions

    assert tasks_count_dashboard == ui, (f'UI dashboard panel task count: {tasks_count_dashboard} '
                                         f'does not match UI outstanding task count: {ui}')
    logger_utility().info(
        f'UI dashboard panel task count: {tasks_count_dashboard} '
        f'matches UI outstanding task count: {ui}')

    assert ui == db, (f'UI outstanding task count: {ui} does not match DB '
                      f'outstanding task count: {db}')
    logger_utility().info(f'UI outstanding task count: {ui} '
                          f'matches DB outstanding task count: {db}')

    assert db == api, (f'DB outstanding task count: {db} does not match API '
                       f'outstanding task count: {api}')
    logger_utility().info(f'DB outstanding task count: {db} '
                          f'matches API outstanding task count: {api}')
