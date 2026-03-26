

from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect
from qa.pages.contact import ContactPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.add_contact_ui
def test_add_contact_ui(reset_db, page_instance: Page, get_new_contact_data: dict):
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Contacts')
    contact_panel = ContactPage(page_instance)
    # convert data to list
    contact_to_add_list = [v for v in get_new_contact_data.values()]
    # call add task function
    contact_panel.click_add_contact(contact_to_add_list)
    # verify it exists in the UI table
    new_contact_exists = contact_panel.verify_new_contact_in_contact_table(contact_to_add_list)
    assert len(new_contact_exists) > 1, f'New contact {get_new_contact_data} not found in the UI contacts table'
    logger_utility().info('Navigate to Dashboard panel...')
    dashboard_page.click_sidebar_menu('Dashboard')
    # verify activity log for the addition
    assert dashboard_page.find_activity_log(new_contact_exists, 'added', 'contact')
