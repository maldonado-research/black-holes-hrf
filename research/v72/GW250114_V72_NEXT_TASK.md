# GW250114 HRF v72 — Next official-data task

## Highest-value continuation

Replace the conditional released-point detector surfaces with a joint raw analysis in which remnant/QNM, sky/time, calibration, PSD/ACF, and the proposed HRF product/anchor coordinates are inferred or stress-tested together. The deliverable must estimate real nonlinear nuisance images and their least-favorable separation, not only point-template distances.

## Required sequence

1. Freeze the v72 official-input hashes, generated lock, imported `qnm_filter` commit/tree, conditioning settings, and full scan rule before inspecting new branch statistics.
2. Reproduce every released `-3M` through `-9M` network grid and quantify cache residuals. Run the same H1/L1 pointwise additivity check for every lane.
3. Replace released-row maxima with continuous or sufficiently dense likelihood-only optimization. Separate maximum likelihood from maximum posterior density.
4. Perform detector-specific remnant/QNM inference or a validated bridge with adequate support. Do not reuse the v71-failed direct-importance clouds.
5. Vary sky/time, polarization, QNM content, filter shift, calibration, sampling, and multiple pre/post/segmented PSD/ACF windows. Record DQ and hardware-injection-frequency checks.
6. Specify the HRF generative likelihood, including the no-extra-HRF null. Calibrate the nonregular maximized delay/start/QNM/carrier scan on injections and off-source controls.
7. Produce paired samples or bounded nonlinear images for the product coordinate, direct-wave/echo anchor, trajectory, calibration, remnant, and waveform nuisances.
8. Compute the actual target and competitor image sets, their least-favorable Mahalanobis distance, and robustness to covariance estimation, bounded bias, and nonlinear boundaries.
9. Before evaluating the physical branch, preregister either a two-sided exclusion radius/indifference gap around `ln(4)` with both endpoint lanes controlled, an interval/equivalence procedure with declared coverage or type-I semantics, or a normalized continuous-alternative prior with scale sensitivity. Do not claim exact-point rejection of the unrestricted punctured continuum.
10. For a finite competitor bank, freeze its size and use the v72 intersection/multiplicity accounting. Keep the least-favorable score distinct from a composite Bayes factor.
11. Prototype the smallest physically defensible two-delay or echo observable satisfying a nonzero response determinant. Reject pure multiples, minimum-phase restatements of the product, or amplitude laws with free normalization.

## Admission conditions

A physical-branch lane may proceed only if all of the following hold:

- raw network replay and detector additivity remain stable across admitted settings;
- detector-specific remnant/QNM support is adequate;
- the HRF/null search is calibrated as a nonregular problem;
- target and competitor nuisance images have a positive declared-resolution margin;
- the worst admitted lane reaches its preregistered distance/probability requirement;
- adverse differential bias remains below the allowed budget;
- the result survives waveform, calibration, PSD/ACF, start-time, and detector stress tests.

## Kill conditions

Stop or publish a negative methods result if any required nuisance image intersects the target at the declared resolution; if a free normalization or trajectory restores an exact alias; if detector-specific inference cannot be supported; if the nonregular null cannot be calibrated; or if the strict distance/bias gate fails.

## Recommended public milestone

Do not make a new discovery or Zenodo claim from v72. The next worthwhile release should be either:

1. an observable-complete raw joint analysis with preregistered composite control; or
2. a fully documented negative result showing where the official workflow loses identification or power.
