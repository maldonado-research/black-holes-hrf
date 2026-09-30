# HRF v72 — Composite closure, least-favorable separation, and raw replay

**Project:** GW250114 Quantized Horizon Response / branch-control program  
**Version:** v72  
**Date:** 2026-07-12  
**Status:** mathematical/statistical methods and official-data reproducibility only; **no detection or discovery claim**.

## Main result

v72 advances two independent fronts.

1. It closes the composite-alternative loophole. When the full observable laws are total-variation continuous along an admitted punctured-alternative nuisance path—as in the stipulated common-fixed-covariance Gaussian mean model—a point target such as `tau=ln(4)` has zero uniform separation from the unrestricted continuum `tau != ln(4)`. For randomized tests, the minimax maximum of type-I and worst-alternative type-II error is exactly `1/2`. A uniformly separated continuous-`tau` classification gate therefore requires a preregistered indifference gap/exclusion radius; interval/equivalence inference instead needs its own declared coverage or type-I semantics, and a Bayesian comparison needs a normalized prior with scale sensitivity.
2. It executes the complete fixed-conditioning `-7M`, `85x40` frequency–damping grid on official H1/L1 discovery-v1 strain. The raw network grid reproduces the released cached maximum within the declared numerical tolerance, and the conditional H1/L1 quadratic contributions add to the network value at machine precision under common released parameters and preprocessing. This does not reproduce the Nature paper's full marginalization, template/SNR inference, or other start-time lanes. These are implementation/reproducibility results, not detector-only inference or HRF branch evidence.

The released posterior-density proxy and the maximum-likelihood released row produce materially different surface shapes and damping maxima. Detector-specific remnant/QNM inference, an HRF generative likelihood, global nuisance-image distances, and nonregular-null calibration remain unexecuted. The physical interpretation is locked.

`GW250114_V72_math_summary.json` is intentionally scoped to the deterministic no-strain math subpackage; its `raw_detector_factorization=NOT_EXECUTED` entry describes that module only. The integrated raw status is recorded in `GW250114_V72_summary.json` and `GW250114_V72_gate_status.csv`.

```text
UNRESTRICTED_CONTINUOUS_TAU_UNIFORM_GATE_EXACT_FAIL
FINITE_COMPOSITE_LEAST_FAVORABLE_FRAMEWORK_PASS_METHOD_ONLY
TWO_OBSERVABLE_OPTIMAL_DESIGN_THEOREM_PASS_METHOD_ONLY
OFFICIAL_RAW_MINUS7M_NETWORK_SURFACE_REPRODUCTION_PASS
CONDITIONAL_RAW_DETECTOR_QUADRATIC_ARITHMETIC_ADDITIVITY_PASS
POINT_SELECTION_SENSITIVITY_MATERIAL_NOT_RESOLVED
DETECTOR_SPECIFIC_REMNANT_INFERENCE_NOT_EXECUTED
HRF_GENERATIVE_LIKELIHOOD_NOT_EXECUTED
NONREGULAR_NULL_NOT_CALIBRATED
PHYSICAL_INTERPRETATION_LOCKED
```

## Read first

1. `GW250114_V72_ONE_PAGE_CERTIFICATE.md`
2. `GW250114_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.md`
3. `GW250114_V72_THEOREM_AND_PROOF.md`
4. `GW250114_V72_RAW_MINUS7M_REPLAY_AUDIT.md`
5. `GW250114_V72_gate_status.csv`
6. `GW250114_V72_OBSERVABLE_COMPLETION_CANDIDATES.csv`
7. `GW250114_V72_NEXT_TASK.md`

## Reproduce the deterministic mathematics

```bash
python gw250114_v72_composite_closure_design.py --outdir reproduced_math --strict
```

## Reproduce the raw replay

The official strain, posterior, Nature companion ZIP, and cached `-7M` grid are not duplicated in this package. Their hashes and official source pages are recorded in the raw audit and `SOURCES.md`. The separate NRSur7dq4 waveform asset is not used or certified by this fixed-grid replay.

```bash
# Verify the Nature ZIP against SOURCES.md, then expose its pinned local source.
unzip GW250114_horizon_signatures.zip \
  'GW250114_horizon_signatures/qnm_filter_code/*' -d companion_source
cp -R companion_source/GW250114_horizon_signatures/qnm_filter_code .

pixi install --frozen
mkdir -p reproduced_raw
cp pixi.lock pixi.toml \
  gw250114_v72_raw_preflight.py \
  gw250114_v72_raw_minus7m_replay.py \
  gw250114_v72_raw_minus7m_finalize.py \
  gw250114_v72_raw_surface_compare.py reproduced_raw/

pixi run python gw250114_v72_raw_minus7m_replay.py \
  --posterior posterior_samples_NRSur7dq4.h5 \
  --h1 H-H1_GWOSC_O4b_16KHZ_R1-1420877824-4096.hdf5 \
  --l1 L-L1_GWOSC_O4b_16KHZ_R1-1420877824-4096.hdf5 \
  --cached DW_ftau_-7.0M.h5 \
  --nature-zip GW250114_horizon_signatures.zip \
  --lock pixi.lock \
  --toml pixi.toml \
  --qnm-filter-source qnm_filter_code \
  --pixi-bin "$(command -v pixi)" \
  --only-mode released_logL_plus_logprior \
  --outdir reproduced_raw

pixi run python gw250114_v72_raw_minus7m_replay.py \
  --posterior posterior_samples_NRSur7dq4.h5 \
  --h1 H-H1_GWOSC_O4b_16KHZ_R1-1420877824-4096.hdf5 \
  --l1 L-L1_GWOSC_O4b_16KHZ_R1-1420877824-4096.hdf5 \
  --cached DW_ftau_-7.0M.h5 \
  --nature-zip GW250114_horizon_signatures.zip \
  --lock pixi.lock \
  --toml pixi.toml \
  --qnm-filter-source qnm_filter_code \
  --pixi-bin "$(command -v pixi)" \
  --only-mode maximum_log_likelihood_released_row \
  --outdir reproduced_raw

pixi run python gw250114_v72_raw_minus7m_finalize.py \
  --outdir reproduced_raw \
  --nature-zip GW250114_horizon_signatures.zip \
  --posterior posterior_samples_NRSur7dq4.h5 \
  --h1 H-H1_GWOSC_O4b_16KHZ_R1-1420877824-4096.hdf5 \
  --l1 L-L1_GWOSC_O4b_16KHZ_R1-1420877824-4096.hdf5 \
  --cached DW_ftau_-7.0M.h5 \
  --lock reproduced_raw/pixi.lock \
  --toml reproduced_raw/pixi.toml \
  --qnm-filter-source qnm_filter_code \
  --pixi-bin "$(command -v pixi)" \
  --preflight reproduced_raw/GW250114_V72_RAW_PREFLIGHT.json
```

The preflight is fail-closed: it checks the frozen official-file hashes and HDF5 schemas, the actual Python/Pixi/package versions, and the imported `qnm_filter` path, commit, tree, and tracked-state cleanliness before grid evaluation. The packaged comparator then checks fresh versus recovered surfaces by exact axes/maxima and a declared centered-log-likelihood tolerance rather than timing or PNG hashes.

## Decision

No real `ln(4)`, `g=4`, area-quantization, black-hole microstate, or quantum-horizon inference is admitted. No Zenodo update is recommended from v72 alone.
