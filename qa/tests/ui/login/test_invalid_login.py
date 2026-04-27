import os

from playwright.sync_api import expect
from qa.tests.actions.auth_actions import AuthActions
from qa.utilities.logging_utils import logger_utility
import pytest


@pytest.mark.parametrize('invalid_credentials', [('', '', ''),
                                                 ('bad_username@gmail.com', 'bad_password', 'Invalid email'),
                                                 (os.environ.get('USER_EMAIL'), 'bad_password', 'Invalid password'),
                                                 ('bad_username@gmail.com', os.environ.get('USER_PASSWORD'), 'Invalid email')],
                         ids=['empty credentials', 'bad_credentials', 'valid email/wrong password',
                              'wrong username/valid password'])
@pytest.mark.invalid_login
def test_invalid_login_ui(page_instance_login_tests, invalid_credentials):
    auth = AuthActions(page_instance_login_tests)
    user_name = invalid_credentials[0]
    password = invalid_credentials[1]
    error_message = invalid_credentials[2]
    auth.login(user_name, password)

    if user_name  == '' and password == '':
        expect(auth.login_page.page_text).to_be_visible()
        logger_utility().info('User still on login page')
    else:
        expect(auth.login_page.page_body).to_contain_text(error_message)
        logger_utility().info(f'Error message: {error_message} correctly displayed')



