from qa.utilities.db_client import DBClient
from qa.utilities.logging_utils import logger_utility


class DBHelper:
    def __init__(self):
        self.db_client = DBClient()

    def clean_db(self):
        tables = ('activity', 'bill', 'task', 'expense', 'asset', 'contact', 'note')
        self.db_client.clean_db_tables(tables)

    def get_outstanding_tasks_count(self):
        tasks = self.db_client.get_outstanding_tasks()
        outstanding_tasks_count = len(tasks)

        return outstanding_tasks_count

    def get_task_by_description(self, description):

        task = self.db_client.get_task_by_description(description)
        if task:
            logger_utility().info(f'New task with description: {description} found in DB')
            return True

        else:
            return False
