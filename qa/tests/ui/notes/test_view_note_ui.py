
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.note import NotePage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.view_note_ui
def test_view_note_ui(reset_db, add_note_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Notes panel')
    dashboard_page.click_sidebar_menu('Notes & Docs')
    note_panel = NotePage(page_instance)
    # find row to view
    note_row = note_panel.find_note_row_to_action(add_note_via_api)
    cells = note_panel.get_note_row_values(note_row)
    logger_utility().info(f'Cell values: {cells}')
    note_panel.view_note(note_row)
    # verify note popup window
    note_modal_details = note_panel.get_note_modal_details()
    logger_utility().info(f'Note modal details: {note_modal_details}')
    assert note_modal_details[0] == cells[1]
    assert note_modal_details[1] == cells[0]
    assert note_modal_details[2] == cells[2]
    assert note_modal_details[3] == cells[3]