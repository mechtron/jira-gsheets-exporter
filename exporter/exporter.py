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


def convert_to_gsheets_friendly_date(jira_date_string):
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
        current_column = 0
        for column in config["report_columns"]:
            value = ""
            if column["type"] == "key":
                value = issues[i][column["key"]]

            elif column["type"] == "field":
                # Custom field support:
                if "customfield_" in column["field_name"]:
                    if (
                        column["field_name"] in issues[i]["fields"]
                        and issues[i]["fields"][column["field_name"]]
                    ):
                        value = issues[i]["fields"][column["field_name"]]
                        if hasattr(value, "__contains__") and "value" in value:
                            value = value["value"]
                # Nested key support:
                elif "." in column["field_name"]:
                    keys = column["field_name"].split(".")
                    value = issues[i]["fields"][keys[0]]
                    if value:
                        for key in keys[1:]:
                            value = value[key]
                else:
                    value = issues[i]["fields"][column["field_name"]]

            elif column["type"] == "issue_link":
                value = "{base_url}/browse/{issue_id}".format(
                    base_url=issues[i]["self"].split("/rest")[0],
                    issue_id=issues[i]["key"],
                )

            # Feature: Regex capture
            if "regex_capture" in column and value != "":
                if isinstance(value, list):
                    value = value[0]
                match = re.search(
                    r"{}".format(column["regex_capture"]), value,
                )
                if match:
                    value = match.group(1)

            # Feature: Date formatter
            if "date_formatter" in column and value != "":
                if column["date_formatter"] == "google_sheets":
                    value = convert_to_gsheets_friendly_date(value)
                else:
                    exit(
                        "Unknown date_formatter {}".format(
                            column["date_formatter"]
                        )
                    )

            cell_list[i * column_count + current_column].value = value
            current_column += 1

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
