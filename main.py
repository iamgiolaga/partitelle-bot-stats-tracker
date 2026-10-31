import os
import re
import json
from datetime import datetime

import psycopg2
import gspread
from google.oauth2.service_account import Credentials


def get_db_schema():
    # Empty (e.g. unset GitHub secret) falls back to the legacy "public" schema
    schema = os.environ.get("PB_DB_SCHEMA") or "public"
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", schema):
        raise ValueError(
            f"Invalid PB_DB_SCHEMA {schema!r}: must match ^[a-z_][a-z0-9_]*$"
        )
    return schema


def get_db_stats():
    schema = get_db_schema()
    conn = psycopg2.connect(
        host=os.environ["PB_DB_HOST"],
        database=os.environ["PB_DB_NAME"],
        user=os.environ["PB_DB_USER"],
        password=os.environ["PB_DB_PASSWORD"],
        port=os.environ["PB_DB_PORT"],
        options=f"-c search_path={schema}",
    )
    cur = conn.cursor()

    # Number of active matches (rows of the active_match view, resolved via search_path)
    cur.execute("SELECT COUNT(*) FROM active_match")
    active_matches = cur.fetchone()[0]

    cur.close()
    conn.close()

    return active_matches


def write_to_sheet(active_matches):
    creds_json = os.environ["GOOGLE_CREDENTIALS_JSON"]
    creds_dict = json.loads(creds_json)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(credentials)

    spreadsheet_name = os.environ.get("SPREADSHEET_NAME", "Projects Tracker")
    sheet_tab = os.environ.get("SHEET_TAB", "partitellebot")

    spreadsheet = gc.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(sheet_tab)

    # Add header if the sheet is empty
    if not worksheet.get_all_values():
        worksheet.append_row(["Date", "Stat"])

    now = datetime.now().strftime("%d/%m/%Y")
    worksheet.append_row([now, active_matches])
    print(f"[{now}] Active matches: {active_matches} — written to Google Sheets")


def main():
    active_matches = get_db_stats()
    write_to_sheet(active_matches)


if __name__ == "__main__":
    main()
