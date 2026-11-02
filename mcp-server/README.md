# SkillStack MCP Server

A Model Context Protocol (MCP) server that exposes the
[SkillStack](../README.md) **168-skill / 9-theme** library to any MCP-aware
client (Claude Desktop, Cursor, Cline, Continue, ...).

It lets the agent answer questions like *"which skill should I load for this
task?"* and *"give me the full SKILL.md content for this skill"* — without
having to grep the repo every time.

## Tools exposed

| Tool                            | What it does                                                                                                                                               |
|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `list_skills`                   | Returns a JSON array of every SkillStack skill: `{theme, name, description, tags, path}`.                                                                  |
| `search_skills(query)`          | Free-text search across skill names, descriptions, and tags. Returns ranked matches with a score.                                                          |
| `get_skill(theme, skill_name?)` | Returns the full `SKILL.md` body for `<theme>/<skill_name>/SKILL.md`. Omit `skill_name` for theme-level skills like `LLM/SKILL.md`.                        |
| `route_task(task_description)`  | Maestro-style keyword router. Returns 1–3 skill suggestions for a natural-language task, plus the matched theme and the keywords that triggered the match. |

## How it works

The server walks `../` (the `skills/` directory) at startup, finds every
`**/SKILL.md` file (excluding `maestro/SKILL.md`, which is the router itself),
parses the YAML frontmatter with `js-yaml`, and builds an in-memory index.
The parser is **tolerant of malformed YAML** — if a SKILL.md has a broken
`tags:` field (e.g., a missing opening `[`), it falls back to per-field regex
extraction so the rest of the file is still indexed.

Tags come from the `tags:` frontmatter field when present; otherwise they are
derived from the `description` by tokenising, dropping stopwords, and counting
the most frequent terms.

## Install

```bash
cd /home/z/my-project/skills/mcp-server
npm install
```

This pulls `@modelcontextprotocol/sdk`, `glob`, and `js-yaml`. Node 18+ is
required (the server uses ESM and the global `fetch`).

## Run (smoke test)

```bash
npm start
# or directly:
node index.js
```

The server speaks JSON-RPC over stdio, so it will appear to "hang" waiting
for input. That is correct — it is an MCP server, not a CLI. Kill with
`Ctrl-C`.

### Quick test without an MCP client

You can hit the underlying functions directly from a one-liner to verify the
index builds correctly:

```bash
node -e '
  import("./index.js").catch(async () => {
    const { Server } = await import("@modelcontextprotocol/sdk/server/index.js");
  });
'
```

If you want a true end-to-end test, install the
[`@modelcontextprotocol/inspector`](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
and point it at this server:

```bash
npx @modelcontextprotocol/inspector node /home/z/my-project/skills/mcp-server/index.js
```

## Register with Claude Desktop

Edit
`~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) — or `%APPDATA%\Claude\claude_desktop_config.json` (Windows) — and add
an entry under `mcpServers`:

```jsonc
{
  "mcpServers": {
    "skillstack": {
      "command": "node",
      "args": [
        "/home/z/my-project/skills/mcp-server/index.js"
      ],
      "env": {
        // Optional: override the skills root. Defaults to the parent of the
        // mcp-server folder, which is /home/z/my-project/skills.
        "SKILLS_ROOT": "/home/z/my-project/skills"
      }
    }
  }
}
```

Restart Claude Desktop. The four `list_skills` / `search_skills` /
`get_skill` / `route_task` tools will now appear in the tool palette inside
any conversation.

> **Tip:** Use the **absolute path** to `index.js`. Claude Desktop does not
> expand `~` or relative paths reliably.

## Register with Cursor

Edit `.cursor/mcp.json` in your project (or the global one at
`~/.cursor/mcp.json`) and add the same entry under `mcpServers`:

```jsonc
{
  "mcpServers": {
    "skillstack": {
      "command": "node",
      "args": [
        "/home/z/my-project/skills/mcp-server/index.js"
      ]
    }
  }
}
```

Reload the Cursor window (`Cmd/Ctrl-Shift-P` → "Developer: Reload Window")
and verify the server shows up under **Settings → MCP** with a green dot.

## Test commands

Once registered, ask the client things like:

| Prompt                                                             | Expected tool call                                                                                                         |
|--------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| *"What skills does SkillStack have?"*                              | `list_skills`                                                                                                              |
| *"Find anything related to Optuna"*                                | `search_skills(query="Optuna")`                                                                                            |
| *"Get the journal-manuscript-writer skill from academic-research"* | `get_skill(theme="academic-research", skill_name="journal-manuscript-writer")`                                             |
| *"Draft a methods section in LaTeX"*                               | `route_task(task_description="Draft a methods section in LaTeX")` → suggests `academic-research/journal-manuscript-writer` |
| *"Audit my LLM outputs for bias"*                                  | `route_task(...)` → suggests `ai-output-judgement/bias-auditor`                                                            |

### Manual JSON-RPC test

You can also send a raw JSON-RPC request over stdio:

```bash
(echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.0.0"}}}'; \
 echo '{"jsonrpc":"2.0","method":"notifications/initialized"}'; \
 echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_skills","arguments":{}}}'; \
 sleep 1) | node /home/z/my-project/skills/mcp-server/index.js
```

You should see the `initialize` response, then the `list_skills` tool result
printed as a JSON-RPC `result` envelope containing the 167 indexed skills
(the maestro orchestrator itself is excluded from the listing).

## Layout

```
mcp-server/
├── package.json    # name: skillstack-mcp, type: module, bin: ./index.js
├── index.js        # MCP server (stdio transport)
├── README.md       # this file
└── .gitignore      # node_modules/, *.log
```

## Author & license

- **Author:** Hossam Magdy Balaha
- **License:** MIT — same as the rest of SkillStack.
- **Skill count:** 168 skills across 9 themes (the MCP server excludes
  `maestro/SKILL.md` itself from `list_skills` because it is the router, not
  a skill to invoke).

## Troubleshooting

- **`Cannot find module '@modelcontextprotocol/sdk'`** → you forgot
  `npm install`. Run it once inside `mcp-server/`.
- **Claude Desktop shows the server in red** → check the path is absolute
  and points at `index.js` (not the directory). Check `node` is on `PATH`
  for the user Claude Desktop runs as.
- **`list_skills` returns an empty array** → the server could not find any
  `SKILL.md` files. Make sure the `skills/` folder sits next to
  `mcp-server/`, or set the `SKILLS_ROOT` env var to its absolute path.
