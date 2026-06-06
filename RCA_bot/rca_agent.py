import os
import subprocess
from datetime import datetime
import google.generativeai as genai

# ==========================================
# GEMINI CONFIG
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set"
    )

genai.configure(api_key=api_key)

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

# ==========================================
# FILE PATHS
# ==========================================

FAILURE_LOG = os.path.join(BASE_DIR, "logs", "failure.log")
SUCCESS_LOG = os.path.join(BASE_DIR, "logs", "success.log")
GIT_DIFF_LOG = os.path.join(BASE_DIR, "logs", "git_diff.log")
REPORT_FILE = os.path.join(BASE_DIR, "reports", "rca_report.txt")

os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)

# ==========================================
# READ LOGS
# ==========================================

failure_log = "No failure log found"
if os.path.exists(FAILURE_LOG):
    with open(FAILURE_LOG, "r", encoding="utf-8") as f:
        failure_log = f.read()

success_log = "No success log found"
if os.path.exists(SUCCESS_LOG):
    with open(SUCCESS_LOG, "r", encoding="utf-8") as f:
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

    with open(GIT_DIFF_LOG, "w", encoding="utf-8") as f:
        f.write(git_diff)

except Exception as e:
    git_diff = f"Unable to retrieve git diff\n\nReason:\n{str(e)}"

# ==========================================
# PROMPT
# ==========================================

prompt = f"""
You are a Senior DevOps Root Cause Analysis Agent.

Analyze the following information.

CURRENT FAILURE LOG:
{failure_log}

LAST SUCCESSFUL RUN LOG:
{success_log}

RECENT GIT DIFF:
{git_diff}

Generate a professional RCA report.

Provide:
1. Root Cause
2. Why Previous Run Succeeded
3. Did Recent Code Changes Cause Failure?
4. Recommendation
5. Retry Recommended (YES/NO)
6. Confidence Score (%)
"""

# ==========================================
# GEMINI ANALYSIS
# ==========================================

try:
    response = model.generate_content(prompt)
    rca_output = response.text

except Exception as e:
    rca_output = f"Gemini Analysis Failed\n\nReason:\n{str(e)}"

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

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(report)

print("Report saved:", REPORT_FILE)