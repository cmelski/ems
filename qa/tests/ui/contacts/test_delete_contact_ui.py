
from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.contact import ContactPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.delete_contact_ui
def test_delete_contact_ui(reset_db, add_contact_via_api: tuple, page_instance):
    dashboard_page = DashboardPage(page_instance)
    logger_utility().info('Navigate to Contacts panel')
    dashboard_page.click_sidebar_menu('Contacts')
    contact_panel = ContactPage(page_instance)
    # find row to delete
    contact_row = contact_panel.find_contact_row_to_action(add_contact_via_api)
    contact_panel.delete_contact(contact_row)
    # verify confirmation popup
    expect(contact_panel.error_container).to_contain_text('Contact removed')
    # verify contact no longer exists in the UI table
    deleted = contact_panel.verify_contact_not_in_contact_table(add_contact_via_api)
    assert deleted is True, f'Contact {add_contact_via_api} still exists in the UI contacts table'
    logger_utility().info(f'Contact {add_contact_via_api} not found in the UI contacts table after Delete')
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the deletion
    assert dashboard_page.find_activity_log(add_contact_via_api, 'deleted', 'contact')
