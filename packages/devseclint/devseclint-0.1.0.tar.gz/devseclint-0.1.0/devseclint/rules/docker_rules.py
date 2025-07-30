def scan_dockerfile(path):
    issues = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if 'latest' in line.lower():
                issues.append({
                    "file": str(path),
                    "line": i + 1,
                    "severity": "medium",
                    "message": "Avoid using 'latest' tag in Dockerfile",
                    "code": line.strip()
                })
            if 'apt-get install' in line and '-y' not in line:
                issues.append({
                    "file": str(path),
                    "line": i + 1,
                    "severity": "low",
                    "message": "Consider using non-interactive flag (-y) for apt-get",
                    "code": line.strip()
                })
    return issues