# GW250114 HRF v72 — Composite-alternative closure, least-favorable separation, optimal design, and raw `-7M` replay

**Date:** 2026-07-12  
**Claim class:** mathematical/statistical methods and official-data reproducibility. **Not a black-hole, area-quantization, or quantum-horizon discovery claim.**

## Executive decision

v72 resolves the two highest-priority questions left by v71.

First, it executes the complete fixed-conditioning `-7M`, `85x40` frequency–damping grid on official discovery-v1 H1/L1 strain. The raw network grid reproduces the released cached grid up to a numerically tiny nonconstant residual, and the raw detector quadratic contributions add to the network objective at machine precision. This closes the v71 environment and fixed-grid execution blockers, but it does not reproduce the Nature paper's full marginalization, template/SNR inference, or other start-time lanes.

Second, it corrects the interpretation of an “exact `ln(4)` versus continuous `tau`” comparison. When the full observable laws are total-variation continuous along an admitted punctured-alternative nuisance path, the alternative closure contains a target observable distribution. No fixed statistical experiment satisfying that closure condition can obtain a positive uniform margin against the continuum. For randomized tests, the minimax maximum of type-I and worst-alternative type-II error is exactly one half. The correct next claim must be resolution-aware.

Neither result establishes an HRF signal or a physical lattice branch. The raw replay is conditional on released point estimates and the direct-wave model, while the theorem says that even an ideal completed observable must declare what separation from `ln(4)` is scientifically distinguishable.

## 1. Exact continuous-alternative closure theorem

Write `lambda=ln(tau)` and let `P_{lambda,eta}` be the full observable law. Assume total-variation continuity along at least one feasible nuisance sequence `(lambda_n,eta_n)->(lambda_0,eta_0)` with `lambda_n!=lambda_0`. This holds in the stipulated common-fixed-covariance Gaussian model when the mean is continuous. For that Gaussian model, let

\[
\mathcal M_\lambda
=
\{\mathbf g(\lambda,\boldsymbol\eta):\boldsymbol\eta\in\mathcal H\}
\]

be the admitted mean nuisance image. The approaching sequence of full probability laws gives zero distributional separation. In the common-covariance Gaussian model it is accompanied by

\[
\boxed{
\operatorname{dist}\!\left(\mathcal M_{\lambda_0},
\bigcup_{\lambda\ne\lambda_0}\mathcal M_\lambda\right)=0 .
}
\]

For any test, total-variation convergence makes the alternative rejection probability approach the target rejection probability. Its worst target/alternative error is therefore at least `1/2`; a fair randomized rule attains `1/2`. Zero mean-image distance alone would not suffice if covariance, support, or another part of the law changed discontinuously.

This is a uniform statement. It does not deny that data can consistently distinguish `lambda_0` from each fixed `lambda_1!=lambda_0` as information grows.

The new exact gate is:

```text
UNRESTRICTED_CONTINUOUS_TAU_UNIFORM_GATE_EXACT_FAIL
CONTINUOUS_TAU_RESOLUTION_GATE_REQUIRES_EXCLUSION_RADIUS_OR_NORMALIZED_PRIOR
```

Three admissible formulations remain:

1. preregister `|lambda-lambda_0|>=delta_0` as the alternative;
2. state an interval/equivalence result with declared coverage or type-I semantics; a uniform classification margin additionally requires an indifference gap between the target and alternative regions;
3. compare a point-mass target model to a normalized continuous model and disclose sensitivity to the alternative prior scale.

## 2. Least-favorable separation for composite nuisance images

Let `X~N(mu,K)` with fixed positive-definite `K`. Let `A` be the target mean-image set and `C` the competitor image set. If both are closed and convex and a closest pair `(a_*,c_*)` exists, define

\[
d^2=(a_*-c_*)^T K^{-1}(a_*-c_*),
\]

\[
L=(a_*-c_*)^T K^{-1}
\left[X-\frac{a_*+c_*}{2}\right].
\]

Convex projection inequalities give

\[
\operatorname{Var}(L)=d^2,
\qquad
\inf_{a\in A}E_aL\ge\frac{d^2}{2},
\qquad
\sup_{c\in C}E_cL\le-\frac{d^2}{2}.
\]

For `d>0`, consequently,

\[
\inf_{a\in A}P_a(L>c)
\ge
\Phi\!\left(\frac d2-\frac c d\right),
\]

and the midpoint rule has worst-case error no greater than `Phi(-d/2)`. If `d=0`, the images intersect or have zero margin and the standardized bounds that divide by `d` are not used. The score is the likelihood ratio for the least-favorable endpoint pair. It is **not** automatically a composite Bayes factor.

For `c=ln(10)` and target probability `0.90`, the positive solution is

\[
\boxed{d\ge3.781060437530837.}
\]

In an affine nuisance model with `A=mu_p+Col(B_p)`, `C=mu_g+Col(B_g)`, `delta=mu_p-mu_g`, and `C_B=[B_p,-B_g]`,

\[
d^2=\delta^T\!\left[
K^{-1}-K^{-1}C_B(C_B^TK^{-1}C_B)^+C_B^TK^{-1}
\right]\delta.
\]

This is the global affine analogue of the v71 nuisance-quotient Fisher information. Allowing unrestricted affine extrapolation is conservative; a zero affine distance can arise outside the physically admitted nuisance domain and must be checked against the actual bounded nonlinear image.

## 3. Resolution and multiplicity budgets

The historical point branches have

\[
\tau_p=\ln4=1.3862943611198906,
\qquad
\tau_g=1.3802695723157803,
\]

\[
\Delta_\lambda=0.004355437628170275.
\]

In the linear-affine scalar-width approximation, an exclusion radius `delta_0` gives `d=delta_0/q_eff` for each endpoint. Because `|lambda-lambda_0|>=delta_0` is two-sided, the target is claimed only when both endpoint scores exceed `ln(10)`. Allocating the 10% miss budget equally by Bonferroni control requires `d>=4.3486867653` for each side. The resulting joint-90% screens are:

| Exclusion radius | Maximum `q_eff` |
|---|---:|
| quarter old gap | 0.0250388% |
| half old gap | 0.0500776% |
| full old gap | 0.1001552% |
| 1% log radius | 0.2299545% |

The earlier `0.115190902%` width remains the correct 90% threshold for one preregistered named competitor. Applying it simultaneously to the two exclusion endpoints guarantees only an 80% target-success lower bound.

For `K` preregistered finite competitors, a conservative intersection rule allocates the miss probability by Bonferroni. At the old full gap:

| Competitors | Required pairwise `d` | Maximum `q_eff` |
|---:|---:|---:|
| 1 | 3.78106 | 0.115191% |
| 2 | 4.34869 | 0.100155% |
| 3 | 4.65675 | 0.093530% |
| 5 | 5.02411 | 0.086691% |
| 10 | 5.49132 | 0.079315% |

These are declared Gaussian design screens, not measurements of GW250114.

For the most extreme low-power benchmark, ordinary double-precision linear-space evaluation underflows to `0.0`; the generator therefore also records a stable log tail. The carrier-lane value is `log10 P(L>ln(10))=-666.0361`, while the NRSur benchmark probability is `4.61467661e-10`. Neither changes a gate.

## 4. Optimal two-observable completion design

For two local observables

\[
Y_i=q_i\lambda+b_i\eta+\epsilon_i,
\qquad
\operatorname{Var}(\epsilon_i)=\frac{\sigma_i^2}{n_i},
\qquad n_1+n_2=N,
\]

with one shared nuisance `eta`, independent errors, `n_i>0`, `sigma_i>0`, and at least one nonzero nuisance loading `b_i`, the efficient information is

\[
I_{\rm eff}
=
\frac{a_1a_2(q_1b_2-q_2b_1)^2}
{a_1b_1^2+a_2b_2^2},
\qquad a_i=\frac{n_i}{\sigma_i^2}.
\]

Within this stipulated two-channel/one-shared-nuisance model, the exact local rank-completion rule is

\[
\boxed{q_1b_2-q_2b_1\ne0.}
\]

Replication of a channel with the same nuisance slope does not complete the rank. When both nuisance loadings are nonzero, the fixed-total-resource optimum is

\[
\frac{n_1}{N}
=
\frac{|b_2|/\sigma_2}{|b_1|/\sigma_1+|b_2|/\sigma_2},
\qquad
I_{\rm eff,max}
=
N\frac{(q_1b_2-q_2b_1)^2}
{(|b_1|\sigma_2+|b_2|\sigma_1)^2}.
\]

If `b_1=b_2=0`, nuisance profiling is unnecessary and the displayed quotient form is replaced by the ordinary information `sum_i a_i q_i^2`.

For the v69 gauge, a physically relevant two-delay prototype is

\[
g_i=t\,F_i(\tau).
\]

In log coordinates the common free-timescale nuisance has `b_i=1`, while `q_i=d ln F_i/d ln tau`. The local determinant is therefore proportional to `q_1-q_2`, equivalently to a nonzero derivative of `F_2/F_1` with respect to `tau`. A second pure multiple of the first delay has equal slopes and remains rank-deficient. If another variable such as `beta` is also free, it contributes another nuisance column; two scalars generally no longer suffice. Every calibration, phase, amplitude, remnant, and trajectory nuisance must be included before declaring completion.

## 5. Detector nuisance-sharing theorem

With a nuisance coefficient shared across detectors,

\[
I_{\rm common}=\min_a\sum_d\|q_d-B_da\|^2_{K_d^{-1}}.
\]

Allowing detector-specific coefficients gives

\[
I_{\rm ds}=\sum_d\min_{a_d}\|q_d-B_da_d\|^2_{K_d^{-1}},
\qquad I_{\rm common}\ge I_{\rm ds}.
\]

Individually locally aliased detectors gain positive shared-nuisance tangent information only when the alias coefficients required by the detectors are inconsistent. If the same coefficient fits every detector, network stacking preserves the local linear alias. Exact global nonidentifiability requires a separate finite transformation or nuisance-image intersection, as supplied by the v69 single-delay gauge. This theorem must be applied after a valid raw likelihood factorization; it cannot rehabilitate importance-deconditioned released network samples that failed v71 support gates.

## 6. Fixed-conditioning official raw `-7M` grid replay

v72 acquired and locally froze by SHA-256:

- GWOSC discovery-v1 16-kHz H1 and L1 strain;
- the official NRSur7dq4 posterior HDF5;
- the Nature companion archive and embedded `qnm_filter` source;
- the embedded `qnm_filter` source required by the replay.

The publisher MD5 values were also checked for the two Zenodo downloads: `4874fef35088209c9fa4073f15a27a78` for the Nature ZIP and `9b115931b66439a1d5649a2b7b7aa143` for the NRSur7dq4 posterior. The imported editable source is tied to commit `55f14436d4ea510b71754b95da9701009e8a1c12` and Git tree `377f807dd345a138c32d274f3cb746f60dd0cecf` by the packaged preflight receipt.

A Python 3.11 environment was resolved from the released `pixi.toml`, and a generated `pixi.lock` is packaged. The release did not itself contain this lock; v72 does not mislabel it as author supplied. Runtime versions are queried by the replay preflight rather than hard-coded.

The replay evaluated `160–238 Hz` in `2 Hz` steps and damping rates `50–890 s^-1` in `10 s^-1` steps at `-7M`, for `3400` points per surface.

Using the row selected by the released implementation, `argmax(log_likelihood+log_prior)` among released posterior samples:

| Surface | Frequency | Damping rate | Decay time |
|---|---:|---:|---:|
| H1+L1 raw | 200 Hz | 450 s^-1 | 2.2222 ms |
| H1 raw contribution | 200 Hz | 390 s^-1 | 2.5641 ms |
| L1 raw contribution | 198 Hz | 510 s^-1 | 1.9608 ms |

The released cached network grid also peaks at `200 Hz, 450 s^-1`. For `cached-raw`:

- mean: `-2.36553e-4` log-likelihood units;
- centered RMS: `3.50989e-5`;
- centered maximum absolute residual: `7.73436e-5`;
- point-to-point range: `1.50175e-4`.

Using the same common released row and conditioning objects, raw pointwise H1/L1 quadratic-contribution arithmetic has maximum error

\[
\max|\ell_{H1+L1}-\ell_{H1}-\ell_{L1}|
=1.13687\times10^{-13}.
\]

This passes the fixed-conditioning grid-replay and conditional quadratic-arithmetic implementation gates. Additivity is an implementation identity of the released independent-detector objective, not independent physical validation. It does not establish absolute detector likelihood normalization or detector-only statistical inference.

## 7. Point-selection sensitivity prevents physical promotion

The companion calculation selects `argmax(log_likelihood+log_prior)` among released samples; this is a released-draw posterior-density proxy, not a maximum-likelihood solution. Selecting the maximum-`log_likelihood` released row instead changes the network maximum to `200 Hz, 420 s^-1`; its detector maxima are `202 Hz, 360 s^-1` for H1 and `202 Hz, 480 s^-1` for L1.

After subtracting a mean offset, the two network surfaces differ by:

- centered RMS `4.03722354` log-likelihood units;
- centered maximum absolute difference `14.3581211`;
- point-to-point range `19.7060848`.

These are two posterior rows, not continuous optimizer solutions. The active inputs changed together—remnant mass, spin, right ascension, declination, and geocentric time—so the shift establishes joint fixed-point sensitivity but cannot identify which nuisance caused it. Polarization was recorded in the receipt but was not passed to `qnm_filter` and is not credited for the change. Detector-specific remnant/QNM inference, calibration marginalization, alternative PSD/ACF windows, filter/start-time scans, and a complete HRF generative model remain required.

The detector-separated surfaces are therefore admitted only as conditional quadratic contributions at a common released point. They are not detector-only HRF cross-validation results.

The final fail-closed replay records `9/9` preflight checks, `16/16` raw finalizer checks, and `26/26` tolerance-comparator checks. Across every H1, L1, and network surface, the fresh replay preserves the grid axes and maximum indices; its largest centered difference from the recovered core is `3.07161e-7` log-likelihood units, below the declared `1e-5` numerical threshold. This is a replay-consistency statement, not an independent astrophysical validation.

## 8. Observable-completion priorities

The strongest next physical completion candidates remain:

1. raw joint inference of the product coordinate and a detector-aware direct-wave timescale, including remnant/QNM and calibration nuisance;
2. a concrete pair `g_i=t F_i(tau)` whose log-`tau` slopes differ after retaining the common free timescale;
3. echo timing with an independently constrained Kerr scaling factor;
4. echo-train amplitude ratios only after calibrating the barrier response.

Minimum-phase reconstruction that remains a function of `tau*t`, pure multiples of the same delay, a free branch-amplitude normalization, and product-only catalogs do not complete the rank. Absorption, tidal heating, greybody factors, and Love-number ideas remain undeveloped until they supply a calibrated nonproduct `tau` dependence.

## 9. Current honest decision

- The exact v69 single-delay nonidentifiability theorem remains in force.
- The v71 nuisance-quotient and covariance gates remain unpassed by real joint samples.
- v72 passes the official fixed-conditioning `-7M` raw-grid replay and conditional H1/L1 quadratic-arithmetic gates.
- v72 detects material released-row conditioning sensitivity and does not promote conditional detector surfaces to an HRF cross-fit.
- An exact point target versus an unrestricted continuous alternative is uniformly unresolvable without a declared resolution or normalized prior.
- The least-favorable and optimal-design results are methods, not event measurements.
- No extra-HRF nonregular-null calibration has been performed.
- No real `ln(4)`, `g=4`, area-quantization, microstate, or quantum-horizon interpretation is admitted.
- Another Zenodo release is not recommended yet. A public milestone should contain an observable-complete raw joint analysis or a documented negative result from that workflow.
