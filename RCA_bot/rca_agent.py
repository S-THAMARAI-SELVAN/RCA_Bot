import os
import subprocess
from datetime import datetime
import google.generativeai as genai

# ==========================================
# GEMINI CONFIG
# ==========================================

genai.configure(
    api_key="AQ.Ab8RN6Lek_L9gZDoUHsfVOhKjKzB05-vhH26nwWLy7p0VJB6eA"
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

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

os.makedirs(
    os.path.join(BASE_DIR, "logs"),
    exist_ok=True
)

os.makedirs(
    os.path.join(BASE_DIR, "reports"),
    exist_ok=True
)

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
# GIT DIFF
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
# GEMINI ANALYSIS
# ==========================================

try:

    print("\nSending data to Gemini...\n")

    response = model.generate_content(prompt)

    rca_output = response.text

    print("Gemini Response Received\n")

except Exception as e:

    rca_output = f"""
Gemini Analysis Failed

Reason:
{str(e)}
"""

# ==========================================
# REPORT
# ==========================================

report = f"""
=================================================
      CI/CD PIPELINE FAILURE RCA REPORT
=================================================

Generated Time:
{datetime.now()}

{rca_output}

=================================================
"""

# ==========================================
# SAVE REPORT
# ==========================================

print("Writing report to:")
print(REPORT_FILE)

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(report)

print("Report Saved Successfully")

# Verify save

with open(
    REPORT_FILE,
    "r",
    encoding="utf-8"
) as f:

    saved_report = f.read()

print("\n===== SAVED REPORT =====\n")
print(saved_report)
print("\n========================\n")