# Contributing to Swarm2.0

First off: thanks for being here. The fact that you're reading this means you want to make a small (or large) corner of the AI assistant world better, and that's legitimately cool. 🎉

---

## 🧭 Ground Rules

- Be kind. This isn't the place for flame wars about Python vs. Rust.
- Keep it focused. PRs should do one thing well, not twelve things kinda.
- Don't break what works. If the routing logic ran fine before your change, it should run fine after.
- Read the existing code before adding new code. There's a style here — match it.

---

## 🌿 Branching Model

We use a simple trunk-based model:

| Branch | Purpose |
|---|---|
| `main` | Stable, ship-worthy code. Don't push directly. |
| `feature/<short-name>` | New features (e.g. `feature/streaming-responses`) |
| `fix/<short-name>` | Bug fixes (e.g. `fix/discord-pong-missing`) |
| `chore/<short-name>` | Maintenance, deps, docs (e.g. `chore/update-requirements`) |

```bash
# Typical workflow
git checkout main
git pull
git checkout -b feature/your-awesome-thing
# ... make changes ...
git push origin feature/your-awesome-thing
# open a PR
```

---

## 📝 Commit Style

We use [Conventional Commits](https://www.conventionalcommits.org/). No, you don't have to memorize the spec. Just use one of these prefixes:

```
feat:     a new feature
fix:      a bug fix
docs:     documentation changes only
chore:    build, deps, tooling — no production code changes
refactor: code restructuring (not a feat, not a fix)
test:     adding or fixing tests
perf:     performance improvements
```

**Examples:**
```
feat: add streaming response support for /query endpoint
fix: handle Discord PING before signature verification
docs: update GUIDE.md with Windows Task Scheduler steps
chore: bump sentence-transformers to 3.4.1
refactor: extract routing keywords into named constants
```

Keep the subject line under 72 characters. Use the body for *why*, not *what* — the diff already shows what.

---

## 🔀 Pull Requests

- Target `main` (or a specific feature branch if coordinated).
- Title should follow commit style (`feat:`, `fix:`, etc.).
- Description should explain: what you changed, why, and how to test it.
- Link related issues with `Closes #123` or `Fixes #123`.
- Keep PRs small. A 50-line PR gets reviewed in 10 minutes. A 1000-line PR gets reviewed... eventually.

**PR checklist (copy-paste this into your PR description):**
```
- [ ] The code works locally (I tested it)
- [ ] Existing tests still pass (or I updated them)
- [ ] I updated docs/comments if the behavior changed
- [ ] No API keys or secrets in the code
- [ ] Single-worker constraint respected (no multi-process SQLite)
```

---

## 🧪 Testing

Run the end-to-end test script:

```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/test_agent_end_to_end.py
```

Add tests for new functionality where practical. Look at `scripts/test_agent_end_to_end.py` for patterns.

---

## 🔒 Security

Found a security issue? **Don't open a public issue.** Read [SECURITY.md](SECURITY.md) and follow the responsible disclosure process.

---

## 💡 Ideas & Feature Requests

Open a GitHub Issue with the `enhancement` label. Describe what you want, why it's useful, and (if you have ideas) how it might work. Don't be shy — half the best features come from "I wish this thing could..."

---

## 🤝 Code of Conduct

Be excellent to each other. That's it. That's the whole code of conduct.

---

*Questions? Open an issue. Wrong type of question? Still open an issue. We'll figure it out together.*
