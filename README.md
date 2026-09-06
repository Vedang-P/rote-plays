# Rote Plays by [@vedang](https://play.modiqo.ai)

Reusable, inspectable procedures built for the [Rote Playoffs Hackathon](https://www.modiqo.ai/blog/the-playoffs) (Sep 1–6, 2026). Every Play below runs through `rote play run`, carries a birth certificate, and is verified before it ships.

**Author:** Vedang Pandey · Rote handle `vedang` · GitHub [@Vedang-P](https://github.com/Vedang-P)

## The collection

| # | Play | What it does | Code | Registry |
|---|---|---|---|---|
| 1 | **paper-brief** | Evidence-bounded research paper briefs: abstract, section map, every metric with dataset + task, novelty claims quoted verbatim | [rote-paper-brief](https://github.com/Vedang-P/rote-paper-brief) | [vedang/paper-brief@0.1.1](https://play.modiqo.ai/vedang/paper-brief@0.1.1) |
| 2 | **env-setup-brief** | One-shot env + API-key setup briefs discovered from project code (7 languages, compose, README), name-only dotenv census, provider map with console URLs | [rote-env-setup-brief](https://github.com/Vedang-P/rote-env-setup-brief) | [vedang/env-setup-brief@0.1.2](https://play.modiqo.ai/vedang/env-setup-brief@0.1.2) |
| 3 | **contribution-ready** | Will this OSS repo merge MY PR? GO/AVOID/UNSURE verdict profiled from the public GitHub API: outsider throughput, maintainer response, friction, onramp | [rote-contribution-ready](https://github.com/Vedang-P/rote-contribution-ready) | [vedang/contribution-ready@0.1.0](https://play.modiqo.ai/vedang/contribution-ready@0.1.0) |
| 4 | **claim-vs-build** | Asked vs claimed vs built, checked deterministically: file/action/command claims scored against the repo and diff, repo-declared checks executed for real, ASK gaps flagged | [rote-claim-vs-build](https://github.com/Vedang-P/rote-claim-vs-build) | [vedang/claim-vs-build@0.1.0](https://play.modiqo.ai/vedang/claim-vs-build@0.1.0) |
| 5 | **session-handoff** | One-command context transfer across harnesses: sweeps Claude Code, Codex, OpenCode and Hermes session stores for this project, secret-masked excerpts, git join, paste-ready re-entry block | [rote-session-handoff](https://github.com/Vedang-P/rote-session-handoff) | [vedang/session-handoff@0.1.1](https://play.modiqo.ai/vedang/session-handoff@0.1.1) |
| 2 | **contribution-ready** | Will they merge MY PR? Profiles an upstream GitHub repo from the public API: outsider throughput, maintainer response, friction, onramp → GO / AVOID / UNSURE with evidence | [rote-contribution-ready](https://github.com/Vedang-P/rote-contribution-ready) | [vedang/contribution-ready@0.1.0](https://play.modiqo.ai/vedang/contribution-ready@0.1.0) |

## How to run any Play here

1. Install Play once: `curl -fsSL https://getrote.dev/playoffs/install.sh | sh`
2. In your harness (`/play` in OpenCode/Claude/Cursor, `$play` in Codex):
   ```
   /play run vedang/<name> <params>
   ```
3. Play inspects the exact version, shows effects, and asks for pull-and-run approval. Nothing runs without your OK.

## Build standard

Every Play in this collection ships only when it meets all five:

1. **Sharp, universal pain** — a job someone repeats weekly
2. **Safe to run** — read-only where possible; writes and credentials disclosed by name up front
3. **Parameterized** — adapts to fresh inputs, never hardcodes one case
4. **Graded honesty** — ranked findings, explicit UNKNOWNs, stated confidence boundary
5. **Bounded and fast** — caps, timeouts, no unbounded walks

Plus: bundled self-check fixtures that run on every invocation, presentation fixtures per step, `rote play lint` clean, quality score 1.00.

## Roadmap

- [x] **paper-brief** — research paper briefs ([registry](https://play.modiqo.ai/vedang/paper-brief@0.1.1) · [code](https://github.com/Vedang-P/rote-paper-brief))
- [x] **contribution-ready** — is this OSS repo alive? PR-worthiness verdict ([registry](https://play.modiqo.ai/vedang/contribution-ready@0.1.0) · [code](https://github.com/Vedang-P/rote-contribution-ready))
- [x] **env-setup-brief** — one-shot env + API-key setup briefs ([registry](https://play.modiqo.ai/vedang/env-setup-brief@0.1.2) · [code](https://github.com/Vedang-P/rote-env-setup-brief))
- [x] **session-handoff** — cross-harness context transfer ([registry](https://play.modiqo.ai/vedang/session-handoff@0.1.1) · [code](https://github.com/Vedang-P/rote-session-handoff))
- [ ] **venue-eligibility** — workshop/conference fit + eligibility check
- [ ] **model-radar** — new model drop summary + benchmark context

## License

Each Play repo carries its own LICENSE (MIT).
