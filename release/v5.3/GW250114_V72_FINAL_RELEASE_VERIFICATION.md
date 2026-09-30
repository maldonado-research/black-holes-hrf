# GW250114 HRF v72 — Final release verification

**Date:** 2026-08-17  
**Status:** `PASS`  
**Scope:** release engineering, corrected methods, and fixed-conditioning official-data reproducibility only.

## Sealed archives

| Archive | SHA-256 | Verification |
|---|---|---|
| `HRF_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.zip` | `1dc2f45c53a4341a2ea1da7e72f20dfb616eec27ded50407c9844ba8a859d629` | deterministic second build byte-identical; ZIP CRC pass; extracted manifest `56/56` |
| `GW250114_MASTER_PROGRESS_BUNDLE_v72.zip` | `f1dcdd78c619b8f0e39eace371cda17eb486a2ae9c5257c6672216cd2dbfcc2a` | deterministic second build byte-identical; ZIP CRC pass; extracted manifest `255/255` |

The master preserves all `195/195` files from the checksum-verified canonical v71 master byte-for-byte and embeds the repaired v72 standalone with its own `56/56` manifest pass.

## Final checks

- corrected mathematics: `17/17 PASS`; two isolated regenerations byte-identical;
- fail-closed official-input/runtime/source preflight: `9/9 PASS`;
- fixed-conditioning raw finalizer: `16/16 PASS`;
- fresh-versus-recovered numerical surface comparator: `26/26 PASS`;
- package audit: `28/28 PASS`, with repeated audit outputs byte-identical;
- one named competitor: `D=3.7810604375`, `q_eff<=0.115190902%` at the historical full gap;
- symmetric two-endpoint exclusion: corrected `D=4.3486867653` per endpoint, `q_eff<=0.100155239%` for a 90% joint lower bound.

The raw computation reproduces the declared fixed-conditioning `-7M`, `85x40` grid. It does not reproduce the full Nature inference or its marginalizations. No HRF detection, real `ln(4)`/`g=4` identification, area quantization, black-hole microstate inference, quantum-horizon claim, or discovery claim is admitted.
