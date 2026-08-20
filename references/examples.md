# Command Examples

Real commands from this codebase, organized by archetype.

## Type A: Script Wrapper

Wraps a backing skill's script with a quick-reference card.

### skill-test.md (20 lines)

```markdown
# Skill Tester

Run automated T1-T4 skill health checks.

## Quick Run
```bash
bash ~/.claude/skills/skill-tester/scripts/run_all.sh
```

## Options
- Single skill: `--skill pdf`
- Categories: `--category T1,T2`
- JSON output: `--format json`
- Save to file: `--output ~/.claude/outputs/skill-tester/report.md`

## T5 Scenario Tests
T5 requires Claude's judgment — invoke the full `/skill-tester` skill for scenario testing.

Full reference: `~/.claude/skills/skill-tester/SKILL.md`
```

**Why it works**: Quick Run is one copy-paste line. Options are scannable.
Notes that T5 needs the full skill (hybrid pattern boundary).

### skill-publish.md (22 lines)

```markdown
# Skill Publisher

Publish a skill to GitHub with git + platform registration.

## Quick Commands
```bash
# Scan status of all skills
bash ~/.claude/skills/skill-publisher/scripts/publish.sh --scan

# Publish a single skill
bash ~/.claude/skills/skill-publisher/scripts/publish.sh smart-search

# Dry-run (preview)
bash ~/.claude/skills/skill-publisher/scripts/publish.sh smart-search --dry-run
```

## Pre-requisites
- README.md and README.zh.md must exist (use the full `/skill-publisher` skill to generate them)
- Logo is optional (use `/image-gen` to create one)

Full reference: `~/.claude/skills/skill-publisher/SKILL.md`
```

**Why it works**: Three usage patterns (scan, publish, dry-run) in one block.
Pre-requisites section prevents common failures.

## Type B: Quick Reference

Provides a cheat sheet for a CLI tool or workflow.

### claude-headless.md (16 lines)

```markdown
# Claude Code Headless

Run `claude -p` in headless mode.

## Quick Reference
- Simple: `claude -p "prompt"`
- JSON: `claude -p "prompt" --output-format json | jq -r '.result'`
- Auto-approve: `--allowedTools "Bash,Read,Edit"`
- Background: wrapper with `--background --notify`
- Nesting fix: `unset CLAUDECODE && claude -p "..."`
- PTY fix (macOS): `script -q /dev/null claude -p "..."`
- Permission: `--permission-mode plan|acceptEdits|bypassPermissions`
- Resume: `--resume SESSION_ID` or `--continue`

Full reference: `~/.claude/skills/claude-code-headless/SKILL.md`
```

**Why it works**: Every line is a self-contained recipe. No explanation needed —
the format speaks for itself. Includes non-obvious gotchas (nesting fix, PTY fix).

### skill-catalog.md (20 lines)

```markdown
# Skill Catalog

Export a structured inventory of all installed skills.

## Quick Run
```bash
~/.local/bin/python3 ~/.claude/skills/skill-catalog/scripts/extract_catalog.py
```

## Output
- JSON: `~/.claude/outputs/skill-catalog/skill-catalog.json`
- CSV: add `--format csv`
- Table: add `--format table` (terminal display)

## What It Extracts
Per skill: name, version, domain, tags, tools, composable relationships.

Full reference: `~/.claude/skills/skill-catalog/SKILL.md`
```

**Why it works**: Script call + output format options + what you get. Under 20 lines.

## Type C: Template (Knowledge Card)

A prompt template or knowledge framework — no backing script.

### image-prompt.md (28 lines)

```markdown
# Image Prompt Generator

Convert vague descriptions into structured AI image generation prompts.

## 7-Component Framework
1. **Subject**: Main focus, specific details
2. **Style**: Art style, medium, artist reference
3. **Composition**: Framing, perspective, layout
4. **Lighting**: Type, direction, mood
5. **Color**: Palette, tone, contrast
6. **Details**: Texture, material, environment
7. **Atmosphere**: Mood, emotion, time of day

## Output Format
Two formats per prompt:
- **Single string**: Ready to paste into any AI image generator
- **Structured JSON**: Components breakdown + negative prompt + recommended model

## Quality Boosters
Automatically appends: `masterpiece, best quality, highly detailed, sharp focus`

Full reference: `~/.claude/skills/image-prompt/SKILL.md`
```

**Why it works**: The 7-component framework IS the value — Claude uses it as a
checklist when generating prompts. No script needed.

### changelog.md (31 lines)

```markdown
# Changelog Generator

Transform git commits into user-facing release notes.

## Usage
Provide a commit range or let it auto-detect from the last tag:
- From tag: commits since last git tag
- Custom range: `v1.0.0..HEAD`
- Last N commits: `--last 20`

## Workflow
1. Gather commits in range
2. Categorize: Breaking | Feature | Improvement | Fix | Security | Noise
3. Filter internal/noise commits
4. Rewrite technical messages as user-friendly benefits
5. Format as markdown release notes

## Output Format
```
# Release Notes — vX.Y.Z

## Breaking Changes
## New Features
## Improvements
## Bug Fixes
```

Full reference: `~/.claude/skills/changelog-gen/SKILL.md`
```

**Why it works**: Workflow steps guide Claude's behavior. Output format shows
exactly what to produce. No script — Claude follows the template directly.

## Type D: Standalone

Self-contained command with no backing skill.

### Example: clean-branches (not yet created)

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

**Why it works**: Single bash command, no skill or script needed.
Dry-run pattern prevents accidental deletion.

## Anti-Patterns

### Too verbose (bad)

```markdown
# Deploy

## Introduction
This command helps you deploy your application to various environments.
It supports multiple deployment targets and can be customized...

## Prerequisites
Before using this command, make sure you have:
- Node.js 18+ installed
- AWS CLI configured
- Docker running
...
```

**Problem**: 50+ lines of explanation before the actual command. Claude already
knows what deployment is. Just show the command.

### Too terse (bad)

```markdown
deploy $1 $2
```

**Problem**: No context, no options, no error guidance. If something goes wrong,
Claude has nothing to work with.

## Line Count Reference

| Command | Lines | Type | Notes |
|---------|-------|------|-------|
| claude-headless | 16 | Quick Reference | Ideal density |
| skill-test | 20 | Script Wrapper | Good hybrid pattern |
| skill-catalog | 20 | Script Wrapper | Clean structure |
| skill-publish | 22 | Script Wrapper | Multiple usage patterns |
| image-prompt | 28 | Template | Framework justifies length |
| changelog | 31 | Template | Workflow + format spec |
| screen-record | 19 | Quick Reference | Under development |

Average: ~22 lines. All under the 50-line recommended limit.
