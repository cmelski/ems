import random

from qa.utilities.logging_utils import logger_utility
from qa.utilities.common_utils import generate_random_string


class TaskValidationService:

    def __init__(self, page, db_helper, api_helper):
        self.page = page
        self.db = db_helper
        self.api = api_helper

    def get_outstanding_task_counts(self) -> tuple[int, int, int]:
        logger_utility().info('Getting outstanding tasks count from task table on the UI...')
        ui = self.page.count_outstanding_tasks()
        logger_utility().info('Getting outstanding tasks count from task table in the DB...')
        db = self.db.get_outstanding_tasks_count()
        logger_utility().info('Getting outstanding tasks count from api...')
        api = self.api.get_outstanding_tasks_count()

        return ui, db, api

    def add_task(self):
        task_description = generate_random_string()
        categories = ['Legal', 'Financial', 'Property', 'Distribution', 'Notifications', 'Other']
        priorities = ['High', 'Medium', 'Low']
        category = random.choice(categories)
        priority = random.choice(priorities)

        # integration
        new_task_data = [task_description, category, '2026-06-30', priority]
        ui = self.page.click_add_task(new_task_data)


        # api

        api = self.api.get_task_by_description(task_description)

        # db

        db = self.db.get_task_by_description(task_description)
        logger_utility().info(f'DB: {db}')

        return ui, api, db