import os
import json
from datetime import datetime

import psycopg2
from psycopg2 import sql
import gspread
from google.oauth2.service_account import Credentials


def get_db_stats():
    conn = psycopg2.connect(
        host=os.environ["PB_DB_HOST"],
        database=os.environ["PB_DB_NAME"],
        user=os.environ["PB_DB_USER"],
        password=os.environ["PB_DB_PASSWORD"],
        port=os.environ["PB_DB_PORT"],
    )
    cur = conn.cursor()
    table_name = os.environ["PB_DB_TABLE_NAME"]

    # Number of active matches (rows in the main table)
    cur.execute(
        sql.SQL("SELECT COUNT(*) FROM {}").format(
            sql.Identifier(table_name)
        )
    )
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
