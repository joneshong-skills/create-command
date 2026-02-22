#!/usr/bin/env python3
"""Validate a Claude Code command file.

Usage:
  python3 validate_command.py <command-name>
  python3 validate_command.py --all
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

COMMANDS_DIR = Path.home() / ".claude" / "commands"
SKILLS_DIR = Path.home() / ".claude" / "skills"

MAX_LINES_WARN = 50
MAX_LINES_ERROR = 100


def validate_one(name: str) -> list[dict]:
    """Validate a single command. Return list of {level, message}."""
    issues = []
    path = COMMANDS_DIR / f"{name}.md"

    # Existence
    if not path.exists():
        issues.append({"level": "ERROR", "message": f"File not found: {path}"})
        return issues

    content = path.read_text()
    lines = content.splitlines()

    # Name convention
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        issues.append({"level": "ERROR", "message": f"Name '{name}' must be kebab-case"})
    if len(name) > 30:
        issues.append({"level": "WARN", "message": f"Name '{name}' is {len(name)} chars (max 30)"})

    # Line count
    line_count = len(lines)
    if line_count > MAX_LINES_ERROR:
        issues.append({"level": "ERROR",
                        "message": f"{line_count} lines exceeds {MAX_LINES_ERROR} max — consider converting to a skill"})
    elif line_count > MAX_LINES_WARN:
        issues.append({"level": "WARN",
                        "message": f"{line_count} lines exceeds {MAX_LINES_WARN} recommended — trim or split"})

    # Frontmatter validation
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1].strip()
            # Check for common YAML issues
            if "name:" in fm:
                fm_name = ""
                for line in fm.splitlines():
                    if line.startswith("name:"):
                        fm_name = line.split(":", 1)[1].strip()
                        break
                if fm_name and fm_name != name:
                    issues.append({"level": "WARN",
                                    "message": f"Frontmatter name '{fm_name}' differs from filename '{name}'"})
        else:
            issues.append({"level": "WARN", "message": "Frontmatter started with --- but not properly closed"})

    # Check for skill reference links
    skill_refs = re.findall(r'~/.claude/skills/([a-z0-9-]+)/SKILL\.md', content)
    for ref in skill_refs:
        skill_path = SKILLS_DIR / ref / "SKILL.md"
        if not skill_path.exists():
            issues.append({"level": "ERROR",
                            "message": f"Referenced skill not found: {ref}/SKILL.md"})

    # Check for TODO placeholders
    todo_count = content.lower().count("todo")
    if todo_count > 0:
        issues.append({"level": "WARN",
                        "message": f"{todo_count} TODO placeholder(s) remaining"})

    # Check has at least a heading
    if not any(line.startswith("#") for line in lines):
        issues.append({"level": "WARN", "message": "No markdown heading found"})

    return issues


def print_results(name: str, issues: list[dict]) -> bool:
    """Print validation results. Return True if passed."""
    errors = [i for i in issues if i["level"] == "ERROR"]
    warns = [i for i in issues if i["level"] == "WARN"]

    if not issues:
        print(f"  \033[32m✓\033[0m {name} — OK")
        return True

    status = "\033[31m✗\033[0m" if errors else "\033[33m⚠\033[0m"
    print(f"  {status} {name}")
    for issue in issues:
        color = "\033[31m" if issue["level"] == "ERROR" else "\033[33m"
        print(f"    {color}{issue['level']}\033[0m: {issue['message']}")

    return len(errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Validate Claude Code commands")
    parser.add_argument("name", nargs="?", help="Command name (without .md)")
    parser.add_argument("--all", action="store_true", help="Validate all commands")
    args = parser.parse_args()

    if not args.name and not args.all:
        parser.print_help()
        sys.exit(1)

    print("Command Validation Report")
    print("=" * 40)

    all_passed = True

    if args.all:
        commands = sorted([f.stem for f in COMMANDS_DIR.glob("*.md")])
        if not commands:
            print("  No commands found in", COMMANDS_DIR)
            sys.exit(0)
        for name in commands:
            issues = validate_one(name)
            if not print_results(name, issues):
                all_passed = False
        print(f"\n{len(commands)} commands checked.")
    else:
        issues = validate_one(args.name)
        all_passed = print_results(args.name, issues)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
