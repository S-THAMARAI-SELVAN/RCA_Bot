import sqlite3
import requests
import os

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

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1512739167703142521/38ii17ED1NNLF6hLB_VloLUfivYCDlk1doJDbkfqfiJBYsGJiBTq2qsQyk-kiPbSG_AX";

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
    print("❌ No RCA reports found in database")
    exit()

timestamp = row[0]
report = row[1]

# Discord message limit protection
message = f"""
🚨 CI/CD Pipeline Failure Alert 🚨

Timestamp:
{timestamp}

{report[:1800]}
"""

payload = {
    "content": message
}

response = requests.post(
    DISCORD_WEBHOOK_URL,
    json=payload
)

if response.status_code == 204:
    print("✅ Discord Alert Sent Successfully")
else:
    print("❌ Failed to send Discord Alert")
    print(response.text)