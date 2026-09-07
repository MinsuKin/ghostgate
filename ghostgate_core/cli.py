"""
GhostGate CLI: The Developer-First Command-Line Interface.
Commands:
  ghostgate scan   - Test real-time format-preserving redaction on any prompt
  ghostgate audit  - Scan developer workstation for AI privacy leaks & assign security grade
  ghostgate demo   - Launch RawHuman interactive Proof-of-Human demonstration
  ghostgate status - Probe local proxy, sentinel, and container health
  ghostgate start  - Launch GhostGate Proxy & CISO Dashboard
"""

from __future__ import annotations
import argparse
import sys
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ghostgate_core.auditor import WorkstationAuditor
from ghostgate_core.redactor import MaskingMode, SecretRedactor

console = Console()


def cmd_scan(args):
    """Scan and redact prompt text in the terminal."""
    prompt = args.prompt
    if not prompt:
        console.print("[red]Error: Please provide prompt text to scan.[/red]")
        sys.exit(1)

    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    redacted_text, ctx = redactor.redact_text(prompt)
    rehydrated_text = redactor.rehydrate_text(redacted_text, ctx)

    console.print("\n[bold cyan]🛡️ GhostGate Prompt Privacy Scanner[/bold cyan]\n")

    table = Table(title="Format-Preserving Redaction Breakdown", border_style="cyan")
    table.add_column("Transformation Stage", style="yellow", no_wrap=True)
    table.add_column("Content / Value", style="white")

    table.add_row("1. Raw Prompt (Developer Input)", prompt)
    table.add_row("2. Sanitized Prompt (Sent to Cloud LLM)", f"[green]{redacted_text}[/green]")
    table.add_row("3. Rehydrated Prompt (Returned to User)", f"[cyan]{rehydrated_text}[/cyan]")

    console.print(table)

    if ctx.redaction_count > 0:
        console.print(
            Panel(
                f"[bold green]✔ {ctx.redaction_count} Secret(s) Shielded with Zero Cloud Egress[/bold green]\n"
                f"Categories: {ctx.categories_redacted}\n"
                f"Format: Exact-length synthetic shadows (LLM syntax preserved)",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                "[dim]No high-entropy credentials or PII detected in this prompt.[/dim]",
                border_style="blue",
            )
        )


def cmd_audit(args):
    """Audit developer workstation for AI data leak vectors."""
    console.print("\n[bold cyan]🔍 Running GhostGate Workstation AI Privacy Audit...[/bold cyan]\n")
    auditor = WorkstationAuditor()
    report = auditor.audit_all()

    # Grade Color
    grade_color = "bold green" if report.grade.startswith("A") else ("bold yellow" if report.grade == "B" else "bold red")

    console.print(
        Panel(
            f"Workstation AI Privacy Grade: [{grade_color}]{report.grade}[/{grade_color}] ({report.score}/100)\n"
            f"OS: {report.environment_summary['os']} | Home: {report.environment_summary['home']}\n"
            f"OpenAI Base URL: {report.environment_summary['openai_base_url']}",
            title="[bold]SECURITY SCORECARD[/bold]",
            border_style="cyan" if report.score >= 80 else "red",
        )
    )

    table = Table(title="Workstation Security Findings", border_style="blue")
    table.add_column("Severity", style="bold", no_wrap=True)
    table.add_column("Audit Check", style="white")
    table.add_column("Remediation / Recommended Action", style="yellow")

    for f in report.findings:
        sev_color = {
            "CRITICAL": "[bold red]CRITICAL[/bold red]",
            "HIGH": "[red]HIGH[/red]",
            "MEDIUM": "[yellow]MEDIUM[/yellow]",
            "PASS": "[green]PASS[/green]",
        }.get(f.severity, f.severity)

        rem = f.remediation or "[dim]No action needed[/dim]"
        table.add_row(sev_color, f.title, rem)

    console.print(table)

    if report.score < 90:
        console.print(
            "\n[bold yellow]💡 Quick 1-Command Fix:[/bold yellow]\n"
            "Run: [green]export OPENAI_BASE_URL=\"http://127.0.0.1:8080/v1\"[/green] in your ~/.zshrc or ~/.bashrc\n"
        )


def cmd_status(args):
    """Check health of running services."""
    endpoints = [
        ("GhostGate Proxy (:8080)", "http://127.0.0.1:8080/health"),
        ("RawHuman Sentinel (:8081)", "http://127.0.0.1:8081/health"),
        ("Air-Gap Ollama (:11434)", "http://127.0.0.1:11434/api/tags"),
        ("CISO Web Dashboard", "http://127.0.0.1:8080/dashboard"),
    ]

    console.print("\n[bold cyan]📡 GhostGate Service Health Status[/bold cyan]\n")
    table = Table(border_style="cyan")
    table.add_column("Service Name", style="white")
    table.add_column("Target URL", style="yellow")
    table.add_column("Live Status", style="bold")

    for name, url in endpoints:
        try:
            r = httpx.get(url, timeout=2.0)
            if r.status_code in (200, 307):
                table.add_row(name, url, "[green]ONLINE (Active)[/green]")
            else:
                table.add_row(name, url, f"[yellow]HTTP {r.status_code}[/yellow]")
        except Exception:
            table.add_row(name, url, "[red]OFFLINE[/red]")

    console.print(table)


def cmd_demo(args):
    """Launch RawHuman CLI demonstration."""
    from rawhuman_engine.demo_cli import main as demo_main
    demo_main()


def cmd_start(args):
    """Start GhostGate proxy directly."""
    from ghostgate_core.proxy import main as proxy_main
    proxy_main()


def main():
    parser = argparse.ArgumentParser(
        prog="ghostgate",
        description="GhostGate Labs: The Agentic Air-Gap OS & AI Privacy Infrastructure",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan and format-preserve a prompt")
    scan_parser.add_argument("prompt", type=str, help="Prompt text with potential secrets")
    scan_parser.set_defaults(func=cmd_scan)

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Audit local workstation AI privacy")
    audit_parser.set_defaults(func=cmd_audit)

    # Status command
    status_parser = subparsers.add_parser("status", help="Check status of GhostGate services")
    status_parser.set_defaults(func=cmd_status)

    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run RawHuman Proof-of-Human demonstration")
    demo_parser.set_defaults(func=cmd_demo)

    # Start command
    start_parser = subparsers.add_parser("start", help="Start GhostGate AI Privacy Proxy")
    start_parser.set_defaults(func=cmd_start)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
