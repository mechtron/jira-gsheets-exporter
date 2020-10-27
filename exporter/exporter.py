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


def regex_get_first_capture_group(input_string, regex):
    match = re.search(r"{}".format(regex), input_string)
    if match:
        return match.group(1)
    return None


def get_nested_value(data, nested_key, selector="first"):
    if selector not in ("first", "last"):
        exit("Unknown selector {}".format(column["selector"]))
    list_index_to_take = 0 if selector == "first" else -1
    keys = nested_key.split(".")
    value = data[keys[0]]
    if value:
        for key in keys[1:]:
            if isinstance(value, list):
                value = value[list_index_to_take][key]
            else:
                value = value[key]
    return value


def get_customfield_value(custom_field, custom_field_key):
    value = custom_field[custom_field_key]
    if hasattr(value, "__contains__") and "value" in value:
        value = value["value"]
    return value


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
                # Feature: customfield array item selector
                customfield_array_selector = "first"
                if "selector" in column:
                    customfield_array_selector = column["selector"]

                # Custom fields with nested keys support:
                if (
                    "customfield_" in column["field_name"] and
                    "." in column["field_name"]
                ):
                    value = get_nested_value(
                        issues[i]["fields"],
                        column["field_name"],
                        customfield_array_selector,
                    )

                # Custom field support:
                elif (
                    "customfield_" in column["field_name"] and
                    column["field_name"] in issues[i]["fields"]
                ):
                    value = get_customfield_value(issues[i]["fields"], column["field_name"])

                # Nested key support:
                elif "." in column["field_name"]:
                    value = get_nested_value(issues[i]["fields"], column["field_name"])

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
                    captured_values = []
                    for item in value:
                        captured_value = regex_get_first_capture_group(
                            item,
                            column["regex_capture"],
                        )
                        if captured_value:
                            captured_values.append(captured_value)
                    if len(captured_values) > 0:
                        if "regex_capture_sort" in column:
                            captured_values.sort()
                        if column["regex_capture_sort"] == "first":
                            value = captured_values[0]
                        if column["regex_capture_sort"] == "last":
                            value = captured_values[-1]
                else:
                    value = regex_get_first_capture_group(
                        value,
                        column["regex_capture"],
                    )

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

    # Blank null cells
    for cell in cell_list:
        if cell.value is None:
            cell.value = ""
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
