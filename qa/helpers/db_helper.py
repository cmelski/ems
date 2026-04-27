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

    def get_contacts(self):

        contacts = self.db_client.get_contacts()
        return contacts

    def add_contact(self, contact_info):

        contact = self.db_client.add_contact(contact_info)
        return contact

    def get_settings(self):

        settings = self.db_client.get_estate_settings()
        return settings

    def add_task(self, task_details):

        task = self.db_client.add_task_to_db(task_details)
        return task

    def get_task(self, task_id):
        task = self.db_client.get_task(task_id)
        return task


