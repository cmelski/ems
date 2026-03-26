from qa.pages.dashboard import DashboardPage
from playwright.sync_api import Page, expect

from qa.pages.contact import ContactPage
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.contact_form_input
def test_add_contact_form_validation(page_instance: Page) -> None:
    dashboard_page = DashboardPage(page_instance)
    dashboard_page.click_sidebar_menu('Contacts')
    contact_panel = ContactPage(page_instance)
    contact_panel.fill_contact_form_invalid()
    expect(contact_panel.error_container).to_be_visible()
    expect(contact_panel.error_container).to_have_text('Please enter a contact name.')
    logger_utility().info(f'Error popup: "{contact_panel.error_container.inner_text()}" correctly displayed')
