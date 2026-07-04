"""Run every rule over every tool and aggregate into a LintResult."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .loader import load_tools
from .rules import Finding, check_tool, ERROR, WARN, INFO


@dataclass
class LintResult:
    tool_count: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def counts(self) -> dict[str, int]:
        c = Counter(f.severity for f in self.findings)
        return {ERROR: c.get(ERROR, 0), WARN: c.get(WARN, 0), INFO: c.get(INFO, 0)}

    @property
    def tools_with_errors(self) -> int:
        return len({f.tool for f in self.findings if f.severity == ERROR})

    def passed(self, strict: bool = False) -> bool:
        counts = self.counts
        if counts[ERROR] > 0:
            return False
        if strict and counts[WARN] > 0:
            return False
        return True


def lint_file(path: str) -> LintResult:
    tools = load_tools(path)
    result = LintResult(tool_count=len(tools))
    for i, tool in enumerate(tools):
        result.findings.extend(check_tool(tool, i))
    # order: errors first, then warns, then infos; stable within severity
    order = {ERROR: 0, WARN: 1, INFO: 2}
    result.findings.sort(key=lambda f: order.get(f.severity, 3))
    return result
