from qa.tests.pages.base import BasePage
from qa.utilities.logging_utils import logger_utility


class TasksPage:

    def __init__(self, page):
        self.page = page
        self.task_table = page.locator('#section-tasks table')
        self.add_task_button = page.get_by_role("button", name="Add Task")
        self.description_input = page.locator('#task-desc')
        self.category_input = page.locator('#task-cat')
        self.due_date_input = page.locator('#task-due')
        self.priority_input = page.locator('#task-priority')
        self.assignee_input = page.locator('#task-assignee')
        self.task_filter_dropdown = '#task-filter'
        self.message_container = page.locator('#toasts')
        self.row_fields = {'description': 'td[name="task-name"',
                           'category': 'td select[name="task-cat"]',
                           'due_date': 'td input[type="date"]',
                           'priority': 'td select[name="task-priority"]',
                           'assignee': 'td select[name="assignee"]',
                           }

    def enter_task_description(self, description: str):
        self.description_input.fill(description)

    def select_task_category(self, category: str):
        self.category_input.select_option(category)

    def enter_task_due_date(self, due_date: str):
        self.due_date_input.fill(due_date)

    def select_task_priority(self, priority: str):
        self.priority_input.select_option(priority)

    def select_task_assignee(self, assignee: int):
        logger_utility().info(f'Assignee: {assignee}')
        self.assignee_input.select_option(str(assignee))

    def select_task_category_row(self, row, category: str):
        row.locator(self.row_fields['category']).select_option(category)

    def enter_task_due_date_row(self, row, due_date: str):
        row.locator(self.row_fields['due_date']).fill(due_date)

    def select_task_priority_row(self, row, priority: str):
        row.locator(self.row_fields['priority']).select_option(priority)

    def select_task_assignee_row(self, row, assignee: int):
        row.locator(self.row_fields['assignee']).select_option(str(assignee))

    def select_task_filter(self, select_option):
        self.page.select_option(self.task_filter_dropdown, value=select_option)

    def find_task_table_cell_value(self, row, column_text):
        column_index = self.base_actions.find_table_header_index(self.task_table, column_text)
        cell_value = self.find_table_cell_value(column_index, row)
        return cell_value

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

    def click_add_task(self):
        self.add_task_button.click()

    def click_save_task(self, row):
        row.get_by_title("Save").click()

    def delete_task(self, row):
        row.get_by_title('Delete').click()
        logger_utility().info('Task deleted.')
