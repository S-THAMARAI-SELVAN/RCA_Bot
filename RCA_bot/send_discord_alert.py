import sqlite3
import requests
import os
import sys

## Force UTF-8 output (extra safety)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_FILE = os.path.join(
    BASE_DIR,
    "database",
    "rca.db"
)

# Store this in Jenkins credentials or environment variables in production
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1512739167703142521/38ii17ED1NNLF6hLB_VloLUfivYCDlk1doJDbkfqfiJBYsGJiBTq2qsQyk-kiPbSG_AX";


try:
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        timestamp,
        rca_report
    FROM pipeline_failures
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row is None:
        print("[ERROR] No RCA reports found in database")
        sys.exit(1)

    timestamp = row[0]
    report = row[1]

    # Discord message limit is 2000 characters
    message = f"""
CI/CD PIPELINE FAILURE ALERT

Timestamp:
{timestamp}

RCA Report:
{report[:1800]}
"""

    payload = {
        "content": message
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=30
    )

    if response.status_code == 204:
        print("[SUCCESS] Discord Alert Sent Successfully")
    else:
        print(f"[ERROR] Discord API returned status code: {response.status_code}")
        print(response.text)
        sys.exit(1)

except sqlite3.Error as e:
    print(f"[ERROR] Database Error: {e}")
    sys.exit(1)

except requests.exceptions.RequestException as e:
    print(f"[ERROR] Discord Request Failed: {e}")
    sys.exit(1)

except Exception as e:
    print(f"[ERROR] Unexpected Error: {e}")
    sys.exit(1)