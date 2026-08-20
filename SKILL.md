---
name: create-command
description: "command, create, add, slash, 建一個指令, 新增 slash command, 把這個做成 command"
version: 0.2.0
tools: Read, Write, Edit, Bash, Glob, Grep, sandbox_execute
argument-hint: "command name or description"
io:
  input:
    - mime: "text/plain"
      description: "Command concept and behavior"
  output:
    - mime: "text/markdown"
      description: "Generated command definition"
disable-model-invocation: true
---

# Create Command

Guide the creation of lightweight Claude Code commands — the slim alternative to full skills.

## Agent Delegation

Delegate command scaffolding to `worker` agent.

## Command vs Skill vs Script vs Hook

The first and most important decision. Use this matrix:

| Signal | → Command | → Skill | → Script | → Hook |
|--------|-----------|---------|----------|--------|
| Steps are fixed, no routing | Yes | | | |
| Needs Claude's judgment at each step | | Yes | | |
| All steps are deterministic code | | | Yes | |
| Should auto-trigger on events | | | | Yes |
| Simple prompt template (<50 lines) | Yes | | | |
| Complex routing / multi-path logic | | Yes | | |
| Wraps an existing script | Yes | | | |
| Needs scripts/, references/, assets/ | | Yes | | |
| Under 500 tokens when loaded | Yes | | | |

**One-line rule**: Does the flow have "看情況決定" nodes? → Skill. All steps are "不管什麼情況都這樣做"? → Command/Script/Hook.

### Decision Tree

```
Is it event-triggered? (before commit, session start, etc.)
  └─ Yes → Hook (~/.claude/hooks/)

Is all logic deterministic code? (no Claude reasoning needed)
  └─ Yes → Shell/Python script

Does it need supporting files? (scripts/, references/, assets/)
  └─ Yes → Skill (~/.claude/skills/)

Is it a simple prompt template? (<50 lines, fixed workflow)
  └─ Yes → Command (~/.claude/commands/)

Default → Skill
```

### Hybrid Pattern

A command can **wrap** an existing skill's script while the skill retains the full logic:

```
Command (lightweight):  Quick reference + script invocation
Skill (full):           Complex routing + judgment + fallbacks
Script (deterministic): The actual automation code
```

Example from this codebase:
- `/skill-test` command → calls `run_all.py` for T1-T4
- `/skill-tester` skill → full T1-T5 with scenario tests and agent judgment

## Command Format

### File Location

```
~/.claude/commands/<command-name>.md
```

Invoked as `/<command-name>` in Claude Code.

### Structure

```markdown
---
name: command-name                          # Optional, defaults to filename
description: Brief description              # Optional but recommended
argument-hint: "[arg1] [arg2]"             # Optional, shown in autocomplete
disable-model-invocation: true             # Optional, user-only
allowed-tools: Bash, Read                  # Optional, restrict tools
---

# Command Title

Brief purpose (1 sentence).

## Quick Run / Usage
[Primary invocation — script call or step list]

## Options / Arguments
[If the command takes arguments]

## Key Reference
[Minimal essential info — tables, flags, cheat sheets]

Full reference: `~/.claude/skills/<related-skill>/SKILL.md`
```

### Argument Substitution

Commands support positional arguments:

| Variable | Meaning |
|----------|---------|
| `$ARGUMENTS` | All arguments as a single string |
| `$1`, `$2`, `$3` | Positional arguments |

Example:
```markdown
# Deploy

Deploy `$1` to `$2` environment.

```bash
./scripts/deploy.sh $1 --env $2
```
```

### Frontmatter Fields

All fields are optional:

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | Slash command name (defaults to filename) |
| `description` | string | When to use (for auto-discovery) |
| `argument-hint` | string | Autocomplete hint, e.g. `"[skill-name]"` |
| `disable-model-invocation` | bool | `true` = only user can invoke |
| `user-invocable` | bool | `false` = only Claude can invoke |
| `allowed-tools` | string | Restrict available tools |
| `context` | string | `"fork"` = run in isolated subagent |
| `agent` | string | Subagent type (Explore, Plan, etc.) |

## Creation Workflow

### Step 1: Classify

Run the decision tree above. If the answer is "Command", proceed.
If uncertain, default to Skill (can always slim down later).

### Step 2: Check Overlap

**Preferred (Sandbox)**:
```python
# sandbox_execute
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/create-command/scripts"))
import validate_command
results = validate_command.check_overlap("<keyword>")
output(results)
```

**Fallback (Bash)**:
```bash
ls ~/.claude/commands/ | grep -i "<keyword>"
ls ~/.claude/skills/ | grep -i "<keyword>"
```

If an existing skill covers the same scope, create the command as a
**lightweight entry point** that references the skill, not a replacement.

### Step 3: Scaffold

```bash
~/.local/bin/python3 ~/.claude/skills/create-command/scripts/init_command.py <command-name> [--hint "args"]
```

Or write directly — commands are simple enough to create inline.

### Step 4: Write Content

**Target**: Under 50 lines. Under 500 tokens when loaded.

Content priority (most important first):
1. **Quick Run** — The primary action (script call, one-liner)
2. **Options** — Arguments and flags
3. **Key Reference** — Only what's needed for the quick run
4. **Full reference link** — Point to the skill's SKILL.md for details

**What NOT to include**:
- Verbose explanations (Claude already knows most things)
- Full documentation (that's the skill's job)
- Examples longer than 3-5 lines
- Continuous improvement sections (commands are static)

### Step 5: Validate

```bash
~/.local/bin/python3 ~/.claude/skills/create-command/scripts/validate_command.py <command-name>
```

Checks:
- File exists and is valid markdown
- Frontmatter YAML is valid (if present)
- Line count under 50 (warn) / 100 (error)
- No orphaned skill references (linked SKILL.md exists)
- Naming convention: kebab-case, no underscores

### Step 6: Test

Invoke the command with `/<command-name>` and verify it works as expected.

## Command Archetypes

### Type A: Script Wrapper

Wraps an existing script with a quick-reference card.

```markdown
# Skill Test

Run automated skill health checks.

## Quick Run
```bash
~/.local/bin/python3 ~/.claude/skills/skill-tester/scripts/run_all.py
```

## Options
- Single skill: `--skill pdf`
- JSON output: `--format json`

Full reference: `~/.claude/skills/skill-tester/SKILL.md`
```

### Type B: Quick Reference

Provides a cheat sheet for a tool or workflow.

```markdown
# Codex Headless

Run `codex exec` in headless mode.

## Quick Reference
- Simple: `codex exec "prompt"`
- Full auto: `--full-auto`
- Model: `-m o4-mini`

Full reference: `~/.claude/skills/codex-cli-headless/SKILL.md`
```

### Type C: Template

A prompt template with argument substitution.

```markdown
# Deploy

Deploy service `$1` to the `$2` environment.

## Steps
1. Run tests: `npm test --project $1`
2. Build: `npm run build --project $1`
3. Deploy: `./infra/deploy.sh $1 $2`
4. Verify: `curl -s https://$2.example.com/$1/health`
```

### Type D: Standalone

A self-contained command with no backing skill.

```markdown
# Clean Branches

Delete local branches that have been merged into main.

```bash
git branch --merged main | grep -v '^\*\|main\|master' | xargs -r git branch -d
```

Dry-run first:
```bash
git branch --merged main | grep -v '^\*\|main\|master'
```
```

## Naming Conventions

| Pattern | Examples | When |
|---------|----------|------|
| Action verb | `deploy`, `changelog`, `readme` | Most commands |
| Noun (tool name) | `skill-catalog`, `screen-record` | Tool reference |
| Skill-name prefix | `skill-test`, `skill-publish` | Skill wrappers |
| No CLI prefix | `codex-headless` not `codex-cli-headless` | CLI quick refs |

Rules:
- kebab-case only (no underscores, no camelCase)
- Shorter than the backing skill name when possible
- Max 30 characters

## Batch Creation

When converting multiple skills to commands at once:

1. List candidates: skills with deterministic workflows or simple templates
2. For each, extract the **Quick Run + Options** core (discard routing logic)
3. Create all command files
4. Validate all: `for f in ~/.claude/commands/*.md; do ~/.local/bin/python3 scripts/validate_command.py "$(basename "$f" .md)"; done`
5. Keep original skills as full-reference backups

## Sandbox Optimization

This skill is **sandbox-optimized**. Batch operations run inside `sandbox_execute`:

- **Overlap check**: Import `scripts/validate_command.py` in sandbox to scan commands and skills directories simultaneously in one pass
- **Batch validation**: When validating multiple commands at once, import the validate script in sandbox and loop over the list without spawning per-command subprocesses

Principle: **Deterministic batch work → sandbox; reasoning/presentation → LLM.**

## Additional Resources

### Reference Files
- **`references/examples.md`** — Real command examples from the codebase

### Scripts
- **`scripts/init_command.py`** — Scaffold a new command file
- **`scripts/validate_command.py`** — Validate command structure and quality
