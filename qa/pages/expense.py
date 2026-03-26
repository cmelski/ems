from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect


class ExpensePage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.expense_table = page.locator('#section-expenses table')
        self.add_expense_button = page.get_by_role("button", name="Log Expense")
        self.description_input = page.locator('#exp-desc')
        self.amount_input = page.locator('#exp-amount')
        self.category_input = page.locator('#exp-cat')
        self.due_date_input = page.locator('#exp-date-incurred')
        self.notes_input = page.locator('#exp-notes')
        self.reimbursable = page.locator('#exp-reimb')
        self.error_container = page.locator('#toasts')

    def find_expense_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.expense_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

    def find_expense_row_to_action(self, expense_details):
        return self.base_actions.find_row_to_action(self.expense_table, expense_details, 'expense')

    def cycle_expense_status(self, row):
        self.base_actions.cycle_status(row, 'expense')

    def find_table_cells_for_specific_column(self, column_text) -> list:
        column_index = self.base_actions.find_table_header_index(self.expense_table, column_text)

        return self.base_actions.find_table_cells_for_specific_column(self.expense_table,
                                                                      column_index, 'expenses')

    def find_table_cell_value(self, index: int, row) -> str:
        return self.base_actions.find_table_cell_value(index, row)

    def click_add_expense(self, values: list):
        self.description_input.fill(values[0])
        self.amount_input.fill(values[1])
        self.due_date_input.fill(values[2])
        self.category_input.select_option(values[3])
        self.notes_input.fill(values[4])
        self.reimbursable.select_option(values[5])
        self.add_expense_button.click()

    def verify_new_expense_in_expense_table(self, values):
        return self.base_actions.verify_new_item_in_table(self.expense_table, values, 'expense')

    def verify_expense_not_in_expense_table(self, expense_details):
        return self.base_actions.verify_item_not_in_table(expense_details, self.expense_table, 'expense')

    def fill_expense_form_invalid(self):
        self.add_expense_button.click()

    def delete_expense(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Expense deleted.')
