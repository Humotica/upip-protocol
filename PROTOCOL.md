# UPIP — Universal Process Integrity Protocol

**Version:** 1.0
**Date:** 2026-03-17
**Authors:** J. van de Meent, R. AI (Humotica AI Lab)
**Status:** Draft Specification

## 1. Purpose

UPIP defines a five-layer protocol for capturing, bundling, and verifying
the complete integrity of a computational process — from starting state through
execution to cross-machine reproduction.

The protocol answers one question with cryptographic certainty:

> **"Given the same starting state, do I get the same result?"**

## 2. Design Principles

1. **State before process.** You cannot reproduce what you cannot define.
2. **Layers are independent.** Each layer produces its own hash.
3. **The stack is immutable.** Once exported, a UPIP bundle never changes.
4. **Verification is execution.** The only way to verify is to reproduce.
5. **The protocol is the proof.** A UPIP paper validates itself by existing.

## 3. The Five Layers

```
┌─────────────────────────────────────────┐
│  L5  VERIFY   Cross-machine verdict     │
├─────────────────────────────────────────┤
│  L4  RESULT   Output + diff hash        │
├─────────────────────────────────────────┤
│  L3  PROCESS  Command + intent + actor  │
├─────────────────────────────────────────┤
│  L2  DEPS     Python + packages + hash  │
├─────────────────────────────────────────┤
│  L1  STATE    Starting state + hash     │
└─────────────────────────────────────────┘
```

### L1 — STATE (Starting State)

Captures the complete starting state before any process runs.

| Field | Type | Description |
|-------|------|-------------|
| `state_type` | enum | `git`, `files`, `image`, `empty` |
| `git_commit` | string? | Full commit SHA (if git) |
| `git_branch` | string? | Branch name (if git) |
| `git_dirty` | bool? | Uncommitted changes present (if git) |
| `file_manifest` | dict | `{path: sha256}` for every file |
| `state_hash` | string | Canonical hash of starting state |

**State hash format:**
- Git: `git:<commit_sha>`
- Files: `files:<sha256 of sorted manifest>`
- Image: `image:<digest>`
- Empty: `empty:0`

**Auto-detection:** If a `.git` directory is present, use git mode.
Otherwise, compute file manifest of all files in source directory.

### L2 — DEPS (Dependencies)

Freezes the exact dependency environment.

| Field | Type | Description |
|-------|------|-------------|
| `python_version` | string | e.g., `3.13.5` |
| `packages` | list | `[{name, version}]` from pip freeze |
| `pip_freeze` | string | Raw `pip freeze` output |
| `deps_hash` | string | `deps:<sha256 of freeze output>` |

### L3 — PROCESS (Definition)

Defines what will be executed and why.

| Field | Type | Description |
|-------|------|-------------|
| `command` | string | Shell command to execute |
| `intent` | string | Human-readable purpose |
| `actor` | string | Who/what initiated this |
| `timeout` | int? | Max seconds (optional) |
| `env_vars` | dict? | Environment overrides (optional) |

### L4 — RESULT (Outcome)

Captures the execution result.

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Process completed without error |
| `exit_code` | int | Process exit code |
| `stdout` | string | Standard output |
| `stderr` | string | Standard error |
| `diff_hash` | string | SHA-256 of file changes |
| `files_added` | list | New files created |
| `files_changed` | list | Modified files |
| `files_removed` | list | Deleted files |
| `result_hash` | string | `sha256:<hash of exit+diff+stdout>` |

### L5 — VERIFY (Cross-Machine Verdict)

Records the result of reproduction on another machine.

| Field | Type | Description |
|-------|------|-------------|
| `machine` | string | Hostname of reproducing machine |
| `timestamp` | ISO 8601 | When reproduction was performed |
| `is_isomorphic` | bool | Results match original |
| `divergence_score` | float | 0.0 = identical, 1.0 = total divergence |
| `environment` | dict | Machine specs (Python, OS, CPU, etc.) |

## 4. Stack Hash

The UPIP stack hash is computed over all five layer hashes:

```
stack_input = f"{L1.state_hash}|{L2.deps_hash}|{L3.command}|{L4.result_hash}"
stack_hash  = "upip:" + sha256(stack_input)
```

This single hash represents the entire process integrity chain.

## 5. Bundle Format

A UPIP bundle is a JSON file with the following structure:

```json
{
  "upip_version": "1.0",
  "title": "Human-readable title",
  "created": "ISO 8601 timestamp",
  "actor": "who created this",
  "stack_hash": "upip:<sha256>",
  "layers": {
    "state": { ... L1 fields ... },
    "deps": { ... L2 fields ... },
    "process": { ... L3 fields ... },
    "result": { ... L4 fields ... },
    "verify": [ ... L5 records ... ]
  }
}
```

## 6. Reproduction Protocol

To reproduce a UPIP bundle:

1. **Load** the bundle JSON
2. **Verify** L1 — check file manifest matches (warn if state diverges)
3. **Compare** L2 — show dependency differences (informational)
4. **Execute** L3 — run the command in an airlock sandbox
5. **Capture** L4 — record result and compute result_hash
6. **Compare** L4 — original result_hash vs reproduction result_hash
7. **Record** L5 — write verification record with machine info

**Verdict:**
- `REPRODUCIBLE` — L4 result hashes match
- `DIVERGENT` — L4 result hashes differ (with divergence details)

## 7. TIBET Integration

UPIP bundles may optionally carry TIBET provenance tokens.
Each layer transition can be recorded as a TIBET action with
full ERIN/ERAAN/EROMHEEN/ERACHTER provenance.

This is not required for the protocol to function.

## 8. Self-Validation Property

A UPIP paper about UPIP can validate itself:

1. The paper is produced by a deterministic script
2. The script is exported as a UPIP bundle
3. Anyone can `upip-reproduce` the bundle
4. The reproduction generates the paper
5. The generated paper describes the protocol that generated it

This circularity is not a flaw — it is the proof.

## 9. Reference Implementation

```
pip install tibet-triage>=0.3.2
```

```bash
# Export a process as UPIP bundle
tibet-triage upip-export -o bundle.upip.json -s ./source/ \
  --title "My Process" -- python3 run.py

# Reproduce on any machine
tibet-triage upip-reproduce bundle.upip.json
```

## 10. License

This protocol specification is released under MIT License.
The protocol itself is free to implement by anyone.

---

*UPIP is part of the TIBET ecosystem — Transparency, Integrity,
Blocking, Evidence, Traceability.*
