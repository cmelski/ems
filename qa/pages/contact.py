from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class ContactPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.contact_table = page.locator('#section-contacts table')
        self.add_contact_button = page.get_by_role("button", name="Add Contact")
        self.contact_name = page.locator('#contact-name')
        self.contact_role = page.locator('#contact-role')
        self.contact_phone = page.locator('#contact-phone')
        self.contact_email = page.locator('#contact-email')
        self.error_container = page.locator('#toasts')

    def find_contact_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.contact_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

    def find_contact_row_to_action(self, contact_details):
        return self.base_actions.find_row_to_action(self.contact_table, contact_details, 'contact')

    def cycle_contact_status(self, row):
        self.base_actions.cycle_status(row, 'contact')

    def find_table_cells_for_specific_column(self, column_text) -> list:
        column_index = self.base_actions.find_table_header_index(self.contact_table, column_text)

        return self.base_actions.find_table_cells_for_specific_column(self.contact_table,
                                                                      column_index, 'contacts')

    def find_table_cell_value(self, index: int, row) -> str:
        return self.base_actions.find_table_cell_value(index, row)

    def click_add_contact(self, values: list):
        self.contact_name.fill(values[0])
        self.contact_role.select_option(values[1])
        self.contact_phone.fill(values[2])
        self.contact_email.fill(values[3])
        self.add_contact_button.click()

    def verify_new_contact_in_contact_table(self, values):
        return self.base_actions.verify_new_item_in_table(self.contact_table, values, 'contact')

    def verify_contact_not_in_contact_table(self, contact_details):
        return self.base_actions.verify_item_not_in_table(contact_details, self.contact_table, 'contact')

    def fill_contact_form_invalid(self):
        self.add_contact_button.click()

    def delete_contact(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Contact deleted.')
