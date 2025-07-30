# devseclint/utils.py
from rich.console import Console

console = Console()

def print_issues(issues):
    for issue in issues:
        console.print(f"[red]File:[/] {issue['file']} [cyan]Line:[/] {issue['line']}")
        console.print(f"[yellow]{issue['severity'].upper()}:[/] {issue['message']}")
        console.print(f"[white]{issue['code']}\n")

    if not issues:
        console.print("[green]No issues found.[/]")