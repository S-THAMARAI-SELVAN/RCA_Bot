import os
import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1512739167703142521/38ii17ED1NNLF6hLB_VloLUfivYCDlk1doJDbkfqfiJBYsGJiBTq2qsQyk-kiPbSG_AX"

report_path = os.path.join("..", "reports", "rca_report.txt")

if not os.path.exists(report_path):
    print("❌ RCA report not found at:", report_path)
    exit()

with open(report_path, "r", encoding="utf-8") as f:
    report = f.read()

payload = {
    "content": "🚨 **CI/CD Pipeline Failure Alert** 🚨\n\n" + report
}

response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

if response.status_code == 204:
    print("✅ Discord Alert Sent Successfully")
else:
    print("❌ Failed to send Discord alert")
    print(response.text)