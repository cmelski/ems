import os
import random
from faker import Faker

import allure
import shutil
from pathlib import Path
import pytest

# load env file variables
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError, expect

from qa.helpers.db_helper import DBHelper
from qa.helpers.api_helper import APIHelper
from qa.integrations.jira_client import get_or_create_issue
from qa.utilities.common_utils import generate_random_string
from qa.utilities.logging_utils import logger_utility

from qa.utilities.db_client import DBClient
import json
from datetime import datetime, date

test_results = []
test_start = {}


# define test run parameters
# in terminal you can run for e.g. 'pytest test_web_framework_api.py --browser_name firefox'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default="test", help="starting url for UI tests"
    )

    parser.addoption(
        "--env", action="store", default="test", help="Environment to run tests against")

    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )


# load corresponding .env file based on --env parameter (e.g. test.env, staging.env, prod.env)
@pytest.fixture(scope="session", autouse=True)
def env(request):
    env_name = request.config.getoption("--env")

    # This gets the directory where conftest.py lives
    project_root = Path(__file__).resolve().parent

    env_path = project_root / f"{env_name}.env"

    print("Loading from:", env_path)

    load_dotenv(env_path, override=True)

    print("BASE_URL:", os.getenv("BASE_URL"))


# return the BASE_URL from the loaded .env file for use in tests
@pytest.fixture(scope="session")
def url_start(env):  # env fixture ensures .env is loaded first
    return os.environ.get("BASE_URL")


# allure results directory setup - clean before test run and create if doesn't exist
def pytest_sessionstart(session):
    allure_dir = Path("qa/allure-results")
    if allure_dir.exists():
        shutil.rmtree(allure_dir)
    allure_dir.mkdir(parents=True, exist_ok=True)


# Log test start times for duration calculation later
def pytest_runtest_logstart(nodeid, location):
    # called when test starts
    test_start[nodeid] = {
        "start_time": datetime.now().isoformat()
    }


# Log skipped and xfailed tests with details
def pytest_runtest_logreport(report):
    if report.skipped:
        logger_utility().info(f"SKIPPED: {report.nodeid} - {report.longrepr}")
    elif report.outcome == "xfailed":
        logger_utility().info(f"XFAIL: {report.nodeid} - {report.longrepr}")


# This hook is called after each test phase (setup, call, teardown).
# We only want to act on the "call" phase which is the actual test execution.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to handle test failures:
    - attach screenshot & log to Allure
    - create Jira issue if enabled
    """
    outcome = yield
    report = outcome.get_result()

    # logger_utility().info(
    #     f"HOOK → when={report.when} | outcome={report.outcome} | test={item.nodeid}"
    # )

    # Only process actual test execution
    if report.when != "call":
        return

    test_name = item.name

    if report.outcome == "passed":
        result = "PASSED"
    else:
        result = "FAILED"

    logger_utility().info(f"TEST RESULT → {test_name}: {result}")

    # --------------------
    # Only act on failures in the test body
    # --------------------

    if report.outcome != "failed":
        return

    logger_utility().info(f"Test failed: {item.nodeid}")

    # --------------------
    # Attach screenshot if page fixture exists
    # --------------------
    page = item.funcargs.get("page")
    if page:
        try:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            logger_utility().info("Attached screenshot to Allure report")
        except Exception as e:
            logger_utility().exception(f"Screenshot capture failed: {e}")

    # --------------------
    # Create Jira issue if enabled
    # --------------------
    if os.getenv("CREATE_JIRA_ON_FAILURE") == "true":
        test_name = item.nodeid
        error = str(report.longrepr)
        jira_project = os.environ.get('JIRA_PROJECT')
        try:
            issue_key = get_or_create_issue(test_name, error, jira_project)
            if issue_key:
                logger_utility().info(f"Issue key: {issue_key}")
                print(f"Issue key: {issue_key}")
                # Add Allure link
                allure.dynamic.link(os.environ.get('JIRA_URL') + '/browse/' + issue_key,
                                    name=f"Jira: {issue_key}")

                # Optionally attach the issue key as text too
                allure.attach(f"Jira issue: {issue_key}", name="Jira Issue Key",
                              attachment_type=allure.attachment_type.TEXT)

            else:
                logger_utility().warning("get_or_create_issue returned None")
        except Exception as e:
            logger_utility().exception(f"Failed to create Jira issue: {e}")
            print(f"Failed to create Jira issue: {e}")

    # --------------------
    # Attach logs to Allure
    # --------------------
    log_path = "logs/test_run.log"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            allure.attach(
                f.read(),
                name="Execution Log",
                attachment_type=allure.attachment_type.TEXT
            )
        logger_utility().info("Attached execution log to Allure")


# This hook is called before each test phase (setup, call, teardown).
def pytest_runtest_setup(item):
    logger_utility().info(f"▶ Starting {item.name}")


# A fixture that runs automatically without being requested in the test. autouse=True
# Framework-level concerns → autouse=True
@pytest.fixture(autouse=True)
def check_env(env):
    try:
        assert os.environ.get("BASE_URL"), "BASE_URL not set"
        logger_utility().info(f'BASE_URL is set: {os.environ.get("BASE_URL")}')
    except AssertionError:
        logger_utility().info('BASE_URL is not set')
        raise


# Example of another global fixture that could be used for setup/teardown around each test
def pytest_runtest_logreport(report):
    if report.skipped:
        logger_utility().info(f"SKIPPED: {report.nodeid} - {report.longrepr}")
    elif report.outcome == "xfailed":
        logger_utility().info(f"XFAIL: {report.nodeid} - {report.longrepr}")
    # Only care about actual test call (not setup/teardown)
    assertion_error = ''
    if report.when == "call":
        node_id = report.nodeid
        if report.failed:
            # extract only the assertion message
            if hasattr(report.longrepr, "reprcrash"):
                assertion_error = report.longrepr.reprcrash.message.split('\n')[0]
        else:
            assertion_error = 'N/A'
        test_results.append({
            "test_name": report.nodeid,
            "result": report.outcome.upper(),
            "error": assertion_error,
            "test_start": test_start[node_id]['start_time'],
            "test_end": datetime.now().isoformat(),
            "duration": report.duration
        })


# At the end of the test session, write the test results to a JSON file for reporting purposes
def pytest_sessionfinish(session, exitstatus):
    data = {
        "test_run_results": test_results
    }

    with open("qa/logs/pass_fail_log.json", "w") as f:
        json.dump(data, f, indent=2)


@pytest.fixture(scope='function')
def db_helper():
    db_helper_object = DBHelper()
    yield db_helper_object
    db_helper_object.db_client.close()


@pytest.fixture(scope='function')
def reset_db(db_helper):
    logger_utility().info('Resetting DB tables...')
    db_helper.clean_db()


@pytest.fixture()
def get_new_task_data():
    task_description = generate_random_string()
    categories = ['Legal', 'Financial', 'Property', 'Distribution', 'Notifications', 'Other']
    priorities = ['High', 'Medium', 'Low']
    category = random.choice(categories)
    priority = random.choice(priorities)
    fake = Faker('en_GB')
    due_date = fake.future_date().isoformat()
    return {"description": task_description,
            "category": category,
            "due_date": due_date,
            "priority": priority,
            "status": "PENDING"
            }


@pytest.fixture()
def get_new_bill_data():
    bill_description = generate_random_string()
    types = ['Utility', 'Mortgage', 'Credit Card', 'Medical', 'Tax', 'Insurance', 'Other']
    bill_type = random.choice(types)
    fake = Faker('en_GB')
    due_date = fake.future_date().isoformat()
    amount = '50000'
    return {"description": bill_description,
            "amount": amount,
            "due_date": due_date,
            "bill_type": bill_type,
            "status": "UNPAID"
            }


@pytest.fixture()
def get_new_expense_data():
    expense_description = generate_random_string()
    categories = ['Legal Fees', 'Court Costs', 'Funeral', 'Property', 'Accounting', 'Travel', 'Miscellaneous']
    bill_category = random.choice(categories)
    fake = Faker('en_GB')
    due_date = fake.future_date().isoformat()
    amount = '10000.55'
    notes = generate_random_string()
    reimbursable = 'Yes'
    return {"description": expense_description,
            "amount": amount,
            "date_incurred": due_date,
            "category": bill_category,
            "notes": notes,
            "reimbursable": reimbursable,
            "status": "UNPAID"
            }


@pytest.fixture()
def get_new_asset_data():
    asset_name = generate_random_string()
    types = ['Real Estate', 'Bank Account', 'Vehicle', 'Investment', 'Personal Property', 'Life Insurance',
             'Business Interest', 'Other']
    asset_type = random.choice(types)
    value = '25000.76'
    beneficiary = generate_random_string()
    location = generate_random_string()
    statuses = ['Identified', 'Appraised', 'In Transfer', 'Distributed', 'Sold']
    status = random.choice(statuses)

    return {"name": asset_name,
            "type": asset_type,
            "value": value,
            "beneficiary": beneficiary,
            "location": location,
            "status": status
            }


@pytest.fixture()
def get_new_contact_data():
    contact_name = generate_random_string() + ' ' + generate_random_string()
    roles = ['Attorney', 'Executor', 'Accountant', 'Beneficiary', 'Financial Advisor', 'Real Estate Agent',
             'Creditor', 'Other']
    contact_role = random.choice(roles)
    fake = Faker('en_GB')
    phone = fake.phone_number()
    email = fake.email()

    return {"name": contact_name,
            "role": contact_role,
            "phone": phone,
            "email": email
            }

@pytest.fixture()
def get_new_note_data():
    current_date = date.today().isoformat()
    note_title = generate_random_string()
    categories = ['Meeting Notes', 'Legal', 'Financial', 'Beneficiary', 'Correspondence',
                  'Miscellaneous']
    note_category = random.choice(categories)
    note_content = generate_random_string() + ' ' + generate_random_string() + ' ' + generate_random_string()

    return {"date": current_date,
            "title": note_title,
            "category": note_category,
            "content": note_content
            }

@pytest.fixture(scope='function')
def api_helper():
    api_helper_object = APIHelper()
    return api_helper_object


@pytest.fixture()
def add_task_via_api(api_helper, get_new_task_data) -> tuple:
    logger_utility().info('Adding a new task via API...')
    response = api_helper.add_task(get_new_task_data)
    task_id = response['task']['id']
    task_description = response['task']['description']
    return task_id, task_description


@pytest.fixture()
def add_bill_via_api(api_helper, get_new_bill_data) -> tuple:
    logger_utility().info('Adding a new bill via API...')
    formatted_amount = get_new_bill_data['amount']
    get_new_bill_data['amount'] = float(formatted_amount)
    response = api_helper.add_bill(get_new_bill_data)
    bill_id = response['bill']['id']
    bill_description = response['bill']['description']
    return bill_id, bill_description


@pytest.fixture()
def add_expense_via_api(api_helper, get_new_expense_data) -> tuple:
    logger_utility().info('Adding a new expense via API...')
    formatted_amount = get_new_expense_data['amount']
    get_new_expense_data['amount'] = float(formatted_amount)
    response = api_helper.add_expense(get_new_expense_data)
    expense_id = response['expense']['id']
    expense_description = response['expense']['description']
    return expense_id, expense_description

@pytest.fixture()
def add_asset_via_api(api_helper, get_new_asset_data) -> tuple:
    logger_utility().info('Adding a new asset via API...')
    formatted_value = get_new_asset_data['value']
    get_new_asset_data['value'] = float(formatted_value)
    response = api_helper.add_asset(get_new_asset_data)
    asset_id = response['asset']['id']
    asset_name = response['asset']['name']
    return asset_id, asset_name

@pytest.fixture()
def add_contact_via_api(api_helper, get_new_contact_data) -> tuple:
    logger_utility().info('Adding a new contact via API...')
    response = api_helper.add_contact(get_new_contact_data)
    contact_id = response['contact']['id']
    contact_name = response['contact']['name']
    return contact_id, contact_name

@pytest.fixture()
def add_note_via_api(api_helper, get_new_note_data) -> tuple:
    logger_utility().info('Adding a new note via API...')
    response = api_helper.add_note(get_new_note_data)
    note_id = response['note']['id']
    note_title = response['note']['title']
    return note_id, note_title


@pytest.fixture(scope='function')
def add_tasks_via_api(api_helper):
    logger_utility().info('Adding 3 new tasks via API...')
    categories = ['Legal', 'Financial', 'Property', 'Distribution', 'Notifications', 'Other']
    priorities = ['High', 'Medium', 'Low']
    status = ['PENDING', 'IN-PROGRESS', 'DONE']
    fake = Faker('en_GB')
    for i in range(3):
        task_description = generate_random_string()
        category = random.choice(categories)
        priority = random.choice(priorities)
        due_date = fake.future_date().isoformat()
        new_task = {"description": task_description,
                    "category": category,
                    "due_date": due_date,
                    "priority": priority,
                    "status": status[i]
                    }

        response = api_helper.add_task(new_task)


# main tests fixture that yields page object
# and then closes context and browser after yield as part of teardown
@pytest.fixture(scope="function")
def page_instance(request, url_start):
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("--headless")

    with sync_playwright() as p:
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)

        context = browser.new_context()

        page = context.new_page()

        page.goto(url_start)
        logger_utility().info('Launching UI...')

        try:
            yield page
        finally:
            context.close()
            browser.close()
