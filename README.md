# Rote Plays by [@vedang](https://play.modiqo.ai)

Reusable, inspectable procedures built for the [Rote Playoffs Hackathon](https://www.modiqo.ai/blog/the-playoffs) (Sep 1–6, 2026). Every Play below runs through `rote play run`, carries a birth certificate, and is verified before it ships.

**Author:** Vedang Pandey · Rote handle `vedang` · GitHub [@Vedang-P](https://github.com/Vedang-P)

## The collection

| # | Play | What it does | Code | Registry |
|---|---|---|---|---|
| 1 | **paper-brief** | Evidence-bounded research paper briefs: abstract, section map, every metric with dataset + task, novelty claims quoted verbatim | [rote-paper-brief](https://github.com/Vedang-P/rote-paper-brief) | `vedang/paper-brief` |

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

- [x] **paper-brief** — research paper briefs (shipped)
- [ ] **contribution-ready** — is this OSS repo alive? PR-worthiness verdict
- [ ] **env-setup-doctor** — one-shot API-key + environment setup audit
- [ ] **session-handoff** — uniform cross-session workflow brief
- [ ] **venue-eligibility** — workshop/conference fit + eligibility check
- [ ] **model-radar** — new model drop summary + benchmark context

## License

Each Play repo carries its own LICENSE (MIT).
