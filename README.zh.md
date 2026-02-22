[English](README.md) | [繁體中文](README.zh.md)

# create-command

Build lightweight slash commands — the slim alternative to full skills.

## 說明

Create Command guides creation of Claude Code slash commands (`~/.claude/commands/*.md`) — lightweight, single-purpose directives for frequent tasks that don't need the full skill infrastructure.

## 功能特色

- Distinguishes when a command is better than a full skill
- Generates properly structured `.md` files for `~/.claude/commands/`
- Provides guidance on command naming and argument patterns
- Includes examples and usage hints in the command file
- Covers one-shot commands, template commands, and parameter commands
- Keeps commands lean — no scripts, no assets, just intent

## 使用方式

透過以下觸發語句呼叫 Claude Code 來使用此技能：

- "create a command"
- "make a slash command"
- "新增 command"
- "建立指令"
- "skill 還是 command"

## 相關技能

- [`create-skill`](https://github.com/joneshong-skills/create-skill)
- [`create-agent`](https://github.com/joneshong-skills/create-agent)

## 安裝

將技能目錄複製到 Claude Code 技能資料夾：

```
cp -r create-command ~/.claude/skills/
```

放置在 `~/.claude/skills/` 的技能會被 Claude Code 自動發現，無需額外註冊。
