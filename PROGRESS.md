# PROGRESS — env-setup-doctor (play #3)

Status: **paused mid-build** (2026-09-06). Design locked, analyzer + play built,
self-check 44/44, `rote play lint` clean. NOT yet released or published.

## What this play is

One-shot API-key + environment setup audit. Pass `--keys A,B,C` and/or
`--env-example path/to/.env.example`; it checks presence (env + dotenv),
emptiness, placeholders, provider shapes, and — opt-in via `probe=true` —
live-verifies known keys against their own providers. Returns READY/GAPS plus
a copy-paste export block for the gaps. Values are never echoed.

## Locked decisions

- D1: inputs = explicit `--keys` list AND `--env-example` parse (either suffices)
- D2: local checks + **opt-in** live probes (`probe=true`; GET-only, own provider, 15s timeout)
- D3: report + printed snippet only — the play writes no files, sends nothing anywhere

## Built (in `env-setup-doctor/`)

- `main.ts` — frontmatter DAG (selfcheck → validate → scan/live in parallel) + presentation renderer
- `deps.toml` — python3 only, stdlib, no network deps
- `resources/analyze.py` — normalize, dotenv parse, placeholder/shape tables, verdict algebra, live probes, self-check
- `resources/selfcheck/cases.json` — 44 cases incl. the anti-leak invariant (no raw secret in output, no value/secret fields in schema)
- `resources/presentation-fixtures/{selfcheck,validate,scan,live}/` — deterministic (fake `CRD_FIXTURE_*` names + `sample.env`)
- Live probe table v1: OPENAI_API_KEY, ANTHROPIC_API_KEY, GITHUB_TOKEN, GH_TOKEN

## Fixes applied during build (do not regress)

- F1: `--probe` was overloaded as step selector + true/false flag → split into `--probe <scan|live>` + `--do-probe <true|false>`
- F2: SHAPE_TABLE order — `sk-ant-` must precede `sk-` (longest prefix first)
- F3: fixture `timeout_ms` must exactly match each step's declared timeout (validate/scan 30000, selfcheck/live 60000)
- F4: frontmatter YAML — no nested single-quotes inside single-quoted strings (broke the `probe` description)

## Left to do (resume here)

1. Live tests: real GAPS run, fatal case (no keys → validate exit 2 → BLOCKED), `probe=true` run
   (env here has HF_TOKEN + ANTHROPIC_* names — probe only with explicit say-so; never print values)
2. Install to `~/.rote/flows/env-setup-doctor/` + `deno.json {"version":1}`, lint, `rote play release`
3. `rote play index --rebuild`, search-verify
4. Registry: whoami → `registry play info vedang/env-setup-doctor` → dry-run push → public push → inspect + acceptance run
5. README row #3 + roadmap checkbox in `rote-plays/README.md`; code repo `Vedang-P/rote-env-setup-doctor`
6. House bar to meet: lint clean (done), score 1.00 (unmeasured), 34+ self-check (44 passing)

## Related

- Roadmap slot: `rote-plays/README.md` (`env-setup-doctor` — still unchecked)
- Precedent: `vedang/contribution-ready@0.1.0` (same lifecycle: lint → flows copy → release → index → push → verify)
