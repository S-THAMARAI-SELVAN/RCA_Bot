import os
import subprocess
import sqlite3
import ollama
from datetime import datetime
from db import save_failure
# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

print("Current Working Directory:")
print(os.getcwd())

print("Base Directory:")
print(BASE_DIR)

# ==========================================
# FILE PATHS
# ==========================================

FAILURE_LOG = os.path.join(
    BASE_DIR,
    "logs",
    "failure.log"
)

SUCCESS_LOG = os.path.join(
    BASE_DIR,
    "logs",
    "success.log"
)

GIT_DIFF_LOG = os.path.join(
    BASE_DIR,
    "logs",
    "git_diff.log"
)

REPORT_FILE = os.path.join(
    BASE_DIR,
    "reports",
    "rca_report.txt"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "rca.db"
)

os.makedirs(
    os.path.join(BASE_DIR, "logs"),
    exist_ok=True
)

os.makedirs(
    os.path.join(BASE_DIR, "reports"),
    exist_ok=True
)

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect(DATABASE_FILE)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rca_reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    report TEXT
)
""")

conn.commit()

# ==========================================
# READ FAILURE LOG
# ==========================================

failure_log = "No failure log found"

if os.path.exists(FAILURE_LOG):

    with open(
        FAILURE_LOG,
        "r",
        encoding="utf-8"
    ) as f:

        failure_log = f.read()

# ==========================================
# READ SUCCESS LOG
# ==========================================

success_log = "No success log found"

if os.path.exists(SUCCESS_LOG):

    with open(
        SUCCESS_LOG,
        "r",
        encoding="utf-8"
    ) as f:

        success_log = f.read()

# ==========================================
# GET GIT DIFF
# ==========================================

try:

    git_diff = subprocess.check_output(
        "git diff HEAD~1 HEAD",
        shell=True,
        text=True,
        stderr=subprocess.STDOUT,
        cwd=BASE_DIR
    )

    with open(
        GIT_DIFF_LOG,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(git_diff)

except Exception as e:

    git_diff = f"""
Unable to retrieve git diff

Reason:
{str(e)}
"""

# ==========================================
# PROMPT
# ==========================================

prompt = f"""
You are a Senior DevOps Root Cause Analysis Agent.

Analyze the following information.

==================================
CURRENT FAILURE LOG
==================================

{failure_log}

==================================
LAST SUCCESSFUL RUN LOG
==================================

{success_log}

==================================
RECENT GIT DIFF
==================================

{git_diff}

Generate a professional RCA report.

Provide:

1. Root Cause
2. Why Previous Run Succeeded
3. Did Recent Code Changes Cause Failure?
4. Recommendation
5. Retry Recommended (YES/NO)
6. Confidence Score (%)

Keep the response concise and professional.
"""

# ==========================================
# OLLAMA ANALYSIS
# ==========================================

try:

    print("\nSending data to Ollama...\n")

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    rca_output = response["message"]["content"]

    print("Ollama Response Received\n")

except Exception as e:

    rca_output = f"""
Ollama Analysis Failed

Reason:
{str(e)}
"""

# ==========================================
# REPORT
# ==========================================

timestamp = str(datetime.now())

report = f"""
=================================================
      CI/CD PIPELINE FAILURE RCA REPORT
=================================================

Generated Time:
{timestamp}

{rca_output}

=================================================
"""

# ==========================================
# SAVE REPORT FILE
# ==========================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(report)

print("Report Saved Successfully")

# ==========================================
# SAVE TO SQLITE
# ==========================================

save_failure(
    timestamp,
    failure_log,
    success_log,
    git_diff,
    report
)

conn.commit()

conn.close()

print("Report Stored In SQLite")

# ==========================================
# DISPLAY REPORT
# ==========================================

print("\n===== RCA REPORT =====\n")

print(report)

print("\n======================\n")