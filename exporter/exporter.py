#!/usr/bin/env python3

import os
import re
import string
import time

from gsheets import (
    insert_row,
    setup_gspread_worksheet,
    write_header_row,
)
from jira import get_project_issues

HEADER_ROW_COLUMNS = [
    "Issue", "Summary", "Team", "Type", "Story Points", "Business Value",
    "Status", "Creator", "Assignee", "Sprint", "Date Created",
    "Date Last Status Change", "Link",
]
JIRA_PROJECT_NAME = os.environ.get("JIRA_PROJECT_NAME")


def build_range(row_number, column_count, row_count):
    return "A{0}:{1}{2}".format(
        row_number,
        string.ascii_uppercase[column_count-1],
        row_count,
    )


def update_jira_data(worksheet, issues):
    print("Updating Jira data..")
    column_count = len(HEADER_ROW_COLUMNS)
    cell_range = build_range(2, column_count, len(issues))
    cell_list = worksheet.range(cell_range)
    for i in range(0, len(issues)-1):
        # Issue key
        cell_list[i*column_count].value = issues[i]["key"]
        # Issue title
        cell_list[i*column_count+1].value = issues[i]["fields"]["summary"]
        # Team
        if issues[i]["fields"]["customfield_13805"]:
            cell_list[i*column_count+2].value = (
                issues[i]["fields"]["customfield_13805"]["value"]
            )
        else:
            cell_list[i*column_count+2].value = ""
        # Type
        if (
            "customfield_13919" in issues[i]["fields"] and
            issues[i]["fields"]["customfield_13919"]
        ):
            cell_list[i*column_count+3].value = (
                issues[i]["fields"]["customfield_13919"]["value"]
            )
        else:
            cell_list[i*column_count+3].value = ""
        # Story points
        if (
            "customfield_10013" in issues[i]["fields"] and
            issues[i]["fields"]["customfield_10013"]
        ):
            cell_list[i*column_count+4].value = (
                issues[i]["fields"]["customfield_10013"]
            )
        else:
            cell_list[i*column_count+4].value = ""
        # Business value
        if (
            "customfield_13920" in issues[i]["fields"] and
            issues[i]["fields"]["customfield_13920"]
        ):
            cell_list[i*column_count+5].value = (
                issues[i]["fields"]["customfield_13920"]["value"]
            )
        else:
            cell_list[i*column_count+5].value = ""
        # Status
        cell_list[i*column_count+6].value = (
            issues[i]["fields"]["status"]["statusCategory"]["name"]
        )
        # Creator
        cell_list[i*column_count+7].value = (
            issues[i]["fields"]["creator"]["displayName"]
        )
        # Assignee
        if issues[i]["fields"]["assignee"]:
            cell_list[i*column_count+8].value = (
                issues[i]["fields"]["assignee"]["displayName"]
            )
        else:
            cell_list[i*column_count+8].value = ""
        # Sprint
        cell_list[i*column_count+9].value = ""
        if issues[i]["fields"]["customfield_10560"]:
            match = re.search(
                r"name=([A-Za-z0-9 _#-]*)",
                issues[i]["fields"]["customfield_10560"][0],
            )
            if match:
                cell_list[i*column_count+9].value = match.group(1)
        # Date created
        cell_list[i*column_count+10].value = issues[i]["fields"]["created"]
        # Date last status change
        cell_list[i*column_count+11].value = (
            issues[i]["fields"]["statuscategorychangedate"]
        )
        # Link
        cell_list[i*column_count+12].value = (
            "{base_url}/browse/{issue_id}"
        ).format(
            base_url=issues[i]["self"].split("/rest")[0],
            issue_id=issues[i]["key"],
        )
    worksheet.update_cells(cell_list)


def main():
    issues = get_project_issues(JIRA_PROJECT_NAME)
    worksheet = setup_gspread_worksheet()
    write_header_row(worksheet, HEADER_ROW_COLUMNS)
    update_jira_data(worksheet, issues)


def handler(event, context):
    main()


if __name__ == "__main__":
    main()
