# devseclint/rules/k8s_rules.py
import yaml

def scan_kubernetes_yaml(path):
    issues = []
    try:
        with open(path, 'r') as f:
            docs = list(yaml.safe_load_all(f))
        for doc in docs:
            if not doc or 'kind' not in doc:
                continue
            containers = doc.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
            for container in containers:
                sc = container.get('securityContext', {})
                if not sc.get('runAsNonRoot'):
                    issues.append({
                        "file": str(path),
                        "line": 1,
                        "severity": "high",
                        "message": "Kubernetes container missing runAsNonRoot",
                        "code": yaml.dump(container)
                    })
    except Exception as e:
        issues.append({
            "file": str(path),
            "line": 0,
            "severity": "error",
            "message": f"YAML parse error: {str(e)}",
            "code": ""
        })
    return issues