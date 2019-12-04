import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


GOOGLE_SERVICE_CREDS_JSON = os.environ.get("GOOGLE_SERVICE_CREDS_JSON")
GOOGLE_SHEET_NAME = os.environ.get("GOOGLE_SHEET_NAME")
GOOGLE_SHEET_TAB_NAME = os.environ.get("GOOGLE_SHEET_TAB_NAME")


def setup_gspread_worksheet():
    print("Authorizing gspread..")
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(GOOGLE_SERVICE_CREDS_JSON),
        scopes=scope,
    )
    gc = gspread.authorize(credentials)
    sh = gc.open(GOOGLE_SHEET_NAME)
    return sh.worksheet(GOOGLE_SHEET_TAB_NAME)


def write_header_row(worksheet, column_names):
    print("Updating the header row..")
    row = 1
    column = 1
    for key in column_names:
        worksheet.update_cell(row, column, key)
        column+=1


def append_row(worksheet, row):
    worksheet.append_row(row)


def insert_row(worksheet, row, row_number):
    worksheet.insert_row(row, row_number)


def update_cell(worksheet, column, row, new_value):
    worksheet.update_cell(row, column, new_value)
