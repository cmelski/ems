

from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.note import NotePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_note_ui
def test_add_note_ui(reset_db, page_instance: Page, get_new_note_data: dict):
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Notes & Docs')
    note_panel = NotePage(page_instance)
    # convert data to list
    note_to_add_list = [v for v in get_new_note_data.values()]
    # call add task function
    note_panel.click_add_note(note_to_add_list)
    # verify it exists in the UI table
    new_note_exists = note_panel.verify_new_note_in_note_table(note_to_add_list)
    assert len(new_note_exists) > 1, f'New note {get_new_note_data} not found in the UI notes table'
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the addition
    assert dashboard_page.find_activity_log(new_note_exists, 'added', 'note')
