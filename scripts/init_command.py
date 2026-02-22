#!/usr/bin/env python3
"""Scaffold a new Claude Code command file.

Usage:
  python3 init_command.py <command-name> [--hint "args"] [--description "desc"]
  python3 init_command.py changelog --hint "[range]" --description "Generate changelog"
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

COMMANDS_DIR = Path.home() / ".claude" / "commands"

TEMPLATE = """\
---
name: {name}
description: {description}
argument-hint: "{hint}"
---

# {title}

{description}

## Quick Run

TODO: Add primary invocation command or steps.

## Options

TODO: Add arguments and flags.

## Key Reference

TODO: Add essential reference info (tables, flags, cheat sheets).
"""

TEMPLATE_NO_HINT = """\
---
name: {name}
description: {description}
---

# {title}

{description}

## Quick Run

TODO: Add primary invocation command or steps.
"""


def validate_name(name: str) -> list[str]:
    """Validate command name. Return list of issues."""
    issues = []
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        issues.append(f"Name '{name}' must be kebab-case (lowercase, hyphens only)")
    if len(name) > 30:
        issues.append(f"Name '{name}' exceeds 30 chars ({len(name)})")
    if '_' in name:
        issues.append(f"Use hyphens, not underscores: '{name}'")
    return issues


def to_title(name: str) -> str:
    """Convert kebab-case to Title Case."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def main():
    parser = argparse.ArgumentParser(description="Scaffold a Claude Code command")
    parser.add_argument("name", help="Command name (kebab-case)")
    parser.add_argument("--hint", default="", help="Argument hint for autocomplete")
    parser.add_argument("--description", default="", help="Brief description")
    parser.add_argument("--dir", default=str(COMMANDS_DIR), help="Commands directory")
    args = parser.parse_args()

    # Validate
    issues = validate_name(args.name)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        sys.exit(1)

    # Check overlap
    commands_dir = Path(args.dir)
    target = commands_dir / f"{args.name}.md"
    if target.exists():
        print(f"WARNING: {target} already exists. Overwrite? [y/N] ", end="")
        if input().strip().lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    # Check skill overlap
    skills_dir = Path.home() / ".claude" / "skills"
    matching_skills = [d.name for d in skills_dir.iterdir()
                       if d.is_dir() and args.name in d.name]
    if matching_skills:
        print(f"NOTE: Related skills found: {', '.join(matching_skills)}")
        print("  Consider making this command a wrapper for the existing skill.")

    # Generate
    commands_dir.mkdir(parents=True, exist_ok=True)
    title = to_title(args.name)
    description = args.description or f"TODO: Describe what {title} does."

    if args.hint:
        content = TEMPLATE.format(
            name=args.name, title=title,
            description=description, hint=args.hint
        )
    else:
        content = TEMPLATE_NO_HINT.format(
            name=args.name, title=title, description=description
        )

    target.write_text(content)
    print(f"Created: {target}")
    print(f"Invoke with: /{args.name}")
    if "TODO" in content:
        print("  Edit the file to replace TODO placeholders.")


if __name__ == "__main__":
    main()
