#!/usr/bin/env python3
"""Validate Cartographing Kittens skill frontmatter.

Enforces, for every `*/SKILL.md` at the repo root:

- `name` is a non-empty string
- `description` is a non-empty string containing the substring
  "Cartographing Kittens MCP server"
- `metadata.source` is a string starting with
  "https://github.com/Kakise/cartographing-kitties-skills/"
- `requires.mcp_servers` is a list containing at least "kitty"
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_PREFIX = "https://github.com/Kakise/cartographing-kitties-skills/"
REQUIRED_DESCRIPTION_SUBSTRING = "Cartographing Kittens MCP server"


def _parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def validate_skill(path: Path) -> list[str]:
    display = path.relative_to(REPO_ROOT)
    try:
        frontmatter = _parse_frontmatter(path)
    except ValueError as exc:
        return [f"{display}: {exc}"]

    errors: list[str] = []

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{display}: `name` must be a non-empty string")

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{display}: `description` must be a non-empty string")
    elif REQUIRED_DESCRIPTION_SUBSTRING not in description:
        errors.append(
            f"{display}: `description` must mention `{REQUIRED_DESCRIPTION_SUBSTRING}`"
        )

    metadata = frontmatter.get("metadata", {})
    if not isinstance(metadata, dict):
        errors.append(f"{display}: `metadata` must be a mapping")
    else:
        source = metadata.get("source")
        if not isinstance(source, str) or not source.startswith(EXPECTED_SOURCE_PREFIX):
            errors.append(
                f"{display}: `metadata.source` must start with `{EXPECTED_SOURCE_PREFIX}`"
            )

    requires = frontmatter.get("requires", {})
    if not isinstance(requires, dict):
        errors.append(f"{display}: `requires` must be a mapping")
    else:
        mcp_servers = requires.get("mcp_servers", [])
        if not isinstance(mcp_servers, list) or "kitty" not in mcp_servers:
            errors.append(
                f"{display}: `requires.mcp_servers` must be a list containing `kitty`"
            )

    return errors


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(REPO_ROOT.glob("*/SKILL.md"))
    if not skill_files:
        print("No SKILL.md files found at repo root", file=sys.stderr)
        return 1

    for skill_path in skill_files:
        errors.extend(validate_skill(skill_path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skill(s) — frontmatter OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
