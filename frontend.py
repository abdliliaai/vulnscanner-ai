from __future__ import annotations

"""Command-line interface for VulnScan-AI.

This CLI provides a simple way to launch vulnerability assessments from the
terminal.  It delegates the heavy lifting to :mod:`scanner`, keeping the
front-end lean while allowing alternative interfaces (e.g., a web backend)
to reuse the same core logic.
"""

import argparse
from typing import Iterable

from scanner import scan_targets


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Futuristic front-end for VulnScan-AI using Hexstrike MCP",
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help="IP addresses or domains to scan",
    )
    return parser


def main(targets: Iterable[str] | None = None) -> None:
    """Entry point for the CLI."""
    if targets is None:
        parser = build_parser()
        args = parser.parse_args()
        targets = args.targets
    scan_targets(targets)


if __name__ == "__main__":
    main()
