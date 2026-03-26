import os
import requests
from requests.auth import HTTPBasicAuth
from qa.utilities.logging_utils import logger_utility


# --------------------------
# SEARCH EXISTING ISSUE
# --------------------------
def find_existing_issue(test_name):
    # --------------------------
    # CONFIG
    # --------------------------
    JIRA_URL = os.getenv("JIRA_URL")
    PROJECT_KEY = os.getenv("JIRA_PROJECT")
    AUTH = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))

    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    jql = (
        f'project = {PROJECT_KEY} '
        f'AND summary ~ "{test_name}" '
        f'AND statusCategory != Done'
    )

    response = requests.post(
        f"{JIRA_URL}/rest/api/3/search/jql",
        json={
            "jql": jql,
            "fields": ["key"],
            "maxResults": 1
        },
        auth=AUTH,
        headers=HEADERS
    )

    response.raise_for_status()
    data = response.json()

    logger_utility().info(f"JQL response: {data}")

    issues = data.get("issues", [])
    if not issues:
        return None

    issue = issues[0]
    issue_key = issue.get("key")

    if not issue_key:
        logger_utility().warning(f"Issue found but no key field: {issue}")
        return None

    return issue_key


# --------------------------
# CREATE NEW ISSUE
# --------------------------
def create_issue(test_name, error, jira_project):
    """
    Create a new Jira bug issue with test name and error.
    Returns the new issue key.
    """
    # --------------------------
    # CONFIG
    # --------------------------
    JIRA_URL = os.getenv("JIRA_URL")
    PROJECT_KEY = os.getenv("JIRA_PROJECT")
    AUTH = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))

    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    url = f"{JIRA_URL}/rest/api/3/issue"

    payload = {"fields": {"project": {
        "key": f"{jira_project}"
    },
        "summary": f"Test failure: {test_name}",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Created via automation hook in conftest.py. {error}"
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "Bug"
        }
    }
    }

    r = requests.post(url, json=payload, auth=AUTH, headers=HEADERS)
    r.raise_for_status()
    return r.json()["key"]


# --------------------------
# GET OR CREATE ISSUE
# --------------------------
def get_or_create_issue(test_name, error, jira_project):
    """
    Returns existing issue key if found, otherwise creates a new issue.
    """
    existing = find_existing_issue(test_name)
    if existing:
        return existing
    return create_issue(test_name, error, jira_project)
