import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


GOOGLE_SERVICE_CREDS_JSON = os.environ.get("GOOGLE_SERVICE_CREDS_JSON")


def setup_gspread_worksheet(sheet_name, sheet_tab_name):
    print("Authorizing gspread..")
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(GOOGLE_SERVICE_CREDS_JSON), scopes=scope,
    )
    gc = gspread.authorize(credentials)
    sh = gc.open(sheet_name)
    return sh.worksheet(sheet_tab_name)


def write_header_row(worksheet, report_columns):
    print("Updating the header row..")
    row = 1
    column = 1
    for key in report_columns:
        worksheet.update_cell(row, column, key["column_name"])
        column += 1


def append_row(worksheet, row):
    worksheet.append_row(row, value_input_option="USER_ENTERED")


def insert_row(worksheet, row, row_number):
    worksheet.insert_row(row, row_number, value_input_option="USER_ENTERED")


def update_cell(worksheet, column, row, new_value):
    worksheet.update_cell(row, column, new_value)
