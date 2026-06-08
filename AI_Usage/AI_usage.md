# AI Usage Documentation

This document explains how AI was used in the development of the **RCA Bot (Root Cause Analysis Bot)**, including system design support, prompt engineering, debugging assistance, and automation decisions.

---

## 1. What AI Helped With

| Area | AI Contribution |
|------|----------------|
| System Architecture Design | Designed multi-stage RCA pipeline (logs → Git diff → AI analysis → report generation) |
| Jenkins Integration | Suggested pipeline failure detection workflow and log extraction strategy |
| Prompt Engineering | Created structured prompts for root cause analysis and remediation steps |
| Log Analysis Logic | Helped design parsing strategy for Jenkins failure logs and success comparison |
| Git Diff Interpretation | Assisted in extracting meaningful changes from commit history |
| SQLite Design | Suggested schema for storing RCA reports and historical failures |
| Discord Integration | Designed webhook-based notification system |
| Code Debugging | Helped fix issues in Python automation scripts and API handling |
| Documentation | Generated README structure, architecture diagrams, and usage instructions |

---

## 2. Prompts Used

### 2.1 RCA Generation Prompt (Core AI Prompt)

```text
You are an expert DevOps engineer and Site Reliability Engineer (SRE).

Analyze the following CI/CD pipeline failure.

Inputs:
- Jenkins Failure Logs
- Previous Successful Build Logs
- Git Diff Changes

Task:
1. Identify the most probable root cause of failure
2. Explain why the failure happened
3. Provide step-by-step remediation steps
4. Suggest preventive measures for future builds

Rules:
- Be precise and technical
- Do not hallucinate missing logs
- Focus only on provided data
- Output must be structured clearly

Return format:
Root Cause:
Explanation:
Impact:
Fix:
Prevention:
Confidence Score:
```

---

### 2.2 Log Summarization Prompt

```text
Summarize the following Jenkins pipeline logs into key failure points.

Focus only on errors, stack traces, and failed stages.
Ignore successful steps.

Output:
- Failure Stage
- Error Message
- Possible Cause
```

---

### 2.3 Git Diff Analysis Prompt

```text
Analyze the following Git diff changes and identify any modifications that could have caused a CI/CD pipeline failure.

Focus on:
- Dependency changes
- Configuration updates
- Environment variable changes
- Build or deployment script modifications

Return only relevant risk factors.
```

---

## 3. AI-Based Agent Workflow Design

The RCA Bot system follows this pipeline:

1. Detect Jenkins pipeline failure  
2. Collect failure logs  
3. Collect last successful build logs  
4. Extract Git diff from latest commit  
5. Send structured context to LLM (Llama 3 via Ollama)  
6. Generate Root Cause Analysis report  
7. Store results in SQLite database  
8. Send notification via Discord webhook  

---

## 4. AI Mistakes and Fixes

### 1. Overly Generic Root Cause
- Issue: AI sometimes gave vague outputs like "configuration issue"
- Fix: Forced log-based reasoning in prompt

### 2. Hallucinated Causes
- Issue: AI inferred errors not present in logs
- Fix: Added strict rule: "use only provided data"

### 3. Unstructured Output
- Issue: Inconsistent response format
- Fix: Enforced structured RCA template

### 4. Long Verbose Responses
- Issue: Over-detailed explanations
- Fix: Added conciseness constraints

### 5. Discord Formatting Issues
- Issue: Webhook message formatting broken
- Fix: Added output sanitization before sending

### 6. SQLite Insert Errors
- Issue: Response length exceeded DB limits
- Fix: Added truncation and validation layer

---

## 5. Human Review Checklist

- Jenkins failure detection tested  
- Git diff integration verified  
- Ollama Llama 3 responses validated  
- SQLite storage confirmed  
- Discord alerts working  
- Prompt outputs structured correctly  
- Edge cases tested  

---

## 6. Tools and Models Used

| Tool | Purpose |
|------|--------|
| Ollama (Llama 3) | Local AI model for RCA generation |
| Python | Automation and pipeline logic |
| Jenkins | CI/CD pipeline execution |
| SQLite | RCA report storage |
| Git | Change tracking |
| Discord Webhooks | Alert notifications |
| ChatGPT / Cursor AI | Design and debugging assistance |

---

## 7. Key Outcome of AI Usage

AI helped significantly in:

- Designing full RCA pipeline architecture  
- Reducing manual log debugging effort  
- Improving failure analysis accuracy  
- Automating DevOps troubleshooting workflow  
  