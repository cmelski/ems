from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect

from qa.pages.tasks import TasksPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.task_form_input
def test_add_task_form_validation(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Tasks')
    task_panel = TasksPage(page_instance)
    task_panel.fill_task_form_invalid()
    expect(task_panel.error_container).to_be_visible()
    expect(task_panel.error_container).to_have_text('Please enter a task description.')
    logger_utility().info(f'Error popup: "{task_panel.error_container.inner_text()}" correctly displayed')
