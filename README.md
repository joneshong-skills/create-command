[English](README.md) | [繁體中文](README.zh.md)

# create-command

Build lightweight slash commands — the slim alternative to full skills.

## Description

Create Command guides creation of Claude Code slash commands (`~/.claude/commands/*.md`) — lightweight, single-purpose directives for frequent tasks that don't need the full skill infrastructure.

## Features

- Distinguishes when a command is better than a full skill
- Generates properly structured `.md` files for `~/.claude/commands/`
- Provides guidance on command naming and argument patterns
- Includes examples and usage hints in the command file
- Covers one-shot commands, template commands, and parameter commands
- Keeps commands lean — no scripts, no assets, just intent

## Usage

Invoke by asking Claude Code with trigger phrases such as:

- "create a command"
- "make a slash command"
- "新增 command"
- "建立指令"
- "skill 還是 command"

## Related Skills

- [`create-skill`](https://github.com/joneshong-skills/create-skill)
- [`create-agent`](https://github.com/joneshong-skills/create-agent)

## Install

Copy the skill directory into your Claude Code skills folder:

```
cp -r create-command ~/.claude/skills/
```

Skills placed in `~/.claude/skills/` are auto-discovered by Claude Code. No additional registration is needed.
