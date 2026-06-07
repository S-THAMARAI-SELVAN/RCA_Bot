# 🤖 RCA Bot - AI-Powered DevOps Troubleshooting Recommendation [![GitHub](https://img.shields.io/badge/GitHub-RCA_Bot-blue?logo=github)](https://github.com/S-THAMARAI-SELVAN/RCA_Bot) [![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/) [![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?logo=jenkins)](https://www.jenkins.io/) [![License](https://img.shields.io/badge/License-MIT-green)]() **Automated Root Cause Analysis system** for CI/CD pipeline failures using AI-powered log analysis, git diff comparison, and intelligent remediation suggestions. ## 🎯 What It Does When a Jenkins pipeline fails, RCA Bot automatically: - 📊 **Analyzes** failure logs + success logs + recent git commits - 🧠 **Generates** AI-powered root cause analysis using Llama3 - 📝 **Produces** professional RCA reports with remediation steps - 💾 **Stores** all analyses for historical trending - 🔔 **Alerts** team via Discord with key insights **Business Impact:** Reduce debugging time from hours to minutes • Enable faster incident resolution • Empower on-call engineers --- ## 🏗️ System Architecture
mermaid
graph LR
    A["Jenkins Pipeline"] -->|Failure| B["RCA Agent"]
    B -->|Reads| C["Failure Logs"]
    B -->|Reads| D["Success Logs"]
    B -->|Executes| E["Git Diff"]
    C & D & E -->|Multi-source<br/>Analysis| F["Ollama/Llama3"]
    F -->|AI Processing| G["RCA Report"]
    G -->|Stores| H["SQLite DB"]
    H -->|Sends| I["Discord Alert"]
    I -->|Notifies| J["Team"]
    B -->|Validates| K["Website Files"]
**Key Flow:** Pipeline Failure → Collect Data (3 sources) → AI Analysis → Report + Alert --- ## 🚀 Features | Feature | Description | |---------|-------------| | **Multi-Source Analysis** | Combines failure logs + success logs + git changes | | **AI-Powered** | Uses Llama3 via Ollama for intelligent reasoning | | **Automated Validation** | Pre-deployment website integrity checks | | **Historical Tracking** | SQLite persistence for trend analysis | | **Real-time Alerts** | Discord notifications for instant team awareness | | **Retry Recommendations** | Suggests fixes with confidence scoring | | **Git Integration** | Analyzes recent code changes for context | --- ## 🛠️ Tech Stack - **Language:** Python 3.8+ - **CI/CD:** Jenkins (pipeline orchestration) - **AI Engine:** Ollama + Llama3 (local LLM inference) - **Database:** SQLite3 (persistent storage) - **Notifications:** Discord Webhooks - **Version Control:** Git - **Validation:** BeautifulSoup4 (HTML parsing) --- ## 📁 Project Structure
RCA_Bot/
├── RCA_bot/
│   ├── rca_agent.py           # Main orchestrator
│   ├── db.py                  # Database operations
│   ├── validator.py           # Pre-deployment checks
│   └── send_discord_alert.py  # Notification system
├── database/
│   └── rca.db                 # SQLite persistence
├── logs/
│   ├── failure.log            # Jenkins failures
│   ├── success.log            # Last successful run
│   └── git_diff.log           # Code changes
├── reports/
│   └── rca_report.txt         # Latest analysis
├── Jenkinsfile                # CI/CD pipeline
└── README.md
--- ## 📊 Workflow Diagram
mermaid
sequenceDiagram
    participant J as Jenkins
    participant A as RCA Agent
    participant O as Ollama
    participant D as Database
    participant DC as Discord
    
    J->>A: Pipeline Failed!
    A->>A: Read failure log
    A->>A: Read success log
    A->>A: Execute git diff
    A->>O: Send analysis request
    O->>O: Process with Llama3
    O->>A: Return analysis
    A->>D: Save to SQLite
    A->>DC: Send alert
    DC->>DC: Notify team
--- ## ⚡ Quick Start ### Prerequisites
bash
# Core requirements
- Python 3.8+
- Jenkins (with git)
- Ollama (with Llama3 model)
- Discord server & webhook URL
### Installation 1. **Clone Repository**
bash
   git clone https://github.com/S-THAMARAI-SELVAN/RCA_Bot.git
   cd RCA_Bot
2. **Install Python Dependencies**
bash
   pip install requests beautifulsoup4 ollama
3. **Verify Ollama Setup**
bash
   # Ensure Ollama running on localhost:11434
   ollama pull llama3
   curl http://localhost:11434/api/tags
4. **Configure Discord Webhook** - Create webhook in Discord server settings - Update webhook URL in RCA_bot/send_discord_alert.py 5. **Set Up Jenkins Integration** - Add repository to Jenkins - Configure Jenkinsfile - Add post-failure trigger:
groovy
     post {
         failure {
             bat 'python RCA_bot/rca_agent.py'
             bat 'python RCA_bot/send_discord_alert.py'
         }
     }
--- ## 📖 Usage ### Automated (Jenkins) RCA Bot runs automatically on pipeline failures and alerts team via Discord. ### Manual Execution
bash
# Run complete analysis
python RCA_bot/rca_agent.py

# Send alert
python RCA_bot/send_discord_alert.py

# Validate website
python RCA_bot/validator.py
### Query Historical Data
python
import sqlite3

conn = sqlite3.connect("database/rca.db")
cursor = conn.cursor()
cursor.execute("SELECT timestamp, rca_report FROM pipeline_failures ORDER BY id DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}\n")
--- ## 🔍 Sample RCA Output
ROOT CAUSE ANALYSIS REPORT
Generated: 2024-06-06 10:35:22

FAILURE SUMMARY:
Database connection failed during deployment

ROOT CAUSE:
Recent commit changed DB_PASSWORD environment variable, but 
deployment script uses old configuration.

IMPACT:
- Deploy stage failed
- Website unavailable for 12 minutes
- Affected: Production environment

RECOMMENDATIONS:
1. Update environment variables in deployment config
2. Add environment variable validation step
3. Review credential management process

RETRY SUGGESTION:
✓ Run with updated environment variables
Confidence Score: 94%
--- ## 🎓 Learning Outcomes This project demonstrates: - ✅ **DevOps Automation** - Jenkins pipeline integration - ✅ **AI Integration** - Local LLM for intelligent analysis - ✅ **Database Design** - SQLite schema for analytics - ✅ **System Architecture** - Multi-component orchestration - ✅ **Python Excellence** - Production-grade scripting - ✅ **Problem Solving** - Intelligent automation for complex problems --- ## 🚧 Future Enhancements - [ ] Web dashboard for RCA history visualization - [ ] Slack/Teams integration alongside Discord - [ ] ML-based failure prediction - [ ] Advanced metrics & trending dashboard - [ ] Email notifications for critical failures - [ ] Custom AI prompts per team - [ ] PagerDuty integration for on-call alerts - [ ] Automated remediation actions --- ## 💼 For Recruiters & Interviewers **Key Technical Achievements:** 1. **Multi-threaded Analysis** - Parallel log processing 2. **LLM Integration** - Localhost Ollama for cost-effective AI 3. **Event-Driven Architecture** - Jenkins webhooks trigger RCA 4. **Data Persistence** - SQLite for historical trending 5. **System Design** - Modular, maintainable Python code 6. **Automation** - Reduces debugging from hours to minutes **Business Value:**Reduces manual log analysis effort and accelerates CI/CD failure troubleshooting. --- ## 📚 Resources - [Ollama Documentation](https://ollama.ai) - [Llama3 Model](https://ollama.ai/library/llama3) - [Discord Webhooks](https://discord.com/developers/docs/resources/webhook) - [Jenkins CI/CD](https://www.jenkins.io/doc/) --- ## 📝 License MIT License - Feel free to fork and adapt for your organization --- ## 👨‍💻 About Built as an end-to-end DevOps solution demonstrating modern cloud automation, AI integration, and intelligent system design. **Questions?** Open an issue or reach out on GitHub!