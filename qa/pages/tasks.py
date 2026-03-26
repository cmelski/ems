import time

from qa.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect

TASK_FILTER_DROPDOWN_VALUES = ['pending', 'in-progress', 'done', 'all']


class TasksPage:

    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.task_table = page.locator('#section-tasks table')
        self.add_task_button = page.get_by_role("button", name="Add Task")
        self.description_input = page.locator('#task-desc')
        self.category_input = page.locator('#task-cat')
        self.due_date_input = page.locator('#task-due')
        self.priority_input = page.locator('#task-priority')
        self.task_filter_dropdown = '#task-filter'
        self.error_container = page.locator('#toasts')

    def select_task_filter(self, select_option):
        self.page.select_option(self.task_filter_dropdown, value=select_option)

    def find_task_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.task_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

    def find_task_row_to_action(self, task_details):
        return self.base_actions.find_row_to_action(self.task_table, task_details, 'task')

    def cycle_task_status(self, row):
        self.base_actions.cycle_status(row, 'task')

    def find_table_cells_for_specific_column(self, column_text) -> list:
        column_index = self.base_actions.find_table_header_index(self.task_table, column_text)

        return self.base_actions.find_table_cells_for_specific_column(self.task_table,
                                                                      column_index, 'tasks')

    def find_table_cell_value(self, index: int, row) -> str:
        return self.base_actions.find_table_cell_value(index, row)

    def count_outstanding_tasks(self) -> int:
        cell_values = self.find_table_cells_for_specific_column('STATUS')
        cell_values_count = len(cell_values)
        completed_tasks_count = cell_values.count('DONE')
        outstanding_tasks_count = cell_values_count - completed_tasks_count
        return outstanding_tasks_count

    def click_add_task(self, values: list):
        self.description_input.fill(values[0])
        self.category_input.select_option(values[1])
        self.due_date_input.fill(values[2])
        self.priority_input.select_option(values[3])
        self.add_task_button.click()

    def verify_new_task_in_task_table(self, values):
        return self.base_actions.verify_new_item_in_table(self.task_table, values, 'task')

    def verify_task_not_in_task_table(self, task_details):
        return self.base_actions.verify_item_not_in_table(task_details, self.task_table, 'task')

    def fill_task_form_invalid(self):
        self.add_task_button.click()

    def delete_task(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Task deleted.')
