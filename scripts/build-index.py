#!/usr/bin/env python3
"""Build index.json from skills/*/SKILL.md frontmatter.

Run from the repo root:
    python scripts/build-index.py

This reads every skills/*/SKILL.md, parses the YAML frontmatter,
and writes a consolidated index.json that the Ghost registry client fetches.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
INDEX_FILE = Path(__file__).resolve().parent.parent / "index.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_yaml_simple(text: str) -> dict:
    """Minimal YAML parser for skill frontmatter (no pyyaml dependency)."""
    result = {}
    current_key = None
    current_list = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            val = stripped[2:].strip().strip("\"'")
            if current_list is not None:
                current_list.append(val)
            continue

        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip("\"'")

            if not val:
                current_key = key
                if key in ("triggers", "tools", "tags", "bins", "env"):
                    current_list = []
                    if key in ("bins", "env"):
                        if "requires" not in result:
                            result["requires"] = {}
                        result["requires"][key] = current_list
                    else:
                        result[key] = current_list
                else:
                    current_list = None
            else:
                current_list = None
                if key in ("priority",):
                    try:
                        val = int(val)
                    except ValueError:
                        pass
                result[key] = val

    return result


def build_skill_entry(skill_dir: Path, author: str = "boona13") -> dict | None:
    """Parse a SKILL.md and return an index entry."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        print(f"  SKIP {skill_dir.name}: no frontmatter", file=sys.stderr)
        return None

    fm = parse_yaml_simple(match.group(1))
    name = fm.get("name", skill_dir.name)
    description = fm.get("description", "")

    if not name or not description:
        print(f"  SKIP {skill_dir.name}: missing name or description", file=sys.stderr)
        return None

    return {
        "name": name,
        "description": description,
        "author": author,
        "version": fm.get("version", "1.0.0"),
        "tags": fm.get("tags", []),
        "triggers": fm.get("triggers", []),
        "tools": fm.get("tools", []),
        "requires": fm.get("requires", {}),
        "installs": 0,
        "rating": 0.0,
        "updated_at": str(date.today()),
    }


def main():
    if not SKILLS_DIR.exists():
        print(f"Skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        entry = build_skill_entry(skill_dir)
        if entry:
            skills.append(entry)
            print(f"  OK   {entry['name']}")

    index = {
        "version": "1.0.0",
        "updated_at": str(date.today()),
        "skills": skills,
    }

    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {len(skills)} skills to {INDEX_FILE}")


if __name__ == "__main__":
    main()
