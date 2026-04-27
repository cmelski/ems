from qa.tests.actions.dashboard_actions import DashboardActions
from qa.tests.pages.tasks import TasksPage
from qa.tests.pages.base import BasePage
from qa.helpers.db_helper import DBHelper


class TaskActions:
    def __init__(self, page):
        self.page = page
        self.dashboard_actions = DashboardActions(page)
        self.task_page = TasksPage(page)
        self.base_page = BasePage(page)
        self.db_helper = DBHelper()

    def add_task(self, description, category, due_date, priority, assignee):
        self.task_page.enter_task_description(description)
        self.task_page.select_task_category(category)
        self.task_page.enter_task_due_date(due_date)
        self.task_page.select_task_priority(priority)
        self.task_page.select_task_assignee(assignee)
        self.task_page.click_add_task()

    def update_task(self, row, category, due_date, priority, assignee):
        self.task_page.select_task_category_row(row, category)
        self.task_page.enter_task_due_date_row(row, due_date)
        self.task_page.select_task_priority_row(row, priority)
        self.task_page.select_task_assignee_row(row, assignee)
        self.task_page.click_save_task(row)

    def delete_task(self, row):
        self.base_page.delete_row(row, 'Delete', 'task')

    def cycle_task_status(self, row):
        self.base_page.cycle_status(row, 'task')

    def filter_task(self):
        pass

    def validate_task_status(self, task_id):
        task = self.db_helper.get_task(task_id)
        status = task[5]
        return status

