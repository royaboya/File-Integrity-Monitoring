# File Integrity Monitoring (FIM)

A command-line File Integrity Monitoring tool written in Python. It records a SHA-256 hash of every file in a set of directories (the **baseline**), stores those hashes in PostgreSQL, and later re-scans the same directories to detect files whose contents have changed. Mismatches are logged, summarized in a report, and emailed to you.

The default configuration targets Windows system directories (`C:/Windows` and `C:/Windows/System32`), but any directory can be monitored.

## How it works

1. **Baseline** – `generate-baseline` hashes each file and saves `(filepath, sha256)` pairs to a PostgreSQL table, replacing any previous baseline.
2. **Scan** – `scan` re-hashes the same files and compares each hash to the stored baseline. Any difference is reported as a mismatch.
3. **Alert** – at the end of a scan, an email listing every mismatched file path is sent through Gmail SMTP. Use `-r` to also print a summary report to the terminal.

> Run `generate-baseline` on a system you trust to be clean. The baseline is only as good as the state of the files when it was taken.

## Requirements

- Python 3.8 or newer
- A running PostgreSQL server
- A Gmail account with an [app password](https://support.google.com/accounts/answer/185833) (for email alerts)
- Python packages:

```bash
pip install pyyaml python-dotenv psycopg2-binary requests splunk-sdk
```

> `requirements.txt` in the repo does not yet list these packages, so install them manually as above. `splunk-sdk` is needed because `alerts.py` imports it at startup, even though the CLI does not currently send anything to Splunk.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/royaboya/File-Integrity-Monitoring.git
cd File-Integrity-Monitoring
```

### 2. Create the database table

The tool connects to PostgreSQL using the host, port, user, and password below and uses that user's default database. Create the table there:

```sql
CREATE TABLE IF NOT EXISTS file_hashes_table (
    id SERIAL PRIMARY KEY,
    filepath TEXT UNIQUE NOT NULL,
    filehash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Create a `.env` file

Create a file named `.env` in the project root (do not commit it):

```env
# PostgreSQL
HOST=localhost
PGSQL_PORT=5432
PGSQL_USER=your_postgres_user
PGSQL_PW=your_postgres_password

# Email alerts (Gmail)
GMAIL_SMTP_FROM=you@gmail.com
GMAIL_SMTP=your_gmail_app_password
GMAIL_SMTP_TO=recipient@example.com

# Splunk (loaded by config.py; not used by the CLI yet)
SPLUNK_USER=
SPLUNK_PW=
SPLUNK_HEC_TOKEN=
```

| Variable | Purpose |
| --- | --- |
| `HOST`, `PGSQL_PORT`, `PGSQL_USER`, `PGSQL_PW` | PostgreSQL connection. `PGSQL_PORT` is required and must be a number. |
| `GMAIL_SMTP_FROM` | Gmail address the alert is sent from and logged in with. |
| `GMAIL_SMTP` | The Gmail **app password** for that account (not your normal password). |
| `GMAIL_SMTP_TO` | Address that receives alerts. |
| `SPLUNK_USER`, `SPLUNK_PW`, `SPLUNK_HEC_TOKEN` | Splunk credentials for the alert helpers in `alerts.py`. Not called by the CLI yet. |

### 4. Choose what to monitor

Edit `config.yaml` and list the directories to scan:

```yaml
system_paths_to_scan:
  - "C:/Windows/System32"
  - "C:/Windows"
```

Only files directly inside each listed directory are hashed; subdirectories are not descended into. On Windows, run your terminal as Administrator so protected files can be read. Files that cannot be read are recorded with the hash value `ERROR`.

## Usage

The tool must be run **from the `src/fim` directory**, because the config and log paths are relative to it.

```bash
cd src/fim
```

**Create (or replace) the baseline**

```bash
python main.py generate-baseline
```

This clears the existing baseline table, then hashes every file in the configured directories and stores the results.

**Scan for changes**

```bash
python main.py scan
```

Prints `MISMATCH FOUND: <path>` for each file whose hash differs from the baseline, then sends the email alert.

**Scan and print a summary report**

```bash
python main.py -r scan
```

The `-r` flag goes **before** the subcommand. The report shows the number of scan errors and the number of baseline mismatches.

**Command reference**

| Command / flag | Description |
| --- | --- |
| `generate-baseline` | Creates a new baseline from the directories in `config.yaml`, replacing the old one. |
| `scan` | Compares current file hashes to the baseline. |
| `scan -d` / `scan --deep` | Deep-scan flag. Currently only prints a banner; scanning is not yet recursive. |
| `-r` | Print a report summary after the command finishes. |
| `-h` | Show help. |

## Logs

Logs are written to the `logs/` directory using rotating files (5 MB each, 2 backups kept):

- `logs/info.log` – informational messages and above
- `logs/errors.log` – errors only

## Project structure

```
File-Integrity-Monitoring/
├── config.yaml            # Directories to scan
├── requirements.txt       # Dependency list (incomplete, see Requirements)
├── logs/                  # Rotating log output
└── src/fim/
    ├── main.py            # Entry point; sets up logging and starts the CLI
    ├── cli.py             # Argument parsing and subcommands
    ├── monitor.py         # Baseline generation and scan logic
    ├── hash_utils.py      # Chunked SHA-256 / SHA-512 file hashing
    ├── db.py              # PostgreSQL access for the baseline table
    ├── alerts.py          # Mismatch tracking, email alerts, Splunk helpers
    ├── config.py          # Loads .env values and config.yaml
    └── logger.py          # Rotating file log setup
```

## Known limitations

 Current gaps, although this is more of a PoC project:

- **Not recursive.** Only files directly inside each configured directory are checked.
- **Files missing from the baseline** are counted as errors and also reported as mismatches.
- **An email is attempted at the end of every scan**, even when nothing changed. If email is not configured, the failure is printed and the scan otherwise completes.
- **Splunk alerting** (`create_splunk_alert`) is a stub and is not wired into the CLI.
- **Database setup helpers** (`create_and_verify_db`, `create_and_verify_table`) are not called automatically, so the table must be created manually as shown above.
