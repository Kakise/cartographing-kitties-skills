# Cartographing Kittens — Skills

Canonical skills catalog for [Cartographing Kittens](https://github.com/Kakise/cartographing-kitties-plugin),
the AST-powered codebase intelligence framework for AI coding agents.

This repository ships nine skills that orchestrate Cartographing Kittens' MCP tools into
end-to-end workflows: structural exploration, impact analysis, annotation, brainstorming,
planning, implementation, and review.

## Layout

```
.
├── kitty/                # Router skill — graph-powered codebase intelligence
│   ├── SKILL.md
│   └── references/       # Tool reference, annotation workflow, memory protocol
├── kitty-explore/        # Structural exploration
├── kitty-impact/         # Impact analysis and refactoring
├── kitty-annotate/       # Semantic annotation workflow
├── kitty-brainstorm/     # Requirements gathering
├── kitty-plan/           # Implementation planning
├── kitty-work/           # Plan execution
├── kitty-review/         # Structural code review
└── kitty-lfg/            # Autonomous plan → work → review pipeline
```

Every top-level directory is a self-contained skill. The `kitty/` skill is the router —
the rest implement specific workflows. Sub-directories such as `kitty/references/` carry
inline documentation that the skill body references with relative paths.

## Hard requirement

**Every skill in this catalog requires the Cartographing Kittens MCP server.** The skills
orchestrate MCP tools (`index_codebase`, `query_node`, `find_dependents`, `search`,
`submit_annotations`, …) and have no fallback if the server is not available.

Install the server:

```bash
uvx cartographing-kittens
```

The server's MCP manifest lives in the
[product repository](https://github.com/Kakise/cartographing-kitties-plugin) under
`plugins/kitty/.mcp.json`.

## Frontmatter schema

Each `SKILL.md` declares its host requirements through two layers:

1. **Structured `requires` block** — host runtimes that honor it should hide skills they
   cannot satisfy:

   ```yaml
   requires:
     mcp_servers:
       - kitty
   ```

2. **Description sentence** — every `description:` ends with the literal sentence
   `Requires the Cartographing Kittens MCP server (\`uvx cartographing-kittens\`).` so the
   dependency is visible even to hosts that ignore unknown frontmatter keys.

The `metadata.source` field points back to this repository, mirroring the JetBrains
catalog convention.

## Consumption

### Cartographing Kittens product repository

The product repo mounts this catalog as a Git submodule at `plugins/kitty/skills/`:

```bash
git submodule add https://github.com/Kakise/cartographing-kitties-skills.git plugins/kitty/skills
git submodule update --init --recursive
```

### JetBrains AI Assistant

Clone the repository and point JetBrains AI Assistant at it as a skills catalog. The
flat top-level layout matches the convention used by
[JetBrains/skills](https://github.com/JetBrains/skills).

```bash
git clone https://github.com/Kakise/cartographing-kitties-skills.git
```

### Other Claude-compatible runtimes

Clone the repository into the host's skills directory, or mount it as a submodule of
your plugin layout. Hosts that honor the `requires` frontmatter will surface the MCP
dependency to users.

## Contributing

Skill content is hand-authored. Open a pull request against this repository for skill
edits — do **not** edit `plugins/kitty/skills/` in the consuming product repository
directly; that path is the submodule mount and edits there will be lost on the next
`git submodule update`.

CI runs:
- Cisco's [skill-scanner](https://github.com/JetBrains/skills/blob/main/.github/workflows/skill-scanner.yml)
  on every push and pull request, mirroring the JetBrains catalog convention.
- A frontmatter validator that enforces the `requires` schema and the
  "Cartographing Kittens MCP server" sentence.

## License

MIT — see [LICENSE](./LICENSE).
