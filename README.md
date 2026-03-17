# UPIP — Universal Process Integrity Protocol

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.19074793.svg)](https://doi.org/10.5281/zenodo.19074793)
[![PyPI](https://img.shields.io/pypi/v/tibet-triage)](https://pypi.org/project/tibet-triage/)

**A self-validating paper: the publication reproduces itself to prove what it claims.**

## What is UPIP?

UPIP is a five-layer protocol for capturing, bundling, and verifying the complete integrity of computational processes across machines.

```
L5  VERIFY   ← Cross-machine verdict
L4  RESULT   ← Output + diff hash
L3  PROCESS  ← Command + intent + actor
L2  DEPS     ← Python + packages + hash
L1  STATE    ← Starting state + hash
```

## Where is the paper?

**Not here.** That's the point.

This repo contains the *source* and the *UPIP bundle* — not the paper itself.
The paper is generated when you reproduce the bundle. If the paper appeared
after cloning, it would prove nothing. The proof is in the reproduction.

### Generate the paper yourself

```bash
pip install tibet-triage>=0.3.0

# Clone this repo
git clone https://github.com/Humotica/upip-protocol.git
cd upip-protocol

# Reproduce — the paper appears
tibet-triage upip-reproduce paper.upip.json

# Read the result
cat paper/PAPER.md
```

If the verification hash matches `71e567acbd716906eec490719a383655eba0f3912550bd2b9235ff3bb3300e1b`, the paper is proven correct on your machine.

> Want to read it without running? See the [Zenodo deposit](https://doi.org/10.5281/zenodo.19074793).

### How it was created

```bash
tibet-triage upip-export -o paper.upip.json -s . \
  --title "UPIP Self-Validating Paper" \
  -- python3 paper/produce_paper.py
```

## Cross-Machine Proof

Tested and verified on:

| Machine | Arch | OS | Python | Verdict |
|---------|------|----|--------|---------|
| JTel-brain (HP DL360) | x86_64 | Debian 13 | 3.13.5 | REPRODUCIBLE |
| OomLlama-HUBby (Lenovo P520) | x86_64 | Debian 12 | 3.11.2 | REPRODUCIBLE |
| Pixel (Android smartphone) | ARM64 | Android 16 | - | REPRODUCIBLE |

Same UPIP stack hash: `upip:1ab5335278960bd5a016bc0b54c9989fb24ab33f1bbcb38e5d91a956d3211d31`

## Repository Structure

```
├── PROTOCOL.md              # Formal UPIP specification (v1.0)
├── paper/
│   └── produce_paper.py     # Deterministic paper generator (source)
├── paper.upip.json          # UPIP bundle — reproduce this!
├── examples/
│   └── fibonacci.py         # Simple example computation
├── LICENSE                  # MIT
└── README.md                # You are here

After reproduction, `paper/PAPER.md` and `paper/VERIFICATION.json` appear.
```

## Protocol Specification

See [PROTOCOL.md](PROTOCOL.md) for the formal five-layer specification.

## Software

```bash
pip install tibet-triage
```

- **PyPI**: https://pypi.org/project/tibet-triage/
- **TIBET Protocol**: https://pypi.org/project/tibet-core/

## License

MIT — Humotica AI Lab, 2026

## Authors

- Jasper van de Meent (jasper@humotica.com)
- Root AI (root_idd@humotica.nl)
