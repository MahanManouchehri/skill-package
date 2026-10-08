#!/usr/bin/env python3
"""Non-mutating structural sanity checks for hand-off docs.

Usage: python3 validate_handoff.py /path/to/repo /path/to/repo/docs/hand-offs/ticketing
Not a source-semantics verifier; run a separate human/agent evidence audit.
"""
from __future__ import annotations
import pathlib
import re
import sys

REQUIRED = {
    'developer-guide.md': ['شروع سریع', 'File & Symbol Atlas', 'Execution Walkthrough', 'Independent Development Playbook', 'Debugging Playbook', 'Coverage'],
    'llm-context.md': ['Instructions to receiving LLM', 'Architecture and Navigation Map', 'Primary Execution Paths', 'Edit/Impact Locator', 'Context Freshness'],
}
LOCATION = re.compile(r'`([\w./-]+\.(?:php|py|ts|tsx|js|jsx|go|java|rs|rb|cs|kt|sql|yml|yaml|json|md)):L(\d+)(?:-L?(\d+))?`')
TEMPLATE = re.compile(r'\{\{[^}]+\}\}')


def validate(repo: pathlib.Path, out: pathlib.Path) -> list[str]:
    problems: list[str] = []
    repo = repo.resolve()
    for fn, sections in REQUIRED.items():
        f = out / fn
        if not f.is_file():
            problems.append(f'MISSING: {f}')
            continue
        data = f.read_text(encoding='utf-8')
        if TEMPLATE.search(data):
            problems.append(f'TEMPLATE PLACEHOLDERS: {f}')
        for heading in sections:
            if heading not in data:
                problems.append(f'SECTION MISSING [{fn}]: {heading}')
        if data.count('<!-- HAND-OFF:MANUAL:BEGIN -->') != data.count('<!-- HAND-OFF:MANUAL:END -->'):
            problems.append(f'UNBALANCED MANUAL SECTION: {f}')
        for path, first, last in LOCATION.findall(data):
            target = (repo / path).resolve()
            try:
                target.relative_to(repo)
            except ValueError:
                problems.append(f'PATH ESCAPES REPO: {path}')
                continue
            if not target.is_file():
                problems.append(f'PATH MISSING [{fn}]: {path}')
                continue
            n = sum(1 for _ in target.open(encoding='utf-8', errors='replace'))
            a = int(first); b = int(last or first)
            if a < 1 or b < a or b > n:
                problems.append(f'LINE RANGE INVALID [{fn}]: {path}:L{a}-L{b} (file lines={n})')
    return problems


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(2)
    issues = validate(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
    if issues:
        for issue in issues:
            print('FAIL:', issue)
        sys.exit(1)
    print('PASS: documentation structure and referenced path/line sanity checks (NOT semantic evidence validation).')
