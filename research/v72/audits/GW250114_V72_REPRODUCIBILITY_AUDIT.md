# GW250114 HRF v72 — Reproducibility audit

**Status:** `PASS` — `28/28` checks passed.

| Check | Status | Detail |
|---|---|---|
| `math_self_tests` | PASS | 17/17 |
| `raw_self_tests` | PASS | 16/16 |
| `math_submanifest` | PASS | ok |
| `math_generator_hash` | PASS | name=gw250114_v72_composite_closure_design.py, sha256=31eeaa721eee9caba464a6fe421a5b8c4cff7b3e5cecf6e99e1d53262ddb5b79 |
| `raw_submanifest` | PASS | ok |
| `continuous_closure_exact_values` | PASS | distance=0.0, error=0.5 |
| `one_competitor_strict_distance` | PASS | scope=one preregistered named competitor; D=3.7810604375308374 |
| `one_competitor_historical_gap_width` | PASS | 0.11519090213259128 |
| `two_sided_endpoint_distance` | PASS | K=2; D=4.348686765309588 |
| `two_sided_historical_gap_width` | PASS | 0.1001552391152782 |
| `raw_grid_shape` | PASS | [85, 40] |
| `raw_and_cache_same_maximum` | PASS | raw=(200.0,450.0), cache=(200.0,450.0) |
| `detector_additivity` | PASS | max_abs=1.137e-13 |
| `cache_residual` | PASS | centered_max_abs=7.734e-05 |
| `row_sensitivity_detected` | PASS | released=450.0, ML-row=420.0 |
| `summary_raw_residual_consistency` | PASS | 7.73435551522706e-05 |
| `summary_distance_consistency` | PASS | 3.7810604375308374 |
| `summary_two_sided_consistency` | PASS | D=4.348686765309588; q%=0.1001552391152782 |
| `fixed_conditioning_scope` | PASS | complete fixed-conditioning -7M 85x40 grid; not the full Nature inference |
| `full_nature_inference_not_reproduced` | PASS | full_nature_inference=NOT_REPRODUCED |
| `no_polarization_filter_attribution` | PASS | explicit no-pass qualification=True; filter-call psi/polarization keywords=none |
| `raw_preflight_receipt` | PASS | status=PASS |
| `fresh_replay_comparison_receipt` | PASS | status=PASS |
| `preflight_and_comparator_scripts_present` | PASS | ok |
| `all_json_parse` | PASS | 13 files; ok |
| `all_csv_parse_nonempty` | PASS | 13 files, 97 data rows; ok |
| `png_integrity_and_dimensions` | PASS | GW250114_V72_RAW_MINUS7M_DETECTOR_NETWORK_AUDIT.png:2160x1296; GW250114_V72_continuous_closure.png:1296x846; GW250114_V72_exclusion_precision_budget.png:1332x846; GW250114_V72_multiplicity_precision_budget.png:1296x846; GW250114_V72_two_observable_design.png:1296x846 |
| `physical_gate_locked` | PASS | status=LOCKED, admitted=false |

This audit checks package consistency only. It does not validate an HRF signal or physical interpretation.
