# Authenova Development Log — AI Agent Instructions

## Purpose

This file is the development history and engineering memory of the Authenova project.

Every AI coding agent working on this repository MUST read this file before making changes and MUST update it after completing each development iteration.

The development log must reflect the actual state of the repository, not the agent's assumptions, intentions, or predictions.

---

# Non-Negotiable Rule: Never Fabricate

The AI agent MUST NOT fabricate, assume, or claim implementation that does not actually exist.

Do not claim that:

* a feature is implemented when it is only planned
* a model is working when it has not been executed successfully
* an API works when it has not been tested
* a database is connected when the connection has not been verified
* a test passes when the test was not actually run
* a deployment works when it has not been verified
* an algorithm produces accurate results without evidence
* an external service/API is available without verifying it
* a file exists without checking the repository
* a dependency is installed without checking
* a result is correct merely because the code looks correct

If something cannot be verified, explicitly write:

`UNVERIFIED`

or

`NOT TESTED`

or

`NOT IMPLEMENTED`

Never convert an assumption into a fact.

---

# Before Every Development Iteration

The AI agent MUST:

1. Read `README.md`.
2. Read this `devlog.md`.
3. Inspect the current repository structure.
4. Inspect the relevant existing source files before modifying them.
5. Understand the current implementation state.
6. Identify what is already implemented versus what is only planned.
7. Check the current milestone and task scope.
8. Avoid changing unrelated parts of the project.
9. Preserve working functionality unless the requested task explicitly requires changing it.

Do not recreate or overwrite existing functionality without first inspecting it.

---

# During Development

The AI agent should:

* make the smallest appropriate changes
* follow the established project architecture
* reuse existing components and utilities where appropriate
* avoid unnecessary dependencies
* avoid unnecessary architectural complexity
* maintain clear module boundaries
* keep frontend and backend responsibilities separated
* preserve API contracts
* avoid silently changing schemas
* avoid introducing placeholder implementations that look production-ready
* clearly mark TODOs and incomplete functionality

When a requested feature is outside the current milestone, do not implement it unless explicitly instructed.

---

# Verification Requirements

After making changes, the AI agent MUST verify what was changed whenever technically possible.

Examples:

* run the relevant backend tests
* run the relevant frontend checks
* run linting
* run type checking
* start the application when appropriate
* test API endpoints when appropriate
* verify imports
* verify database connectivity when relevant
* inspect generated files
* verify that modified functionality behaves as expected

The agent must distinguish between:

`PASS` — actually verified

`FAIL` — tested and failed

`NOT TESTED` — not executed

`UNVERIFIED` — cannot currently be confirmed

Never use `PASS` without performing the corresponding verification.

---

# After Every Development Iteration

The AI agent MUST update this file.

Each entry must contain:

## Iteration

A sequential iteration number.

## Date

The actual date of the development iteration.

## Milestone

The current milestone.

## Objective

What the iteration was supposed to accomplish.

## Changes Made

Only describe changes that were actually made.

## Files Created

List files that were actually created.

## Files Modified

List files that were actually modified.

## Files Deleted

List files that were actually deleted.

If none:

`None`

## Dependencies Changed

List dependencies that were actually added, removed, or changed.

If none:

`None`

## Verification

Record commands/tests/checks that were actually executed and their results.

Example:

```text
pytest
Result: PASS

npm run build
Result: PASS
```

If something was not tested:

```text
Frontend browser testing: NOT TESTED
```

## Current State

Describe what is actually working now.

Do not describe future functionality as implemented.

## Known Issues

List currently known problems.

If none are known:

`None known`

## Decisions

Record important architectural or implementation decisions made during the iteration.

## Remaining Work

List what still needs to be completed.

## Next Recommended Step

Give one concise recommendation for the next development iteration.

---

# Development Log Format

Use this format for every entry:

```markdown
## Iteration N — YYYY-MM-DD

### Milestone
Milestone X — <milestone name>

### Objective
<actual objective>

### Changes Made
- <verified change>
- <verified change>

### Files Created
- `<path>`

### Files Modified
- `<path>`

### Files Deleted
- `<path>`

### Dependencies Changed
- <dependency/change>
- None

### Verification
- `<command>` — PASS
- `<command>` — FAIL
- `<check>` — NOT TESTED

### Current State
<verified current state>

### Known Issues
- <issue>
- None known

### Decisions
- <decision>

### Remaining Work
- <remaining task>

### Next Recommended Step
<next step>
```

---

# Architectural Discipline

Authenova is being developed as a modular application.

The AI agent MUST preserve the following conceptual boundaries:

```text
Frontend
    ↓
FastAPI API
    ↓
Application / Orchestration Layer
    ↓
Analysis Services
    ├── OCR
    ├── Validation
    ├── Tampering
    ├── Face Verification
    ├── Risk Engine
    └── RAG
    ↓
Persistence / Storage
```

Do not introduce microservices, Kubernetes, message queues, multiple databases, or other major infrastructure unless explicitly requested.

The current project is intentionally scoped as a focused, explainable MVP.

---

# Source of Truth

The actual repository is the source of truth for implementation status.

The development log is the source of truth for development history.

Documentation must never override the actual state of the code.

If documentation says a feature exists but the implementation is missing, report the feature as:

`NOT IMPLEMENTED`

If the code exists but has not been tested, report it as:

`IMPLEMENTED — NOT VERIFIED`

If a feature is partially implemented, describe exactly what works and what does not.

---

# Handling Uncertainty

When uncertain:

1. Inspect the repository.
2. Inspect relevant files.
3. Run an appropriate verification command.
4. If uncertainty remains, state it explicitly.

Never fill missing information with assumptions.

Use language such as:

* `I could not verify this.`
* `This is currently unimplemented.`
* `This exists as a placeholder only.`
* `The code exists but has not been tested.`
* `The dependency is referenced but installation was not verified.`

Accuracy is more important than appearing complete.

---

# Scope Control

The AI agent MUST NOT silently expand the scope of a milestone.

If the requested task is:

`Set up the project structure`

do not additionally implement:

* OCR algorithms
* face recognition
* tampering detection
* RAG
* authentication
* risk scoring
* deployment
* advanced UI

unless explicitly requested.

Create the architectural locations required for future implementation, but clearly distinguish placeholders from working functionality.

---

# Final Rule

At the end of every iteration, the AI agent must leave the repository and `devlog.md` in a state where another developer or AI agent can understand:

1. What existed before.
2. What was changed.
3. What actually works.
4. What was tested.
5. What failed.
6. What remains incomplete.
7. What should be done next.

Never optimize the development log for appearance.

Optimize it for truth, reproducibility, and continuity.

---

# Devlog Management Rule — Authenova

The project has exactly **one development log**:

`devlog.md`

This file is the **single and permanent development history** for the entire Authenova project.

## STRICT RULE — DO NOT CREATE ADDITIONAL DEVLOG FILES

For every development iteration, milestone, feature, bug fix, refactor, or AI-agent session:

**UPDATE THE EXISTING `devlog.md` FILE.**

NEVER create separate development-log files such as `devlog-1.md`, `iteration-1.md`, `progress.md`, or `session-log.md`.

There must always be **one and only one development log:** `/devlog.md`

## Before Every Iteration
1. Check whether `/devlog.md` exists.
2. Read the existing `/devlog.md`.
3. Determine the latest iteration number.
4. Continue the numbering from the latest entry.
5. Do not create a new devlog file.

## After Every Iteration
Append a new entry to the existing `/devlog.md`. Do not overwrite previous entries unless correcting a factual error. Do not create another Markdown file for the iteration.

## DO NOT FABRICATE THE DEVLOG
The development log must describe the **actual repository state**. Use explicit status labels: `PASS`, `FAIL`, `NOT TESTED`, `UNVERIFIED`, `NOT IMPLEMENTED`, `PARTIALLY IMPLEMENTED`.

## DO NOT CREATE DOCUMENTATION JUST FOR THE DEVLOG
Do not create additional `.md` files merely to document an iteration unless explicitly asked.

## Absolute Rule
**ONE PROJECT → ONE DEVLOG → `devlog.md`**

## Iteration 1 — 2026-09-01

### Milestone
Milestone 1 — Foundation & Architecture

### Objective
Restructure the project into a clean, scalable foundation for the final Authenova application without fabricating functionality.

### Changes Made
- Created foundational directory structure for backend and frontend.
- Migrated OCR module into `backend/app/services/ocr/engine.py`.
- Moved OCR sample image into `data/samples/documents/`.
- Moved test script into `scripts/`.
- Removed old `ocr module` directory.
- Created `backend/app/api/routes/health.py` with `/api/v1/health`.
- Updated `backend/app/main.py` to use API routers.
- Created `backend/Dockerfile` and root `docker-compose.yml`.
- Created architecture, development, and API contracts documentation in `docs/`.
- Moved `requirements.txt` to `backend/`.
- Ensured `venv` is untracked in git.

### Files Created
- `backend/app/api/routes/health.py`
- `backend/Dockerfile`
- `docker-compose.yml`
- `docs/architecture.md`
- `docs/api-contracts.md`
- `docs/development.md`
- Multiple `__init__.py` files across backend directories.

### Files Modified
- `backend/app/main.py`

### Files Deleted
- `ocr module` (directory removed, files moved)

### Dependencies Changed
- None

### Verification
- `python3 -m py_compile backend/app/main.py backend/app/api/routes/health.py` — PASS
- `cd frontend && npm install && npm run build` — PASS
- `cd frontend && npm run lint` — FAIL (eslint not found in frontend environment)
- `tree -L 3` (Repository structure check) — PASS
- `git rm -r --cached venv` — PASS (venv was already untracked)
- FastAPI startup check — NOT TESTED
- PostgreSQL connection — NOT VERIFIED
- Docker verification — NOT TESTED

### Current State
The project architecture has been successfully established following the modular design. The frontend React application exists as a shell and builds successfully. The FastAPI backend has a single `/health` endpoint. The Tesseract OCR script exists in `backend/app/services/ocr/engine.py`. Advanced features (tampering, face verification, risk engine, RAG) remain as unimplemented placeholders.

### Known Issues
- Running `npm run lint` in the frontend directory fails because `eslint` command is not found.

### Decisions
- Preserved existing `App.jsx` and `main.jsx` instead of converting to TypeScript to preserve existing functionality as requested.
- Preserved existing `package.json` dependencies rather than adding new ones prematurely.

### Remaining Work
- Fix frontend linting setup (install `eslint` locally in the frontend workspace).
- Verify database connection and FastAPI startup through Docker.
- Implement subsequent milestones.

### Next Recommended Step
Milestone 2 (or fixing the frontend lint setup) to continue building the core capabilities of the application.

## Iteration 2 — 2026-09-04

### Milestone
Milestone 2 — Core API & Screening Orchestration

### Objective
Complete the remaining API mock endpoints, wire them into the FastAPI app, add the integration orchestrator service, write an end-to-end integration test suite, and perform final validation on a live server instance.

### Changes Made
- Added 8 API route modules (upload, extraction, validation, tampering, face, risk, report, screening) under `backend/app/api/routes/`.
- Wired all 9 routers (including the pre-existing `health`) into `backend/app/main.py` under the `/api/v1` prefix.
- Removed the inline `/health` and `/upload-document` handlers from `main.py`; both are now served by their dedicated routers (`health.router`, `upload.router`).
- Added `backend/app/services/orchestrator/pipeline.py` — the `ScreeningPipeline` service that chains Upload → OCR → Validation → Tampering → Face → Risk → Report using a generated `document_id`.
- Added the `/api/v1/screen` (full pipeline) and `/api/v1/results/{document_id}` (retrieval) endpoints.
- Added Pydantic schemas for all endpoints (upload, extraction, validation, tampering, face, risk, report) under `backend/app/schemas/`.
- Added `pytest` and `httpx` to `backend/requirements.txt`.
- Added `backend/tests/test_api.py` with 10 integration tests covering all endpoints plus the full screening pipeline.

### Files Created
- `backend/app/api/routes/extraction.py`
- `backend/app/api/routes/face.py`
- `backend/app/api/routes/report.py`
- `backend/app/api/routes/risk.py`
- `backend/app/api/routes/screening.py`
- `backend/app/api/routes/tampering.py`
- `backend/app/api/routes/upload.py`
- `backend/app/api/routes/validation.py`
- `backend/app/services/orchestrator/pipeline.py`
- `backend/tests/__init__.py`
- `backend/tests/test_api.py`

### Files Modified
- `backend/app/main.py`
- `backend/requirements.txt`

### Files Deleted
- None

### Dependencies Changed
- Added `pytest>=8.0.0` and `httpx>=0.27.0` to `backend/requirements.txt` (testing-only).

### Verification
- `./venv/Scripts/python.exe -m pytest tests/test_api.py -v` (from `backend/`) — PASS (10 passed in 0.67s)
- FastAPI live startup via `./venv/Scripts/python.exe -m uvicorn app.main:app --port 8011` (background run on Windows, no nohup) — PASS
- `GET /` — PASS (returns "Authenova API is running", version 0.1.0)
- `GET /api/v1/health` — PASS (`{"status":"healthy"}`)
- `GET /openapi.json` — PASS (all 10 paths registered)
- `GET /docs` (Swagger UI) — PASS (HTTP 200)
- `POST /api/v1/upload-document` (multipart) — PASS
- `POST /api/v1/extract-data` — PASS (returns `TEST USER`, `ocr_confidence` 0.94)
- `POST /api/v1/validate-document` — PASS (`is_valid_format=True`)
- `POST /api/v1/detect-tampering` — PASS (`tampering_score` 0.18)
- `POST /api/v1/verify-face` — PASS (`verification_status` `high_similarity`)
- `POST /api/v1/calculate-risk` — PASS (`risk_level` low)
- `POST /api/v1/screen` (end-to-end pipeline, real sample upload of `data/samples/documents/test_document.png`) — PASS (returned `DOC-03F23ECB`, status completed)
- `GET /api/v1/results/DOC-03F23ECB` — PASS (full report with all module results)
- `GET /api/v1/screening-report/DOC-001` — PASS
- `git diff --cached` review of all staged files — PASS
- Frontend browser testing — NOT TESTED (no frontend changes in this iteration)

### Current State
The FastAPI backend now exposes the complete document-screening API surface under `/api/v1`:
`/health`, `/upload-document`, `/extract-data`, `/validate-document`, `/detect-tampering`, `/verify-face`, `/calculate-risk`, `/screening-report/{document_id}`, plus the integrated `/screen` (full pipeline) and `/results/{document_id}`. All responses are currently mock data served through real Pydantic schemas and a working `ScreeningPipeline` orchestrator that stores per-screening results in memory keyed by `document_id`. The integration test suite (10 tests) passes and the live server was exercised end-to-end.

### Known Issues
- All analysis modules (OCR, validation, tampering, face, risk) return hard-coded mock data; they are NOT connected to the actual detection services yet.
- Screening results are stored in-memory only and are lost on server restart.
- The `temp_validation` directory exists in `backend/` (pre-existing, untracked); its contents were not inspected in this iteration.
- Frontend remains a shell that does not yet consume these endpoints.

### Decisions
- Kept all endpoints as mock implementations behind real schemas so the API contract is stable and testable before real services replace them, matching the "no fabrication / placeholder must be clearly marked" rule.
- Used `document_id` as the single connecting identifier across the whole pipeline, exposing it to clients as the handle for retrieving screening results.
- Chose to verify the server via a background uvicorn run on a non-default port (8011) after the previous Unix-style nohup attempt failed on Windows with `cygheap read copy failed` / `Win32 error 299`; this approach succeeded and no repository code was changed to accommodate it.

### Remaining Work
- Connect each pipeline stage to a real service (OCR via `backend/app/services/ocr/engine.py`, validation, tampering, face verification, risk scoring).
- Persist screening results beyond in-memory state (e.g., the planned PostgreSQL layer).
- Wire the frontend to consume `/api/v1/screen` and `/api/v1/results/{document_id}`.
- Expand test coverage for error and validation-failure paths.

### Next Recommended Step
Replace the mock pipeline stages one at a time with the actual analysis services, starting with OCR, keeping the existing API contract intact.
