from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class NotePage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.note_table = page.locator('#section-notes table')
        self.add_note_button = page.get_by_role("button", name="Save Note")
        self.note_title = page.locator('#note-title')
        self.note_category = page.locator('#note-cat')
        self.note_content = page.locator('#note-content')
        self.error_container = page.locator('#toasts')
        self.note_modal = page.locator('#note-modal')

    def get_note_modal_details(self):

        modal_title = self.note_modal.locator('#note-modal-title').text_content()
        modal_body = self.note_modal.locator('#note-modal-meta').text_content()
        modal_date = modal_body.split('·')[0].strip()
        modal_category = modal_body.split('·')[1].strip()
        modal_content = self.note_modal.locator('#note-modal-content').text_content()
        return modal_title, modal_date, modal_category, modal_content

    def get_note_row_values(self, note_row):
        cell_values = self.base_actions.get_table_row_cells(note_row)
        return cell_values

    def find_note_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.note_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

    def find_note_row_to_action(self, note_details):
        return self.base_actions.find_row_to_action(self.note_table, note_details, 'note')

    def cycle_note_status(self, row):
        self.base_actions.cycle_status(row, 'note')

    def find_table_cells_for_specific_column(self, column_text) -> list:
        column_index = self.base_actions.find_table_header_index(self.note_table, column_text)

        return self.base_actions.find_table_cells_for_specific_column(self.note_table,
                                                                      column_index, 'notes')

    def find_table_cell_value(self, index: int, row) -> str:
        return self.base_actions.find_table_cell_value(index, row)

    def click_add_note(self, values: list):
        self.note_title.fill(values[1])
        self.note_category.select_option(values[2])
        self.note_content.fill(values[3])
        self.add_note_button.click()

    def verify_new_note_in_note_table(self, values):
        return self.base_actions.verify_new_item_in_table(self.note_table, values, 'note')

    def verify_note_not_in_note_table(self, note_details):
        return self.base_actions.verify_item_not_in_table(note_details, self.note_table, 'note')

    def fill_note_form_invalid(self):
        self.add_note_button.click()

    def delete_note(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Note deleted.')

    def view_note(self, row):
        row.get_by_title('View').click()
        logger_utility().info('Viewing note...')
