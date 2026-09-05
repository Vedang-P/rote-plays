# DESIGN — contribution-ready (working title)

Play #2 in the vedang collection. "Is this open source repo alive and welcoming PRs?" — profiled from the GitHub API before you invest a single hour writing a PR.

Mission: **profile an upstream repo from `owner/repo` and say, with graded honesty, whether an outside contributor's PR gets merged.**

## Ideation log — description draft (registry register)

> Before you write a PR to a repo you don't own, this profiles the upstream project from the public GitHub API and answers the one question that decides the effort: will they merge my PR? A 3-call civic read (archived? dead for 12 months? committers?) exits early on clearly dead repos; alive repos get a deep dive into outsider throughput (are non-committer PRs actually getting merged?), maintainer response presence, friction (CI, CLA, templates) and the good-first-issue onramp. Returns a GO / AVOID / UNSURE verdict with the single scorecard that decided it, plus a concrete next action — onramp issue links when it's a go, a test-the-water docs PR or a stated evidence gap when it's not. Never a score, always evidence: every signal carries its endpoint and timestamp; anything the API can't answer is reported indeterminate, never guessed. Read-only, zero credentials, github.com only, ~9-11 calls, needs only python3.

## Seat & scope

- Seat: the outside contributor deciding where to spend effort. (Not a hackathon judge, not local-clone disk triage.)
- Verdict axis: **will they merge MY PR?** — maintainer-welcoming weighted.
- Substrate: GitHub REST API, github.com only.
- Auth: **public REST only, zero credentials, no gh login dependency.** Budget ≈ 10-15 calls/project; this is the hard constraint everything else obeys.

## Decisions log

| # | Decision | Status |
|---|---|---|
| D1 | Verdict optimizes "will they merge my PR" | locked |
| D2 | Evidence via GitHub API (gh/REST), input is `owner/repo` | locked |
| D3 | Public REST only; no credentials in the play (house style) | locked |
| D4 | github.com only; no GHES/api_base_url parameter | locked |
| D5 | Two-stage: shallow civic read (few calls, early exit) → deep dive only when alive+welcoming | locked |
| D6 | Verdict language GO / AVOID / UNSURE, flip disclosed | locked |
| D7 | Design persists here, one step per ideation round | locked |
| D8 | Probe map: 3-call stage 1 (civic read) → ~6-call stage 2 (deep dive); ≈9-11 total | locked |
| D9 | Outsider-merge window fixed at 180d; low-volume (<5 merged PRs in window) → thin-data rule: cannot prove throughput either way → UNSURE | locked |
| D10 | Output contract: canonical compare-ready JSON (uniform 3-value grade enum on every scorecard + verdict), presentation a thin layer; composable for a future rank-N-repos sibling play | locked |
| D11 | Every run terminates in `next`: a concrete action with evidence pointer (onramp links for GO, test-the-water path + evidence gap for UNSURE) | locked |
| D12 | Input normalization: `owner/repo` | full URL | git remote form → canonical casing from S1-1. Params: repo, report (findings/all), api_timeout+retry cap | locked |
| D13 | Rate limits: 403+Retry-After is a first-class failure → per-card `indeterminate`, run survives; per-IP bucket disclosed | locked |
| D14 | Self-check fixtures = recorded real API responses trimmed to the read field set, replayed through an injected transport; corpus covers GO/AVOID/UNSURE + dead-repo early exit | locked |
| D15 | Bot-exclusion rule (found live-testing GSoC orgs): bot PRs (dependabot/renovate/github-actions, incl. plain logins) carry no maintainer-response signal and are excluded from throughput + response samples, counted and disclosed | locked |
| D16 | Response presence pairs with acceptance rate (merged share of the sampled closed PRs, already fetched): presence>=50% OR (acceptance>=60% AND presence>=25%) -> GO; silent+rejecting -> AVOID. A project that reviews via approvals looks quiet but merges — silence+merge is engagement | locked |

## The profile schema (5 scorecards)

| # | Scorecard | Signals | Weight |
|---|---|---|---|
| 1 | Maintainer response | *response presence* (downgraded, see honesty rule): did merged/closed PRs get any review/comment; latency unavailable within budget → named downgrade | high |
| 2 | Outsider throughput | % merged PRs from non-committer authors, first-time-author merges (90d), outsider PR open→merged days | high |
| 3 | Friction | CI required on main (branch protection), CLA/DCO gates, PR template, CONTRIBUTING presence | medium |
| 4 | Onramp | `good first issue` / `help wanted` open counts + age, assigned vs unassigned | medium |
| 5 | Vitality (context) | commit cadence, last release, committer count/bus factor, archived flag, abandonment note | context only |

Maintainer identity: derived from `/contributors`; "outsider" = PR author not in committers. Every signal carries raw evidence. Unanswerable → `indeterminate`, never guessed.

## Verdict algebra

Decision rules, not a weighted sum (no fake precision). Bottom line + **which single scorecard flipped it**.

- **GO** — response presence ok AND outsiders merged recently AND friction low
- **AVOID** — archived, ~12mo no commits, or response presence near zero
- **UNSURE** — everything else: evidence too thin in both directions, merges happen but not provably for outsiders, or friction heavy → test-the-water PR first; state exactly what would change the verdict

## Honesty rules (house style)

1. **Metric-downgrade rule:** when the textbook metric needs N+1 calls, measure the downgraded sibling and *name the downgrade* in the profile. A labeled approximation beats a silently dropped — or faked — scorecard.
2. `indeterminate`, never guessed. (paper-brief lineage)
3. Degrade each scorecard separately; a failed source labels the card, not the whole run.
4. Evidence lines carry the API endpoint + timestamp behind each claim.

## Two-stage probe architecture

### Stage 1 — civic read (3 calls; dead repos exit here)

| # | Endpoint | Extracts | Early exit |
|---|---|---|---|
| S1-1 | `GET /repos/{o}/{r}` | archived, license, pushed_at, created_at, open counts, default branch | 404/403 → fatal (not found/private); archived → AVOID |
| S1-2 | `GET /repos/{o}/{r}/commits?per_page=1&sha={default}` | true last-commit date (pushed_at lies: PRs push it) | no commit ≥12mo → AVOID |
| S1-3 | `GET /repos/{o}/{r}/contributors?per_page=100` | committer set (outsider derivation seed) + bus factor | — |

Dead repo = 3 calls total. Alive repos proceed.

### Stage 2 — deep dive (~6 calls)

| # | Endpoint | Scorecard |
|---|---|---|
| D2-1 | `GET /repos/{o}/{r}/pulls?state=closed&sort=updated&per_page=100` | outsider throughput + response presence (author_association, merged_at, comments, review_comments per PR) |
| D2-2 | `GET /repos/{o}/{r}/git/trees/{default}?recursive=0` | friction + onramp files in one glance (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, .github/) |
| D2-3 | `GET /repos/{o}/{r}/labels?per_page=100` | disambiguates "label absent" vs "zero labelled issues" |
| D2-4 | search `repo:o/r type:pr is:merged merged:>=180d` | windowed merge velocity + last-merge date |
| D2-5 | `GET /repos/{o}/{r}/branches/{default}/protection` | 404 = unprotected = a finding, not an error |
| D2-6 | optional CONTRIBUTING head content | cold-open quality (real guidance vs stub) |

### Disclosures built into the probes

- `author_association` reflects today's role (yesterday's first-timer who became a committer counts as committer) — stated in the profile.
- Window fixed at 180d. <5 merged PRs in window → thin-data rule: throughput is unprovable in either direction.
- `pushed_at` never used as commit truth; S1-2 reads real commits.

## Output contract

Canonical JSON to stdout, compare-ready, presentation layered on top (paper-brief lineage).

```json
{
  "profile": { "repo": "o/r", "as_of": "...", "source": "public REST", "api_calls": 9 },
  "verdict": { "grade": "GO|AVOID|UNSURE", "flip": "<deciding scorecard>", "next": "concrete next action" },
  "scorecards": {
    "outsider_throughput": { "grade": "...", "signals": [ { "evidence": "...", "endpoint": "...", "ts": "..." } ] },
    "maintainer_response":  { "grade": "...", "signals": [...] },
    "friction":             { "grade": "...", "signals": [...] },
    "onramp":               { "grade": "...", "signals": [...] }
  },
  "vitality": { "context only, never graded" },
  "stage": { "ran": "stage_1|stage_2", "exit_reason": "..." }
}
```

- Uniform 3-value grade enum (GO/AVOID/UNSURE) on every scorecard → machine-comparable; future rank-N sibling consumes directly.
- Every signal carries endpoint + timestamp; evidence-bounded, no unsourced claims.
- `next` on every terminal: GO → live onramp links; UNSURE → test-the-water PR path + what evidence flips it; AVOID → nothing.

## House-style compliance checklist (paper-brief bar)

- [ ] Single main.ts, rote frontmatter, step DAG: selfcheck → validate → stage gates → parallel probes
- [ ] Presentation fixtures per step; bundled self-check with real case fixtures
- [ ] Read-only, no credentials, needs only python3 (stdlib urllib — no deps.toml additions if possible)
- [ ] `rote play lint` clean, quality score 1.00, fixture-transcript replay for every probe
- [ ] Tags in domain/job/tool/effect/audience shape
- [ ] Parameters: repo (required), report depth knob, api timeout/caps

## Open questions board

- ~~Q1. Stage-1 vs stage-2 exact probe map + early-exit conditions + call budget accounting~~ — resolved as D8/D9 above
- Q2. Parameters + output contract (JSON shape, presentation variants, composability) — resolved: D10/D11
- ~~Q3. Input normalization~~ — resolved: D12
- ~~Q4. Self-check + verification fixture set~~ — resolved: D13/D14
- ~~Q5. Name, tags, description draft~~ — resolved: contribution-ready
- ~~Q6. Registry publication + README/code repo checklist~~ — resolved: build checklist above

## Identity (Q5 — resolved)

- **Name:** `contribution-ready` (matches README roadmap slot, verb-y readiness convention)
- Tags: `domain-open-source` `job-contribution-research` `tool-github-api` `effect-read-only` `audience-contributors`
- Description: see draft in the ideation log above (registry register, evidence-bounded).

## Build checklist (Q6 — resolved as plan)

1. [x] Scaffold `contribution-ready/` mirroring paper-brief layout: main.ts frontmatter step DAG, resources/analyze.py, presentation-fixtures per step, selfcheck.
2. [x] Record + trim frozen fixtures from 8 reference repos (GO prettier/checkstyle · UNSURE ky/wagtail/dart · AVOID archived/dead/OpenELIS + build corpus).
3. [x] Implement analyzer: normalize input → stage 1 gates → stage 2 probes → grade algebra → canonical JSON.
4. [x] Implement presentation layer (findings/all) as deprivileged renderer.
5. [x] Self-check asserts graded honesty under transcripts (thin-data not GO; archived not past stage 1). 34/34 passing.
6. [x] `rote play lint` clean, quality gate passed.
7. [x] Release local → rebuild index → search verify.
8. [x] Registry publish → **vedang/contribution-ready@0.1.0** public, canonical, play_run_eligible, execution_verification: passed (published-reference acceptance run: prettier → GO).
9. [x] Code repo `rote-contribution-ready` on GitHub + push source (https://github.com/Vedang-P/rote-contribution-ready).

## Publication record

- Play URI: https://play.modiqo.ai/vedang/contribution-ready@0.1.0
- Bootstrap: https://play.modiqo.ai/install?play=vedang/contribution-ready@0.1.0
- Run reference: `rote play run https://play.modiqo.ai/vedang/contribution-ready@0.1.0 repo=<owner/repo> --yes`
- Visibility: public · execution: anyone can resolve and run (process work, disclosed before execution)
- Package: 371KB (tree transcripts slimmed to queried paths + entry counts; was 9.4MB)
