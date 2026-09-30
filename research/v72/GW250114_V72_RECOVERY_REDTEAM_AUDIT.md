# GW250114 v72 recovery red-team audit

**Audit date:** 2026-08-17  
**Overall status:** `RECOVERY_REPAIR_VALIDATION_PASS_NO_PHYSICAL_PROMOTION`  
**Scope:** independent review of the recovered v72 methods package and its fixed-conditioning `-7M` raw-grid replay. This is not a physics-result certification.

## Chain of custody

| Artifact | SHA-256 | Audit status |
|---|---|---|
| Canonical v71 standalone | `efe2dcceebc344234eb6d6678f990bc611223219ec2ea3906946fc76fd8abb0b` | `PASS` |
| Canonical v71 master | `a491c495c6ae4910fe747254af60246ae18ca22762a4b4ec35b4872dc0690b3a` | `PASS` |
| Recovered v72 core | `1d0154178d6cf2c478d69fe5fa654957a0e548803c70a26eb19563ea653422d5` | `PASS_AS_RECOVERY_INPUT`; the repaired final v72 archive will necessarily have a different hash |

The recovered core is treated as an auditable input, not as the finished release. The repaired directory passes the repeated `28/28` package audit and the exact `56/56` full-manifest check. The sealed ZIP is verified after manifest freeze; its archive hash is recorded in the external SHA-256 sidecar because an archive cannot contain its own hash.

## Material findings and corrections

1. **One competitor was incorrectly used as if it controlled a symmetric two-sided alternative.** At the historical log-gap
   `delta = 0.004355437628170275`, the one-preregistered-competitor calculation is
   `D = 3.7810604375308374` and `q_eff = 0.0011519090213259128`
   (`0.11519090213259128%`). For two endpoint competitors with a joint success lower bound of `0.90`, Bonferroni control requires
   `D = 4.348686765309588` for each endpoint and `q_eff = 0.001001552391152782`
   (`0.1001552391152782%`). The tables and summaries were corrected to keep these scopes separate. The regenerated math suite reports `17/17 PASS`, and two isolated regenerations are byte-identical across all generated math artifacts.

2. **Detector aliasing is only a local statement here.** The affine/linear calculation diagnoses tangent-space or local aliasing. It does not prove a global exact alias, and a global nuisance-image identification check remains required.

3. **The raw computation is a fixed-conditioning replay, not the full Nature inference.** It evaluates the complete `85 x 40` (`3,400` point) `-7M` grid for two fixed posterior rows on the official H1/L1 strain. It does not reproduce posterior marginalization, uncertainty propagation, model selection, or the complete inference reported by the Nature analysis.

4. **`psi` is recorded but inactive in the replay call.** It is not passed to `qnm_filter`, so no polarization sensitivity or attribution may be claimed from this run. Mass, spin, right ascension, declination, and geocentric time differ between the two row evaluations and move together; the row comparison does not isolate any one of them.

5. **Detector additivity is a diagnostic identity.** The maximum detector/network quadratic additivity discrepancy was `1.1368683772161603e-13`, but this checks implementation arithmetic under the conditioned model; it is not an independent physical validation.

6. **Reproducibility defects were found and repaired.** The recovered raw finalizer hardcoded a Python/Pixi environment and did not fail closed on all input/source checks. The recovered package audit was non-idempotent and did not validate the complete release manifest. The repaired workflow now derives the runtime, binds the source before grid evaluation, compares surfaces by numerical invariants, produces byte-stable repeated package-audit outputs, and verifies the exact full manifest without writing to the package.

## Official-input receipts used in the recovery replay

| Input | SHA-256 | Official MD5 when supplied |
|---|---|---|
| Nature companion ZIP | `752eb33b21ee1a332ad7282eb5ddee695d6cc1ec2859120c779e17fbfcd7c862` | `4874fef35088209c9fa4073f15a27a78` |
| NRSur7dq4 posterior HDF5 | `55b4a47c2c71580e9ef0cd1ff9fa9d32e64813657e9ea31f32e24cda53922d62` | `9b115931b66439a1d5649a2b7b7aa143` |
| H1 4,096 s / 16,384 Hz strain | `23e20dda953d2ede852f4991c018b0f1128f35f2cec7153d835a312be363d19d` | not supplied |
| L1 4,096 s / 16,384 Hz strain | `355dbcaece2b63b5ded9aa353e34b59a672edfd7845b0aa1b9bf73c5439bb825` | not supplied |
| Companion cached `-7M` likelihood surface | `c2f44f586ce256d053f564b512125ea857f519a556f79cbc9c1526da557f0667` | not supplied |

The inspected `qnm_filter` source checkout was commit `55f14436d4ea510b71754b95da9701009e8a1c12`, tree `377f807dd345a138c32d274f3cb746f60dd0cecf`, with a clean tracked state. Binding this source receipt into a fail-closed final replay remains part of the final rebuild gate.

## Fresh independent replay evidence

The recovery audit reran both conditioned rows in a newly installed Python 3.11/Pixi environment using the official files above.

| Conditioned row | Network maximum | H1 maximum | L1 maximum | Fresh-versus-recovered centered network difference |
|---|---|---|---|---|
| Released row `10740` | `200 Hz, 450 s^-1` | `200 Hz, 390 s^-1` | `198 Hz, 510 s^-1` | max abs `3.00217e-7`; RMS `1.62369e-7` |
| Maximum-log-likelihood row `19989` | `200 Hz, 420 s^-1` | `202 Hz, 360 s^-1` | `202 Hz, 480 s^-1` | max abs `1.89396e-7`; RMS `8.69764e-8` |

Both fresh maxima matched the recovered maxima. For released row `10740`, fresh-minus-cache residual diagnostics were: mean `-0.0002365525231`, RMS `3.5098941597e-5`, peak-to-peak `1.5017496935e-4`, and centered maximum absolute difference `7.7343555152e-5`. These are fixed-conditioning reproduction diagnostics only. The packaged preflight, finalizer, and comparator receipts pass `9/9`, `16/16`, and `26/26`, respectively.

## Gate disposition

| Gate | Status |
|---|---|
| Canonical v71 parent integrity | `PASS` |
| Recovered v72 core provenance | `PASS_AS_RECOVERY_INPUT` |
| Corrected composite-separation mathematics | `PASS_17_OF_17_AND_BITWISE_REGENERATION` |
| Fresh official fixed-conditioning `-7M` replay | `PASS_WITH_PACKAGED_9_16_26_RECEIPTS` |
| Full Nature inference | `NOT_REPRODUCED` |
| Runtime/source fail-closed preflight | `PASS` |
| Idempotent package audit and full-manifest verification | `PASS_28_OF_28_AND_56_OF_56` |
| Global nuisance-image distance on a real joint likelihood | `NOT_MEASURED` |
| Detector-disjoint cross-fit / held-out validation | `NEXT_TASK; NOT_EXECUTED` |
| Physical interpretation | `LOCKED` |

The next evidentiary task is a preregistered detector-disjoint cross-fit or other held-out construction that prevents the same detector-conditioned information from serving simultaneously as fit and validation evidence. It must retain the local/global alias distinction and define its target, nuisance images, exclusion region, and error control before execution.

## Claim firewall

This audit does **not** establish a physics discovery; does **not** validate HRF as a physical theory or generative likelihood; does **not** identify `ln(4)` or `g=4`; does **not** establish area quantization, black-hole microstates, or a quantum horizon; and does **not** reproduce the full Nature inference. No repository, publication, or Zenodo claim should be updated from this recovery evidence alone.
