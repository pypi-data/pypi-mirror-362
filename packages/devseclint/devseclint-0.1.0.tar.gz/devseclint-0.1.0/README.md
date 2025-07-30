# DevSecLint 🛡️

A secure config scanner for developers. Scans `.env`, Dockerfile, Kubernetes, and more for misconfigurations — with optional AI-powered fixes (Gemini).

## Features

- 🔍 Detect secrets in `.env`
- 🐳 Scan Dockerfiles for bad practices
- ☸️ Validate Kubernetes YAML for securityContext
- 🤖 AI remediation suggestions (Google Gemini)
- ✅ CLI + Python API + GitHub Action ready

---

## 🔧 Install

```bash
pip install devseclint
```

Or locally:

```bash
pip install -e .
```

## 🚀 CLI Usage
```bash
devseclint scan .
```

### Optional flags:

```
--ai-fix → show AI suggestions

--fix → auto-rewrite files (uses Gemini)

--ci → CI-friendly JSON output
```

### 🧠 AI Fixes (Gemini)
Set your API key:

```bash
export GEMINI_API_KEY=your-key-here
```

or 
- change the `template.env` to `.env` and add `GEMINI_API_KEY`

Then run:

```bash
devseclint scan . --ai-fix
devseclint scan . --fix
```

## 📦 Python API
```python
from devseclint.scanner import scan_directory

results = scan_directory("/path/to/code")
for issue in results:
    print(issue)
```

## ✅ GitHub Action
```yaml
- name: Run DevSecLint
  run: python cli.py scan . --ci
```

- SAMPLE TEMPLATE IN `template.github`, change to `.github`

## 📄 License
MIT © Rohan Shaw