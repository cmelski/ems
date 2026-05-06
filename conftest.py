import os
import random
from faker import Faker
import yaml
import allure
import shutil
from pathlib import Path
import pytest
import time
import datetime

# load env file variables
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError, expect

from qa.helpers.db_helper import DBHelper
from qa.helpers.api_helper import APIHelper
from qa.integrations.jira_client import get_or_create_issue
from qa.utilities.common_utils import generate_random_string
from qa.utilities.logging_utils import logger_utility
from qa.utilities.db_client_metrics import DBClientMetrics

from qa.utilities.db_client import DBClient
import json
from datetime import datetime, date
from dev.main import app  # 👈 import your actual app

test_results = []
test_start = {}
run_start_time = None


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

    parser.addoption(
        "--build-version", action="store", default="unknown", help="Build version for test run tracking"
    )

    parser.addoption(
        "--scope", action="store", default="single", help="test run scope - single, subset, smoke, regression, full"
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
    db_client_metrics = DBClientMetrics()
    db_client_metrics.load_test_cases()

    allure_dir = Path("qa/allure-results")
    if allure_dir.exists():
        shutil.rmtree(allure_dir)
    allure_dir.mkdir(parents=True, exist_ok=True)

    conn = DBClientMetrics()
    cur = conn.cursor
    scope = session.config.getoption("--scope")
    build_version = session.config.getoption("--build-version")

    cur.execute("""
        INSERT INTO test_runs (run_date, build_version, run_scope, total_tests)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """, (
        date.today(),
        build_version,
        scope,
        0  # placeholder for now
    ))

    session.config.run_id = cur.fetchone()[0]

    conn.commit()
    conn.close()


def pytest_collection_finish(session):
    session.config.total_tests = len(session.items)


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
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    # safe duration
    duration = time.perf_counter() - getattr(item, "start_time", time.perf_counter())

    status = "passed" if report.passed else "failed"

    try:
        conn = DBClientMetrics()
        cur = conn.cursor

        cur.execute("""
            INSERT INTO test_case_results (
                run_id,
                test_name,
                duration_seconds,
                status
            )
            VALUES (%s, %s, %s, %s)
        """, (
            item.config.run_id,
            item.nodeid,
            duration,
            status
        ))

        conn.commit()

    except Exception as e:
        print(f"DB INSERT FAILED: {e}")

    finally:
        conn.close()

    # handle defects

    if status == 'failed':
        try:
            conn = DBClientMetrics()
            cur = conn.cursor

            cur.execute("""
                SELECT * FROM test_cases
                WHERE name = %s;
                """, (item.nodeid,))  # <-- pass as tuple

            test_case = cur.fetchone()
            area = test_case[3]
            test_case_id = test_case[0]

            cur.execute("""
                   INSERT INTO defects (
                       created_date,
                       severity,
                       area,
                       test_case_id
                   )
                   VALUES (%s, %s, %s, %s)
               """, (
                date.today(),
                'Medium',
                area,
                test_case_id
            ))

            conn.commit()

        except Exception as e:
            print(f"DB INSERT FAILED: {e}")

        finally:
            conn.close()



#     """
#     Hook to handle test failures:
#     - attach screenshot & log to Allure
#     - create Jira issue if enabled
#     """
#     outcome = yield
#     report = outcome.get_result()
#
#     # logger_utility().info(
#     #     f"HOOK → when={report.when} | outcome={report.outcome} | test={item.nodeid}"
#     # )
#
#     # Only process actual test execution
#     if report.when != "call":
#         return
#
#     test_name = item.name
#
#     if report.outcome == "passed":
#         result = "PASSED"
#     else:
#         result = "FAILED"
#
#     logger_utility().info(f"TEST RESULT → {test_name}: {result}")
#
#     # --------------------
#     # Only act on failures in the test body
#     # --------------------
#
#     if report.outcome != "failed":
#         return
#
#     logger_utility().info(f"Test failed: {item.nodeid}")
#
#     # --------------------
#     # Attach screenshot if page fixture exists
#     # --------------------
#     page = item.funcargs.get("page")
#     if page:
#         try:
#             screenshot = page.screenshot()
#             allure.attach(
#                 screenshot,
#                 name="Failure Screenshot",
#                 attachment_type=allure.attachment_type.PNG
#             )
#             logger_utility().info("Attached screenshot to Allure report")
#         except Exception as e:
#             logger_utility().exception(f"Screenshot capture failed: {e}")
#
#     # --------------------
#     # Create Jira issue if enabled
#     # --------------------
#     if os.getenv("CREATE_JIRA_ON_FAILURE") == "true":
#         test_name = item.nodeid
#         error = str(report.longrepr)
#         jira_project = os.environ.get('JIRA_PROJECT')
#         try:
#             issue_key = get_or_create_issue(test_name, error, jira_project)
#             if issue_key:
#                 logger_utility().info(f"Issue key: {issue_key}")
#                 print(f"Issue key: {issue_key}")
#                 # Add Allure link
#                 allure.dynamic.link(os.environ.get('JIRA_URL') + '/browse/' + issue_key,
#                                     name=f"Jira: {issue_key}")
#
#                 # Optionally attach the issue key as text too
#                 allure.attach(f"Jira issue: {issue_key}", name="Jira Issue Key",
#                               attachment_type=allure.attachment_type.TEXT)
#
#             else:
#                 logger_utility().warning("get_or_create_issue returned None")
#         except Exception as e:
#             logger_utility().exception(f"Failed to create Jira issue: {e}")
#             print(f"Failed to create Jira issue: {e}")
#
#     # --------------------
#     # Attach logs to Allure
#     # --------------------
#     log_path = "logs/test_run.log"
#     if os.path.exists(log_path):
#         with open(log_path, "r") as f:
#             allure.attach(
#                 f.read(),
#                 name="Execution Log",
#                 attachment_type=allure.attachment_type.TEXT
#             )
#         logger_utility().info("Attached execution log to Allure")
#
#     if call.when == "call":  # only actual test execution
#         duration = time.perf_counter() - item.start_time
#
#         outcome = call.excinfo is None
#         status = "passed" if outcome else "failed"
#
#         conn = DBClientMetrics()
#         cur = conn.cursor
#
#         cur.execute("""
#                 INSERT INTO test_case_results (
#                     run_id,
#                     test_name,
#                     duration_seconds,
#                     status
#                 )
#                 VALUES (%s, %s, %s, %s)
#             """, (
#             item.config.run_id,
#             item.nodeid,
#             duration,
#             status
#         ))
#
#         conn.commit()
#         conn.close()


# This hook is called before each test phase (setup, call, teardown).
def pytest_runtest_setup(item):
    logger_utility().info(f"▶ Starting {item.name}")
    item.start_time = time.perf_counter()


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
    conn = DBClientMetrics()
    cur = conn.cursor

    cur.execute("""
            UPDATE test_runs
            SET total_tests = %s
            WHERE id = %s
        """, (
        len(session.items),
        session.config.run_id
    ))

    conn.commit()
    conn.close()

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
def get_updated_task_data(db_helper):
    contact_info = []
    task_description = generate_random_string()
    category = 'Distribution'
    priority = 'Low'
    fake = Faker('en_GB')
    due_date = fake.future_date().isoformat()
    contact_info.extend(['Test Contact 2', 'Lawyer', '48484', 'fff@yahoo.com'])
    contact = db_helper.add_contact(contact_info)
    contacts = db_helper.get_contacts()
    assignee_id = contacts[1][0]
    assignee_name = contacts[0][1]

    return {"description": task_description,
            "category": category,
            "due_date": due_date,
            "priority": priority,
            "status": "PENDING",
            "assignee_id": assignee_id,
            "assignee_name": assignee_name
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
def add_task_via_db(db_helper, task_data) -> tuple:
    logger_utility().info('Adding a new task via DB call...')
    estate = db_helper.get_settings()
    estate_id = estate[0]
    task_details = []
    description = task_data['new_task']['task_name']
    category = task_data['new_task']['task_category']
    due_date = task_data['new_task']['task_due_date']
    status = 'PENDING'
    priority = task_data['new_task']['task_priority']
    assignee = task_data['new_task']['task_assignee_id']
    task_details.extend([description, category, due_date, priority, status, estate_id, assignee])
    result = db_helper.add_task(task_details)
    task_id = result[0]
    task_description = result[1]
    logger_utility().info(f'New task added via DB call: {task_details}')
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
def add_tasks_via_db(db_helper):
    logger_utility().info('Adding 3 new tasks via DB call...')
    fake = Faker('en_GB')
    categories = ['Legal', 'Financial', 'Property', 'Distribution', 'Notifications', 'Other']
    priorities = ['High', 'Medium', 'Low']
    statuses = ['PENDING', 'IN-PROGRESS', 'DONE']
    estate = db_helper.get_settings()
    estate_id = estate[0]
    contact_info = []
    assignee_info = []
    results = []
    contacts = db_helper.get_contacts()
    if not contacts:
        contact_info.extend(['Test Contact', 'Executor', '3838383', 'ddh@gmail.com'])
        contact = db_helper.add_contact(contact_info)
        assignee = contact[0]
    else:
        assignee_info = random.choice(contacts)
        assignee = assignee_info[0]

    for i in range(3):
        task_details = []
        description = generate_random_string()
        category = random.choice(categories)
        due_date = fake.future_date().isoformat()
        status = statuses[i]
        priority = random.choice(priorities)
        task_details.extend([description, category, due_date, priority, status, estate_id, assignee])
        result = db_helper.add_task(task_details)
        results.append(result)

    return results


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # make sure SECRET_KEY is set (important for sessions)
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "test-secret"

    with app.test_client() as client:
        yield client


class FakeUser:
    def __init__(self, id):
        self.id = id
        self.is_authenticated = True


@pytest.fixture
def test_user():
    return FakeUser(1)


@pytest.fixture(scope="session")
def login_data():
    with open("qa/tests/data/login_data.yaml") as f:
        data = yaml.safe_load(f)

    # Override sensitive fields from env vars
    data["valid_login"]["username"] = os.environ.get("USER_EMAIL", data["valid_login"]["username"])
    data["valid_login"]["password"] = (os.environ.get("USER_PASSWORD", data["valid_login"]["password"]))

    return data


@pytest.fixture(scope="function")
def task_data(db_helper):
    with open("qa/tests/data/task_data.yaml") as f:
        data = yaml.safe_load(f)

    fake = Faker('en_GB')
    task_due_date = fake.future_date().isoformat()
    data['new_task']['task_due_date'] = task_due_date

    contact_info = []
    contacts = db_helper.get_contacts()
    if not contacts:
        contact_info.extend(['Test Contact', 'Executor', '3838383', 'ddh@gmail.com'])
        contact = db_helper.add_contact(contact_info)
        data['new_task']['task_assignee_id'] = contact[0]
        data['new_task']['task_assignee_name'] = contact[1]
    else:
        assignee_info = random.choice(contacts)
        data['new_task']['task_assignee_id'] = assignee_info[0]
        data['new_task']['task_assignee_name'] = assignee_info[1]

    return data


def pytest_runtest_teardown(item, nextitem):
    duration = time.perf_counter() - item.start_time
    item.duration = duration


def pytest_runtest_call(item):
    item.start_time = time.perf_counter()


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

        state = "qa/auth_state_test.json" if os.path.exists("qa/auth_state_test.json") else None

        if state:
            context = browser.new_context(storage_state=state)
        else:
            context = browser.new_context()

        # context = browser.new_context()

        page = context.new_page()

        page.goto(url_start)

        logger_utility().info('Launching UI...')

        try:
            yield page
        finally:
            context.close()
            browser.close()


@pytest.fixture(scope="function")
def page_instance_login_tests(request, url_start):
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
