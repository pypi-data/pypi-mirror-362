from pathlib import Path
from devseclint.rules.env_rules import scan_env_file
from devseclint.rules.docker_rules import scan_dockerfile
from devseclint.rules.k8s_rules import scan_kubernetes_yaml

def scan_directory(path: str) -> list[dict]:
    path = Path(path)
    results = []

    for file in path.rglob("*"):
        if file.name == ".env":
            results += scan_env_file(file)
        elif file.name.lower() == "dockerfile":
            results += scan_dockerfile(file)
        elif file.suffix in [".yaml", ".yml"]:
            results += scan_kubernetes_yaml(file)

    return results
