# LangChain Docs + MCP Integration Guide (for this project)

This guide connects your AI tooling to official LangChain docs so answers stay current.

## 1) Documentation index (official)

Primary index:
- https://docs.langchain.com/llms.txt

MCP endpoint:
- https://docs.langchain.com/mcp

Why this matters:
- `llms.txt` gives machine-readable page inventory.
- MCP gives real-time documentation retrieval for assistants.

## 2) Add LangChain docs MCP to your tools

### Codex CLI (global)
```sh
codex mcp add langchain-docs --url https://docs.langchain.com/mcp
```

### VS Code MCP settings
Use your MCP settings JSON and add:

```json
{
  "servers": {
    "docs-langchain": {
      "url": "https://docs.langchain.com/mcp"
    }
  }
}
```

### Cursor MCP settings
```json
{
  "mcpServers": {
    "docs-langchain": {
      "url": "https://docs.langchain.com/mcp"
    }
  }
}
```

### Claude Code (project scope)
```bash
claude mcp add --transport http docs-langchain https://docs.langchain.com/mcp
```

### Claude Code (global user scope)
```bash
claude mcp add --transport http docs-langchain --scope user https://docs.langchain.com/mcp
```

## 3) Best docs pages for THIS Python hybrid assistant

Start with these (from the fetched index):

Core Python docs:
- https://docs.langchain.com/oss/python/langchain/overview.md
- https://docs.langchain.com/oss/python/langchain/quickstart.md
- https://docs.langchain.com/oss/python/langchain/models.md
- https://docs.langchain.com/oss/python/langchain/retrieval.md
- https://docs.langchain.com/oss/python/langchain/agents.md

Provider integrations (matches your Groq/Gemini/OpenAI-compatible setup):
- https://docs.langchain.com/oss/python/integrations/providers/groq.md
- https://docs.langchain.com/oss/python/integrations/providers/google.md
- https://docs.langchain.com/oss/python/integrations/providers/openai.md

LangGraph (if you move from rule-router to graph orchestration):
- https://docs.langchain.com/oss/python/langgraph/overview.md
- https://docs.langchain.com/oss/python/langgraph/quickstart.md
- https://docs.langchain.com/oss/python/langgraph/workflows-agents.md

MCP + observability:
- https://docs.langchain.com/oss/python/langchain/mcp.md
- https://docs.langchain.com/oss/python/langchain/observability.md

## 4) How to use docs programmatically in your workflow

Recommended loop:
1. Query MCP for latest docs before implementing provider-specific code.
2. Generate code changes.
3. Re-query MCP for edge cases and migration notes.
4. Validate with local tests.

Prompt template for assistants:
- "Use docs-langchain MCP server. Check current Python provider docs for Groq/Google/OpenAI integrations and give implementation compatible with latest LangChain v1 patterns."

## 5) Mapping to your current project

Current project routing:
- Local simple: llama.cpp
- Local RAG: sentence-transformers + hnswlib
- Complex: Groq
- Long context: Gemini
- Planning: Kimi (OpenAI-compatible API)

LangChain migration path (optional):
- Replace custom cloud router with LangChain model wrappers.
- Keep existing local llama.cpp path for on-device fallback.
- Use LangChain retriever abstractions if you later swap vector DB.

## 6) Security notes

- Do not put MCP or provider secrets in committed files.
- Keep `.env` out of git (already ignored).
- Use project-scoped MCP when testing new tooling.

## 7) Quick verification checklist

- MCP server added successfully in your tool.
- Tool can query docs and return links.
- At least one provider doc page is retrievable.
- Generated code references current docs patterns.

## 8) Automated probe script

Run this script from project root to verify docs index + MCP + critical pages:

```bash
python scripts/check_langchain_docs_mcp.py
```

It prints a JSON report and exits with code `0` on success, `1` on any failed check.

---

If needed, next step is to add a `scripts/check_langchain_docs_mcp.py` helper that verifies MCP connectivity and confirms key pages are reachable.
