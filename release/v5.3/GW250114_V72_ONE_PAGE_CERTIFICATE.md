# GW250114 HRF v72 — One-page certificate

**Date:** 2026-07-12  
**Claim class:** exact statistical theory plus official-data reproducibility. **Not a detection or discovery claim.**

## Certified mathematical result

Let `lambda=ln(tau)`, let the target be `lambda_0`, and let `P_{lambda,eta}` denote the full observable law. Assume that along at least one feasible nuisance path with `lambda->lambda_0`, these laws converge in total variation to a target law. This holds, in particular, in the stipulated common-fixed-covariance Gaussian mean model when its mean is continuous. Then the full-law target-to-alternative distance is zero; in that Gaussian model the corresponding mean-image statement is

\[
\operatorname{dist}\!\left(\mathcal M_{\lambda_0},
\bigcup_{\lambda\ne\lambda_0}\mathcal M_\lambda\right)=0.
\]

Therefore an exact point target such as `tau=ln(4)` cannot have positive **uniform** separation from an unrestricted continuous alternative that excludes only the point itself. Under the stated full-law continuity assumption, the minimax maximum of type-I and worst-alternative type-II error is `1/2` when randomized tests are allowed. This does not prevent pointwise consistency against any fixed separated alternative.

A valid repair must declare at least one of:

- an exclusion/indifference radius `|lambda-lambda_0|>=delta_0`;
- an interval or equivalence procedure with declared coverage or type-I semantics; a uniform classification gate additionally needs an indifference gap;
- a point-mass-versus-continuous Bayesian model with a normalized prior and prior-scale sensitivity.

For two closed convex Gaussian mean-image sets with closest Mahalanobis distance `d`, the least-favorable endpoint score has variance `d^2`, worst-case target mean at least `d^2/2`, and worst-case competitor mean at most `-d^2/2`. Requiring the score to exceed `ln(10)` with probability at least `0.90` needs

\[
d\ge 3.7810604375.
\]

Within the stipulated scalar log-Gaussian design model, at the old v65–v71 log-branch gap `0.00435543762817`, the corresponding best-case width is `q_eff<=0.115190902%` for one preregistered named competitor. The symmetric exclusion alternative `|lambda-lambda_0|>=delta_0` has two endpoint competitors and therefore requires `q_eff<=0.100155239%` at the full historical gap for a 90% joint-success lower bound. Conservative finite-composite control gives `0.093530%` for three, `0.086691%` for five, and `0.079315%` for ten competitors. These are design screens, not event measurements.

## Certified fixed-conditioning official-data replay

Using official discovery-v1 16-kHz H1/L1 strain, the released NRSur7dq4 posterior file, and the released direct-wave implementation:

- all `85x40=3400` `-7M` frequency–damping points were evaluated from raw strain;
- the raw and cached network surfaces peak at `200 Hz, 450 s^-1`;
- after removing a single additive constant, the maximum cache–raw residual is below `7.8e-5` log-likelihood units in both the original and fresh locked replays;
- under one common released parameter row and preprocessing convention, pointwise conditional quadratic arithmetic `ell_H1+L1=ell_H1+ell_L1` holds to `1.13687e-13`. Parameter-independent detector normalizations were not reconstructed.
- the fail-closed preflight, raw finalizer, and fresh-versus-recovered numerical comparator pass `9/9`, `16/16`, and `26/26`, respectively; the largest centered surface difference is `3.07161e-7`, below the declared `1e-5` replay threshold.

This clears the v71 environment, fixed-conditioning `-7M` grid-reproduction, and conditional quadratic-arithmetic implementation blockers. It does not reproduce the full Nature inference or its marginalizations.

It does **not** clear the physical gate. The released posterior-density proxy gives detector maxima `(H1: 200 Hz, 390 s^-1; L1: 198 Hz, 510 s^-1)`. Selecting the maximum-`log_likelihood` released posterior row instead moves the network maximum from `450` to `420 s^-1`, with a centered RMS surface change of about `4.0372` log-likelihood units. This changes mass, spin, sky position, and geocentric time jointly; it is not a continuous optimizer or a one-nuisance attribution. Detector-specific remnant/QNM inference and nuisance marginalization have not been performed.

## Decision

```text
RAW_REPRODUCTION_PASS
UNRESTRICTED_CONTINUOUS_TAU_UNIFORM_IDENTIFICATION_EXACT_FAIL
FINITE_COMPOSITE_METHODS_PASS_ONLY
REAL_JOINT_NUISANCE_DISTANCE_NOT_MEASURED
PHYSICAL_INTERPRETATION_LOCKED
```

No `ln(4)`, `g=4`, area-quantization, or quantum-horizon claim is admitted.
