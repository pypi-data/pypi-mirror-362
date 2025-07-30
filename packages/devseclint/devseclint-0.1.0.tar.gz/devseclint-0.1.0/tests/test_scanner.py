# tests/test_scanner.py
from devseclint.scanner import scan_directory
import tempfile
from pathlib import Path

def test_env_scan():
    with tempfile.TemporaryDirectory() as tmp:
        env_file = Path(tmp) / ".env"
        env_file.write_text("AWS_SECRET=abc123\n")
        results = scan_directory(tmp)
        assert any("Hardcoded secret" in i["message"] for i in results)

def test_docker_scan():
    with tempfile.TemporaryDirectory() as tmp:
        docker_file = Path(tmp) / "Dockerfile"
        docker_file.write_text("FROM ubuntu:latest\n")
        results = scan_directory(tmp)
        assert any("latest" in i["message"] for i in results)

def test_k8s_scan():
    with tempfile.TemporaryDirectory() as tmp:
        k8s_file = Path(tmp) / "deployment.yaml"
        k8s_file.write_text("""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: nginx
""")
        results = scan_directory(tmp)
        assert any("runAsNonRoot" in i["message"] for i in results)
