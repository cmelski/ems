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
@pytest.mark.add_task
def test_add_task(
        reset_db,
        page_instance: Page,
        db_helper: DBHelper,
        api_helper: APIHelper
) -> None:
    dashboard = DashboardPage(page_instance)

    # click Tasks in the sidebar to load the Tasks panel
    dashboard.click_sidebar_menu('Tasks')

    # initialize the TaskValidationService

    service = TaskValidationService(
        TasksPage(page_instance),
        db_helper,
        api_helper
    )

    ui, api, db = service.add_task()

    assert api is True
    assert db is True
    logger_utility().info(f'New task added successfully')
