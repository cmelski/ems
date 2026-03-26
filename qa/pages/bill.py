from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class BillPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.bill_table = page.locator('#section-bills table')
        self.add_bill_button = page.get_by_role("button", name="Add Bill")
        self.description_input = page.locator('#bill-desc')
        self.amount_input = page.locator('#bill-amount')
        self.type_input = page.locator('#bill-type')
        self.due_date_input = page.locator('#bill-due')
        self.error_container = page.locator('#toasts')

    def find_bill_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.bill_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

    def find_bill_row_to_action(self, bill_details):
        return self.base_actions.find_row_to_action(self.bill_table, bill_details, 'bill')

    def cycle_bill_status(self, row):
        self.base_actions.cycle_status(row, 'bill')

    def find_table_cells_for_specific_column(self, column_text) -> list:
        column_index = self.base_actions.find_table_header_index(self.bill_table, column_text)

        return self.base_actions.find_table_cells_for_specific_column(self.bill_table,
                                                                      column_index, 'bills')

    def find_table_cell_value(self, index: int, row) -> str:
        return self.base_actions.find_table_cell_value(index, row)

    def click_add_bill(self, values: list):
        self.description_input.fill(values[0])
        self.amount_input.fill(values[1])
        self.due_date_input.fill(values[2])
        self.type_input.select_option(values[3])
        self.add_bill_button.click()

    def verify_new_bill_in_bill_table(self, values):
        return self.base_actions.verify_new_item_in_table(self.bill_table, values, 'bill')

    def verify_bill_not_in_bill_table(self, task_details):
        return self.base_actions.verify_item_not_in_table(task_details, self.bill_table, 'bill')

    def fill_bill_form_invalid(self):
        self.add_bill_button.click()

    def delete_bill(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Bill deleted.')
