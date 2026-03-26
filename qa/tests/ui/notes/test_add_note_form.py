from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect

from qa.pages.note import NotePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.note_form_input
def test_add_note_form_validation(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Notes & Docs')
    note_panel = NotePage(page_instance)
    note_panel.fill_note_form_invalid()
    expect(note_panel.error_container).to_be_visible()
    expect(note_panel.error_container).to_have_text('Please enter a title.')
    logger_utility().info(f'Error popup: "{note_panel.error_container.inner_text()}" correctly displayed')
