# GhostHub — Skill Registry for Ghost Agent

The public skill registry for [Ghost](https://github.com/boona13/ghost-agent). Browse, search, and install community skills directly from Ghost's dashboard.

## What is a Skill?

A Ghost skill is a single `SKILL.md` file with YAML frontmatter and markdown instructions. Skills teach Ghost how to handle specific tasks — from managing your email to trading stocks to automating browsers.

When clipboard content matches a skill's triggers, Ghost injects the skill's instructions into its system prompt, giving it specialized knowledge for that task.

## Browse Skills

Open Ghost's dashboard → **Skills** → **GhostHub Registry** tab to search and install skills with one click.

Or use Ghost's tools directly:
```
search the ghosthub registry for "spotify"
```

## Install a Skill

**From the dashboard:** Click **Install** on any skill card.

**From chat:** Ask Ghost:
```
install the weather skill from ghosthub
```

**Manually:** Copy the `SKILL.md` file into `~/.ghost/skills/<skill-name>/SKILL.md`.

## Submit a Skill

Anyone can contribute a skill to the registry.

### 1. Fork this repo

### 2. Create your skill directory

```
skills/
  your-skill-name/
    SKILL.md
```

### 3. Write your SKILL.md

```markdown
---
name: your-skill-name
description: "Brief description of what your skill does"
triggers:
  - "keyword1"
  - "keyword2"
tools:
  - "shell_exec"
  - "web_fetch"
priority: 5
requires:
  bins:
    - "some-cli-tool"
  env:
    - "SOME_API_KEY"
---

# Your Skill Name

Instructions for Ghost go here. Be specific — tell the LLM exactly
what tools to use and what steps to follow.

## Steps

1. Parse the user's input
2. Use `shell_exec` to run the relevant command
3. Present results clearly

## Constraints

- Don't do dangerous things without confirmation
- Handle errors gracefully
```

### 4. Open a Pull Request

The GitHub Action will automatically validate your skill and update `index.json` on merge.

**PR checklist:**
- [ ] Skill has a unique `name` that doesn't conflict with existing skills
- [ ] `description` is clear and concise
- [ ] `triggers` are specific (avoid overly generic words)
- [ ] `tools` lists only the tools your skill actually uses
- [ ] Instructions in the markdown body are specific and actionable
- [ ] No secrets, API keys, or personal data in the skill file

## SKILL.md Reference

### Frontmatter Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Unique skill identifier (lowercase, hyphens) |
| `description` | string | Yes | Brief description shown in the registry |
| `triggers` | list | Yes | Keywords that activate this skill |
| `tools` | list | No | Ghost tools this skill needs |
| `priority` | integer | No | Higher = matched first (default: 0) |
| `os` | string/list | No | OS filter: `"Darwin"`, `"Linux"`, `"Windows"` |
| `requires.bins` | list | No | CLI tools that must be on PATH |
| `requires.env` | list | No | Environment variables that must be set |

### Tips for Good Skills

- **Be specific.** Step-by-step instructions beat vague descriptions.
- **Declare tools.** Listing tools narrows Ghost's focus and improves accuracy.
- **Use constraints.** Tell Ghost what NOT to do (e.g., no destructive ops without confirmation).
- **Define output format.** Show Ghost exactly how to format its response.
- **Test your triggers.** Make sure they're specific enough to not fire on unrelated content.

## Registry Structure

```
skills-registry/
  index.json                  ← Auto-generated master index
  README.md                   ← This file
  skills/
    weather/SKILL.md          ← One directory per skill
    github/SKILL.md
    ...
  scripts/
    build-index.py            ← Generates index.json from skill frontmatter
  .github/
    workflows/
      validate-and-index.yml  ← CI: validate PRs, rebuild index on merge
```

## License

MIT
