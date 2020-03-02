#!/usr/bin/env python3

import datetime
import os
from pathlib import Path
import re
import string
import time
import yaml

from gsheets import (
    insert_row,
    setup_gspread_worksheet,
    write_header_row,
)
from jira import get_project_issues


def build_range(row_number, column_count, row_count):
    return "A{0}:{1}{2}".format(
        row_number, string.ascii_uppercase[column_count - 1], row_count,
    )


def print_date_google_sheets(jira_date_string):
    datetime_parsed = datetime.datetime.strptime(
        jira_date_string, "%Y-%m-%dT%H:%M:%S.%f%z",
    )
    return datetime_parsed.strftime("%m/%d/%Y %H:%M:%S")


def update_jira_data(config, worksheet, issues):
    print("Updating Jira data..")
    column_count = len(config["report_columns"])
    cell_range = build_range(2, column_count, len(issues))
    cell_list = worksheet.range(cell_range)
    for i in range(0, len(issues) - 1):
        # Issue key
        cell_list[i * column_count].value = issues[i]["key"]
        # Issue title
        cell_list[i * column_count + 1].value = issues[i]["fields"]["summary"]
        # Team
        if issues[i]["fields"]["customfield_13805"]:
            cell_list[i * column_count + 2].value = issues[i]["fields"][
                "customfield_13805"
            ]["value"]
        else:
            cell_list[i * column_count + 2].value = ""
        # Issue Type
        cell_list[i * column_count + 3].value = issues[i]["fields"][
            "issuetype"
        ]["name"]
        # Type
        if (
            "customfield_13919" in issues[i]["fields"]
            and issues[i]["fields"]["customfield_13919"]
        ):
            cell_list[i * column_count + 4].value = issues[i]["fields"][
                "customfield_13919"
            ]["value"]
        else:
            cell_list[i * column_count + 4].value = ""
        # Story points
        if (
            "customfield_10013" in issues[i]["fields"]
            and issues[i]["fields"]["customfield_10013"]
        ):
            cell_list[i * column_count + 5].value = issues[i]["fields"][
                "customfield_10013"
            ]
        else:
            cell_list[i * column_count + 5].value = ""
        # Business value
        if (
            "customfield_13920" in issues[i]["fields"]
            and issues[i]["fields"]["customfield_13920"]
        ):
            cell_list[i * column_count + 6].value = issues[i]["fields"][
                "customfield_13920"
            ]["value"]
        else:
            cell_list[i * column_count + 6].value = ""
        # Status
        cell_list[i * column_count + 7].value = issues[i]["fields"]["status"][
            "statusCategory"
        ]["name"]
        # Creator
        cell_list[i * column_count + 8].value = issues[i]["fields"]["creator"][
            "displayName"
        ]
        # Assignee
        if issues[i]["fields"]["assignee"]:
            cell_list[i * column_count + 9].value = issues[i]["fields"][
                "assignee"
            ]["displayName"]
        else:
            cell_list[i * column_count + 9].value = ""
        # Sprint
        cell_list[i * column_count + 10].value = ""
        if issues[i]["fields"]["customfield_10560"]:
            match = re.search(
                r"name=([A-Za-z0-9 _#-]*)",
                issues[i]["fields"]["customfield_10560"][0],
            )
            if match:
                cell_list[i * column_count + 10].value = match.group(1)
        # Date created
        cell_list[i * column_count + 11].value = print_date_google_sheets(
            issues[i]["fields"]["created"]
        )
        # Date last status change
        cell_list[i * column_count + 12].value = print_date_google_sheets(
            issues[i]["fields"]["statuscategorychangedate"]
        )
        # Link
        cell_list[i * column_count + 13].value = (
            "{base_url}/browse/{issue_id}"
        ).format(
            base_url=issues[i]["self"].split("/rest")[0],
            issue_id=issues[i]["key"],
        )
    worksheet.update_cells(cell_list, value_input_option="USER_ENTERED")


def load_config():
    config_path = "{}/config.yml".format(Path(__file__).parent.absolute())
    with open(config_path, "r") as stream:
        return yaml.safe_load(stream)


def main():
    config = load_config()
    issues = get_project_issues(
        config["jira"]["project_name"],
        config["jira"]["base_url"],
        config["jira"]["max_issues_to_fetch"],
    )
    worksheet = setup_gspread_worksheet(
        config["google_sheets"]["sheet_name"],
        config["google_sheets"]["tab_name"],
    )
    write_header_row(worksheet, config["report_columns"])
    update_jira_data(config, worksheet, issues)


def handler(event, context):
    main()


if __name__ == "__main__":
    main()
