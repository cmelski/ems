import os

from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.protected_endpoint
def test_protected_endpoint(page_instance_login_tests):
    page_instance_login_tests.goto(os.environ.get('BASE_URL') + 'api/tasks')
    assert 'login' in page_instance_login_tests.url
    logger_utility().info(f'User remains on the login page')
