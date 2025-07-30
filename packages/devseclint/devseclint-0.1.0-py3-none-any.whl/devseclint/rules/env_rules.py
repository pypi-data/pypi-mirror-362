# devseclint/rules/env_rules.py
import re

def scan_env_file(path):
    issues = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if re.search(r'(AWS|SECRET|KEY|TOKEN)=.+', line, re.IGNORECASE):
                issues.append({
                    "file": str(path),
                    "line": i + 1,
                    "severity": "high",
                    "message": "Hardcoded secret found in .env file",
                    "code": line.strip()
                })
    return issues
