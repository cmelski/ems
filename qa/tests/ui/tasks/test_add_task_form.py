from qa.tests.actions.task_actions import TaskActions
from playwright.sync_api import Page, expect
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.task_form_input_invalid
def test_add_task_form_validation(page_instance: Page) -> None:
    task_actions = TaskActions(page_instance)
    task_actions.dashboard_actions.navigate_to_panel('Tasks')
    task_actions.task_page.click_add_task()
    expect(task_actions.task_page.message_container).to_be_visible()
    expect(task_actions.task_page.message_container).to_have_text('Please enter a task description.')
    logger_utility().info(f'Error popup: "{task_actions.task_page.message_container.inner_text()}" correctly displayed')
