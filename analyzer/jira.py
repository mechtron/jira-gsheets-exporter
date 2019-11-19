import base64
import json
import math
import os
from urllib.request import Request, urlopen


JIRA_API_EMAIL = os.environ.get("JIRA_API_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_TICKETS_TO_ANALYZE = os.environ.get("JIRA_TICKETS_TO_ANALYZE", 1000)


def get_project_issues(jira_project_id):
    jira_auth = "{api_email}:{api_token}".format(
        api_email=JIRA_API_EMAIL, api_token=JIRA_API_TOKEN
    )
    jira_auth_base64 = base64.b64encode(jira_auth.encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic {}".format(jira_auth_base64)}
    all_issues = []
    page_size = 100
    for page_number in range(0, math.ceil(JIRA_TICKETS_TO_ANALYZE/page_size)):
        url = (
            "https://gumgum.jira.com/rest/api/2/search?jql=project={project_id}"
            "&maxResults={page_size}"
            "&startAt={start_at}"
        ).format(
            project_id=jira_project_id,
            page_size=page_size,
            start_at=(page_number-1)*page_size,
        )
        req = Request(url, headers=headers)
        response = urlopen(req)
        response_dict = json.loads(response.read())
        all_issues.extend(response_dict["issues"])
    for jira_issue in all_issues:
        print("Issue key:", jira_issue["key"])
        print("Summary:", jira_issue["fields"]["summary"])
        print("Description:", jira_issue["fields"]["description"])
        if jira_issue["fields"]["customfield_13805"]:
            print("Team:", jira_issue["fields"]["customfield_13805"]["value"])
        if jira_issue["fields"]["customfield_13919"]:
            print("Type:", jira_issue["fields"]["customfield_13919"]["value"])
        print("Status:", jira_issue["fields"]["status"]["statusCategory"]["name"])
        print("Link:", jira_issue["self"])
        print("")
    print("Total count:", len(all_issues))
    return all_issues
