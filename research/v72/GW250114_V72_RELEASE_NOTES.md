# GW250114 HRF v72 — Release notes

## Added

- Exact closure/minimax theorem for a point target against an unrestricted punctured continuous alternative.
- Least-favorable Gaussian score and affine nuisance-image distance.
- Conservative finite-composite multiplicity budgets.
- Optimal two-observable allocation and shared-nuisance rank-completion theorem.
- Common-versus-detector-specific nuisance-alias theorem.
- Bounded-bias separation frontier.
- Full fixed-conditioning raw-strain replay of the released `-7M` `85x40` grid; the full Nature inference and marginalizations were not reproduced.
- Raw H1/L1 conditional quadratic-contribution surfaces and machine-precision arithmetic additivity audit under common released parameters and preprocessing.
- Released posterior-density-proxy versus maximum-log-likelihood-row sensitivity run.
- Deterministic math generator (`17/17`), raw preflight (`9/9`), raw finalizer (`16/16`), fresh-surface comparator (`26/26`), eight math CSV tables, four math figures, raw NPZ surfaces, replay/preflight/comparator scripts, and generated lock.

## Corrected

- In any fixed statistical experiment satisfying the stated total-variation closure condition, an exact `ln(4)` target cannot be uniformly separated from the unrestricted continuum `tau!=ln(4)`. Continuous alternatives must be resolution- or prior-defined.
- The released direct-wave row chosen by `argmax(log_likelihood+log_prior)` is a posterior-density sample proxy, not a maximum-likelihood solution.
- A least-favorable endpoint score is not automatically a composite Bayes factor.
- A two-sided exclusion radius has two endpoint competitors: its full-gap 90% joint width is `0.100155239%`, while `0.115190902%` applies to one named competitor.
- Detector-sharing information is local/tangent unless a finite global gauge or nuisance-image intersection is separately shown.
- The row-sensitivity run did not vary polarization in the executed filter options.

## Cleared since v71

- Python 3.11 raw-pipeline environment blocker.
- Official raw `-7M` network-grid execution blocker.
- Conditional H1/L1 quadratic-arithmetic implementation blocker for the released-point calculation; absolute detector normalizations and detector-only inference remain open.

## Still locked

- Detector-specific remnant/QNM inference.
- Real joint product–anchor covariance and nonlinear nuisance-image distances.
- HRF generative likelihood and nonregular no-extra-HRF calibration.
- A physically calibrated nonproduct second observable.
- Any `ln(4)`, `g=4`, area-quantization, or quantum-horizon interpretation.
