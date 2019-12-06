import base64
import json
import os
from urllib.request import Request, urlopen


JIRA_API_EMAIL = os.environ.get("JIRA_API_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_API_BASE_URL = os.environ.get("JIRA_API_BASE_URL")
JIRA_API_PAGE_SIZE = int(os.environ.get("JIRA_API_PAGE_SIZE", 100))
JIRA_MAX_ISSUES_TO_FETCH = int(
    os.environ.get("JIRA_MAX_ISSUES_TO_FETCH", 1000)
)


def get_project_issues(jira_project_id):
    print("Looking up project issues for {}".format(jira_project_id))
    jira_auth = "{api_email}:{api_token}".format(
        api_email=JIRA_API_EMAIL, api_token=JIRA_API_TOKEN
    )
    jira_auth_base64 = base64.b64encode(jira_auth.encode("utf-8")).decode(
        "utf-8"
    )
    headers = {"Authorization": "Basic {}".format(jira_auth_base64)}
    all_issues = []
    page_number = 0
    total_issue_count = None
    while True:
        url = (
            "https://{base_url}/rest/api/2/search?jql=project={id}"
            "&maxResults={page_size}"
            "&startAt={start_at}"
        ).format(
            base_url=JIRA_API_BASE_URL,
            id=jira_project_id,
            page_size=JIRA_API_PAGE_SIZE,
            start_at=page_number * JIRA_API_PAGE_SIZE,
        )
        req = Request(url, headers=headers)
        response = urlopen(req)
        response_dict = json.loads(response.read())
        if not total_issue_count:
            total_issue_count = response_dict["total"]
        all_issues.extend(response_dict["issues"])
        if (page_number + 1) * JIRA_API_PAGE_SIZE >= JIRA_MAX_ISSUES_TO_FETCH:
            print(
                "First {} issues successfully fetched".format(
                    JIRA_MAX_ISSUES_TO_FETCH,
                )
            )
            break
        if (page_number + 1) * JIRA_API_PAGE_SIZE >= total_issue_count:
            print(
                "All ({}) issues successfully fetched".format(len(all_issues))
            )
            break
        page_number += 1
    print("Total issues loaded:", len(all_issues))
    return all_issues
