from __future__ import annotations

"""Core scanning utilities for VulnScan-AI.

This module centralizes the logic for external network scanning,
exploitation attempts via Hexstrike MCP, and Markdown report generation.
Both the CLI front-end and the HTTP backend reuse these helpers to provide
consistent behavior across interfaces.
"""

from datetime import datetime
from pathlib import Path
import subprocess
from typing import Iterable, Dict

try:  # Optional rich dependency for nicer output
    from rich.console import Console
    from rich.panel import Panel

    console: Console | None = Console()

    def _format_panel(text: str) -> object:  # pragma: no cover - formatting only
        return Panel.fit(text)
except ModuleNotFoundError:  # pragma: no cover - rich is optional
    console = None

    def _format_panel(text: str) -> str:  # pragma: no cover - formatting only
        return text


def external_scan(target: str) -> str:
    """Run an external Nmap scan against ``target``."""
    try:
        result = subprocess.run(
            ["nmap", "-Pn", "-sV", target],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except FileNotFoundError:
        msg = (
            "Nmap is not installed or not in PATH. Install it to enable external scans."
        )
        if console:
            console.print(f"[yellow]{msg}[/yellow]")
        else:
            print(msg)
        return msg
    except subprocess.CalledProcessError as exc:
        msg = f"Nmap scan for {target} failed with exit code {exc.returncode}."
        if console:
            console.print(f"[red]{msg}[/red]")
        else:
            print(msg)
        return exc.stdout or exc.stderr or msg


def exploit_with_hexstrike(target: str) -> str:
    """Invoke Hexstrike MCP to attempt exploitation of ``target``."""
    try:
        result = subprocess.run(
            ["hexstrike", target], capture_output=True, text=True, check=True
        )
        return result.stdout
    except FileNotFoundError:
        msg = (
            "Hexstrike MCP is not installed or not in PATH. "
            "Install it from https://github.com/0x4m4/hexstrike-ai/."
        )
        if console:
            console.print(f"[yellow]{msg}[/yellow]")
        else:
            print(msg)
        return msg
    except subprocess.CalledProcessError as exc:
        msg = f"Hexstrike scan for {target} failed with exit code {exc.returncode}."
        if console:
            console.print(f"[red]{msg}[/red]")
        else:
            print(msg)
        return exc.stdout or exc.stderr or msg


def generate_report(target: str, scan_output: str, exploit_output: str) -> Path:
    """Create a simple Markdown report for ``target``."""
    report_text = (
        f"# VulnScan-AI Report for {target}\n\n"
        f"Generated: {datetime.utcnow().isoformat()}Z\n\n"
        "## External Scan\n"
        f"``\n{scan_output}\n``\n\n"
        "## Exploitation\n"
        f"``\n{exploit_output}\n``\n"
    )
    filename = Path(f"report_{target.replace('/', '_')}.md")
    filename.write_text(report_text)
    return filename


def assess_target(target: str) -> Dict[str, object]:
    """Assess a single target and return raw outputs and report path."""
    if console:
        panel = _format_panel(f"Starting assessment for [cyan]{target}[/cyan]")
        console.print(panel)
    else:
        print(_format_panel(f"Starting assessment for {target}"))
    scan_output = external_scan(target)
    exploit_output = exploit_with_hexstrike(target)
    report_path = generate_report(target, scan_output, exploit_output)
    if console:
        done = _format_panel(f"Report written to [green]{report_path}[/green]")
        console.print(done)
    else:
        print(_format_panel(f"Report written to {report_path}"))
    return {
        "scan_output": scan_output,
        "exploit_output": exploit_output,
        "report_path": report_path,
    }


def scan_targets(targets: Iterable[str]) -> None:
    """Assess multiple targets sequentially."""
    for target in targets:
        assess_target(target)
