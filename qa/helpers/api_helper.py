import json
import os
from qa.utilities.logging_utils import logger_utility
from qa.utilities.api_client import APIClient


class APIHelper:

    def __init__(self):
        self.api_client = APIClient(os.environ.get('BASE_URL'))

    def get_outstanding_tasks_count(self):
        response = self.api_client.call_api_with_retry(endpoint='api/tasks')
        assert response.status_code == 200
        data = response.json()
        outstanding_tasks_count = 0
        for item in data['tasks']:
            if item['status'] == 'pending' or item['status'] == 'in-progress':
                outstanding_tasks_count += 1

        return outstanding_tasks_count

    def get_task_by_description(self, description):
        response = self.api_client.call_api_with_retry(
            endpoint='api/task',
            params={'description': description}  # ✅ correct
        )
        assert response.status_code == 200
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        if data:
            logger_utility().info(f'API call successfully returned task with description: {description}')
            return True
        else:
            return False

    def add_task(self, payload):
        logger_utility().info(f'Payload for api helper: {payload}')
        response = self.api_client.call_api_with_retry(
            endpoint="api/tasks",
            method="POST",
            json=payload
        )
        assert response.status_code == 201
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        return data

    def add_bill(self, payload):
        logger_utility().info(f'Payload for api helper: {payload}')
        response = self.api_client.call_api_with_retry(
            endpoint="api/bills",
            method="POST",
            json=payload
        )
        assert response.status_code == 201
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        return data

    def add_expense(self, payload):
        logger_utility().info(f'Payload for api helper: {payload}')
        response = self.api_client.call_api_with_retry(
            endpoint="api/expenses",
            method="POST",
            json=payload
        )
        assert response.status_code == 201
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        return data

    def add_asset(self, payload):
        logger_utility().info(f'Payload for api helper: {payload}')
        response = self.api_client.call_api_with_retry(
            endpoint="api/assets",
            method="POST",
            json=payload
        )
        assert response.status_code == 201
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        return data

    def add_contact(self, payload):
        logger_utility().info(f'Payload for api helper: {payload}')
        response = self.api_client.call_api_with_retry(
            endpoint="api/contacts",
            method="POST",
            json=payload
        )
        assert response.status_code == 201
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        return data

    def add_note(self, payload):
        logger_utility().info(f'Payload for api helper: {payload}')
        response = self.api_client.call_api_with_retry(
            endpoint="api/notes",
            method="POST",
            json=payload
        )
        assert response.status_code == 201
        data = response.json()
        logger_utility().info(f'API data returned: {data}')
        return data
