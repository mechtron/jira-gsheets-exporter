import base64
import json
import os
from urllib.request import Request, urlopen


JIRA_API_EMAIL = os.environ.get("JIRA_API_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_API_PAGE_SIZE = os.environ.get("JIRA_ISSUES_TO_ANALYZE", 100)
MAX_ISSUES_TO_FETCH = os.environ.get("JIRA_ISSUES_TO_ANALYZE", 1000)


def get_project_issues(jira_project_id):
    print("Looking up project issues for {}".format(jira_project_id))
    jira_auth = "{api_email}:{api_token}".format(
        api_email=JIRA_API_EMAIL, api_token=JIRA_API_TOKEN
    )
    jira_auth_base64 = (
        base64.b64encode(jira_auth.encode("utf-8")).decode("utf-8")
    )
    headers = {"Authorization": "Basic {}".format(jira_auth_base64)}
    all_issues = []
    page_number = 0
    total_issue_count = None
    while True:
        url = (
            "https://gumgum.jira.com/rest/api/2/search?jql=project={id}"
            "&maxResults={page_size}"
            "&startAt={start_at}"
        ).format(
            id=jira_project_id,
            page_size=JIRA_API_PAGE_SIZE,
            start_at=page_number*JIRA_API_PAGE_SIZE,
        )
        req = Request(url, headers=headers)
        response = urlopen(req)
        response_dict = json.loads(response.read())
        if not total_issue_count:
            total_issue_count = response_dict["total"]
        all_issues.extend(response_dict["issues"])
        if (page_number+1)*JIRA_API_PAGE_SIZE >= MAX_ISSUES_TO_FETCH:
            print(
                "First {} issues successfully fetched".format(
                    MAX_ISSUES_TO_FETCH,
                )
            )
            break
        if (page_number+1)*JIRA_API_PAGE_SIZE >= total_issue_count:
            print(
                "All ({}) issues successfully fetched".format(len(all_issues))
            )
            break
        page_number+=1
    print("Total issues loaded:", len(all_issues))
    return all_issues
