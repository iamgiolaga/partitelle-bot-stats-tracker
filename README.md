# Partitelle Bot Stats Tracker

Cron job that collects statistics from the [partitelle-bot](https://github.com/iamgiolaga/partitelle-bot) database and writes them to Google Sheets.

## What it does

- Counts **active matches** (rows in the main table)
- Counts **total users** (rows in the `all_players` table)
- Appends a row with a timestamp to Google Sheets on each run

## Environment Variables

### Database (same as partitelle-bot)

| Variable           | Description        |
| ------------------ | ------------------ |
| `PB_DB_HOST`       | PostgreSQL host    |
| `PB_DB_NAME`       | Database name      |
| `PB_DB_USER`       | Database user      |
| `PB_DB_PASSWORD`   | Database password  |
| `PB_DB_PORT`       | Database port      |
| `PB_DB_TABLE_NAME` | Matches table name |

### Google Sheets

| Variable                  | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `GOOGLE_CREDENTIALS_JSON` | Full Service Account JSON (as a string)        |
| `SPREADSHEET_NAME`        | Spreadsheet name                               |
| `SHEET_TAB`               | Sheet tab name                                 |

## Deploy with GitHub Actions

The workflow runs daily at 10:00 CEST via `.github/workflows/daily-stats.yml`. You can also trigger it manually from the Actions tab.

### Setup

1. Go to the repo on GitHub → **Settings → Secrets and variables → Actions**
2. Add the following **Repository secrets**:
   - `PB_DB_HOST`
   - `PB_DB_NAME`
   - `PB_DB_USER`
   - `PB_DB_PASSWORD`
   - `PB_DB_PORT`
   - `PB_DB_TABLE_NAME`
   - `GOOGLE_CREDENTIALS_JSON` (paste the full Service Account JSON)
3. Push to `main` and the workflow will run on schedule

## Google Sheets Setup

See the dedicated section in the README or ask Copilot for a step-by-step guide.
