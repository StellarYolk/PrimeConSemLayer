# AGENTS.md

## What this repo is

An OpenCode skills registry. It contains no application code, build steps, or tests.

## Structure

- `skills-lock.json` — authoritative source of installed skills, their GitHub origins, and integrity hashes. Do not edit manually.
- `.agents/skills/` — installed skill directories. Each skill has a `SKILL.md` entrypoint plus optional `references/`, `recipes/`, `templates/`, and `channels/`.

## Installed skills

| Skill | Source |
|---|---|
| `ai-sdk` | vercel/ai |
| `autofix` | coderabbitai/skills |
| `code-review` | coderabbitai/skills |
| `excalidraw-diagram-generator` | github/awesome-copilot |
| `frontend-design` | anthropics/skills |
| `personize-governance` | personizeai/personize-skills |
| `personize-memory` | personizeai/personize-skills |
| `personize-solution-architect` | personizeai/personize-skills |

## Working conventions

- Skills are managed through OpenCode's skill system, not manual file edits. Changes to `skills-lock.json` should come from `opencode skill add/remove` commands.
- When adding or modifying a skill, update `skills-lock.json` hash accordingly.
- This repo lives under `PrimeConSemLayer` — part of an internship project.
