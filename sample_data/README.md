# Sample Data for RCA Bot

This folder contains sample data files that demonstrate how RCA Bot analyzes pipeline failures and generates root cause analysis reports.

## Contents

### 1. failure_log.txt
Sample Jenkins pipeline failure log showing:
- Build failure details
- Error stack trace
- Environment information
- Git information
- Impact assessment

**Scenario:** Database connection failure during production deployment

**Key Points:**
- Stage: Deploy
- Error Type: DatabaseConnectionError
- Severity: CRITICAL
- Downtime: 12 minutes

### 2. success_log.txt
Sample successful pipeline execution log showing:
- Complete build process (Build → Test → Deploy)
- All tests passed (45/45)
- Validation results
- Performance metrics
- Services status

**Scenario:** Previous successful deployment for comparison

**Key Points:**
- All stages completed successfully
- 92% code coverage
- Zero broken links
- Optimal performance metrics

### 3. git_diff.txt
Sample Git diff showing recent code changes between commits.

**Key Changes:**
- Modified database connection logic
- Updated environment variable references
- Changed DB_PASSWORD configuration
- Updated deployment script paths

**Files Changed:**
- deploy.py (deployment script)
- config/database.ini (configuration)
- Jenkinsfile (CI/CD pipeline)
- .env.example (environment template)

**Issue Introduced:**
Environment variable dependency without proper Jenkins credential setup

### 4. sample_rca_report.txt
Complete RCA Bot generated report analyzing the failure.

**Report Sections:**
- Executive Summary
- Root Cause Analysis (detailed explanation)
- Why Previous Build Succeeded
- Impact Assessment
- Remediation Steps (immediate, short-term, long-term)
- Retry Recommendation
- Lessons Learned
- Prevention Measures
- Follow-up Actions
- References
- Report Metadata

**Key Findings:**
- Primary Cause: Missing PROD_DB_PASSWORD environment variable
- Contributing Factors: 3 identified
- Confidence Score: 94%
- Estimated Revenue Impact: $2,500+

## How to Use This Sample Data

### For Testing RCA Bot

1. Copy failure_log.txt to `logs/failure.log`
2. Copy success_log.txt to `logs/success.log`
3. Copy git_diff.txt to `logs/git_diff.log`
4. Run RCA Agent:
   ```bash
   python RCA_bot/rca_agent.py
   ```
5. Compare generated report with sample_rca_report.txt

### For Demonstration

- Use these files to demonstrate RCA Bot capabilities to stakeholders
- Show how AI analysis identifies root causes
- Demonstrate multi-source investigation (failure + success + git)
- Highlight business value and impact assessment

### For Training

- Train team members on interpreting RCA reports
- Understand remediation steps and implementation
- Learn from lessons learned section
- Understand prevention measures

### For Documentation

- Reference example report format
- Show expected output structure
- Demonstrate report completeness
- Explain each section's purpose

## Analysis Scenario

**Situation:**
Production deployment fails due to missing environment variable

**Timeline:**
- 09:20:15 - Previous deployment succeeds (Build #2846)
- 09:45:30 - Code change committed (a1b2c3d)
- 10:35:22 - New deployment fails (Build #2847)
- 10:35:22 - RCA Report generated

**Root Cause:**
Missing PROD_DB_PASSWORD in Jenkins environment

**Resolution Time (Expected):**
- Identify cause: 1 minute (with RCA Bot)
- Fix credential: 2 minutes
- Verify fix: 3 minutes
- Redeploy: 5-10 minutes
- **Total: ~15 minutes**

**Without RCA Bot:**
- Manual log investigation: 30-60 minutes
- Engineer debugging: 30-45 minutes
- **Total: 1-2 hours**

**Time Saved: 75-80%**

## Key Insights from Sample Data

### Database Connection Failure Pattern

**Indicator 1:** Error type - DatabaseConnectionError
**Indicator 2:** Git diff shows environment variable change
**Indicator 3:** Missing credential in Jenkinsfile
**Conclusion:** Environment variable not configured

### Why AI Analysis Works

1. **Multi-Source Analysis**
   - Failure log shows what went wrong
   - Success log shows what worked before
   - Git diff shows what changed
   - Combined analysis reveals root cause

2. **Pattern Recognition**
   - AI identifies environment variable dependency
   - Links code change to deployment failure
   - Suggests specific remediation steps

3. **Business Context**
   - Calculates downtime impact
   - Estimates revenue loss
   - Prioritizes fixes by severity

## Customizing Sample Data

To create your own samples:

1. **Replace values:**
   - Timestamp: Update to current date/time
   - Build numbers: Use your pipeline's build numbers
   - Paths: Use your actual project paths
   - Metrics: Use your actual performance data

2. **Add variations:**
   - Different error types (timeout, permission denied, etc.)
   - Different git changes (code vs. config)
   - Different severity levels

3. **Generate from real incidents:**
   - Export actual logs from Jenkins
   - Extract real git commits
   - Use historical data for analysis

## Further Reading

- See README.md in parent directory for RCA Bot overview
- Check deployment guides in DEPLOYMENT_GUIDE.md
- Review troubleshooting in TECHNICAL_REFERENCE.md

## Questions?

For more information about RCA Bot, visit:
- GitHub: https://github.com/S-THAMARAI-SELVAN/RCA_Bot
- Discord: https://discord.gg/rvr6gyAt

---

**Last Updated:** June 2024
**Sample Data Version:** 1.0
**Status:** Ready for Testing
