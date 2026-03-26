
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.note import NotePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_note_ui
def test_delete_note_ui(reset_db, add_note_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Notes panel')
    dashboard_page.click_sidebar_menu('Notes & Docs')
    note_panel = NotePage(page_instance)
    # find row to delete
    note_row = note_panel.find_note_row_to_action(add_note_via_api)
    note_panel.delete_note(note_row)
    # verify confirmation popup
    expect(note_panel.error_container).to_contain_text('Note removed')
    # verify note no longer exists in the UI table
    deleted = note_panel.verify_note_not_in_note_table(add_note_via_api)
    assert deleted is True, f'Note {add_note_via_api} still exists in the UI notes table'
    logger_utility().info(f'Note {add_note_via_api} not found in the UI notes table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_note_via_api, 'deleted', 'note')
