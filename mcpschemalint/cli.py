"""Command-line interface for mcp-schema-lint.

Usage:
    python -m mcpschemalint lint <tools.json> [options]

The input is a JSON file of MCP tool definitions: a bare list, or an object with
a "tools" (or "result.tools") array. Get it from a server's tools/list response,
or export your registered tools to JSON.

Options:
    --strict       treat warnings as failures too
    --html PATH    also write an HTML report
    --md PATH      also write a Markdown report
    --quiet        suppress the text report on stdout

Exit code 0 when clean (no errors; no warnings under --strict), 1 when findings
fail the gate, 2 on a usage/IO error. So it gates CI before a server ships.
"""

from __future__ import annotations

import argparse
import os
import sys

from .linter import lint_file
from . import report as report_mod


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mcpschemalint",
        description="Lint MCP tool schemas for agent-unfriendly patterns (offline, static).",
    )
    sub = parser.add_subparsers(dest="command")
    a = sub.add_parser("lint", help="lint a JSON file of MCP tool definitions")
    a.add_argument("tools", help="path to the tools JSON")
    a.add_argument("--strict", action="store_true", help="fail on warnings too")
    a.add_argument("--html", default=None)
    a.add_argument("--md", default=None)
    a.add_argument("--quiet", action="store_true")
    return parser


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def run(args) -> int:
    try:
        result = lint_file(args.tools)
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc.filename}", file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not args.quiet:
        print(report_mod.render_text(result))
    if args.html:
        _ensure_parent(args.html)
        with open(args.html, "w", encoding="utf-8") as handle:
            handle.write(report_mod.render_html(result))
        if not args.quiet:
            print(f"\nwrote HTML report: {args.html}")
    if args.md:
        _ensure_parent(args.md)
        with open(args.md, "w", encoding="utf-8") as handle:
            handle.write(report_mod.render_markdown(result))
        if not args.quiet:
            print(f"wrote Markdown report: {args.md}")

    return 0 if result.passed(strict=args.strict) else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "lint":
        return run(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
