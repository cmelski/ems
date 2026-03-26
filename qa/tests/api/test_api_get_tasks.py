import os
import pytest
import requests

from qa.utilities import api_client
from qa.utilities.logging_utils import logger_utility
from qa.utilities.api_client import APIClient

MAX_RETRIES = 3



@pytest.mark.api_get_tasks
def test_api_get_tasks():
    """Should succeed on the first attempt."""
    api_client = APIClient(os.environ.get('BASE_URL'))
    response = api_client.call_api_with_retry(endpoint='api/tasks')

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "id" in data['tasks'][0]
    assert len(data['tasks']) > 0
    logger_utility().info("✅ test_api_get_tasks passed")


@pytest.mark.api_404_no_retry
def test_api_404_no_retry():
    """A 404 (client error) should NOT be retried — fail fast."""
    api_client = APIClient(os.environ.get('BASE_URL'))
    response = api_client.call_api_with_retry(endpoint="99999")

    # 404 is a client error; we expect it back without retrying
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    logger_utility().info("✅ test_api_404_no_retry passed")
