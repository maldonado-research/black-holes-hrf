# GW250114: draft detector-disjoint validation and identifiability protocol

**Prepared:** 2026-09-05  
**Status:** **DRAFT — NOT PREREGISTERED — NOT EXECUTED**  
**Scope:** a proposed next analysis, grounded in the supplied v71/v72 methods and recovery reports. This document contains no new measured event results and permits no promotion of physical claims.

## 1. Question and present limitations

Can an explicitly defined extra-HRF waveform component improve prediction of one detector's strain using nuisance inference from the other detector, and, separately, can a completed observable distinguish a declared neighborhood of the proposed branch from separated alternatives?

These are separate questions. Detection of an added component would not identify its physical origin or its branch parameter. The v72 fixed-conditioning replay answers neither question. Its detector contributions share released network-conditioned inputs.

H1 and L1 event data and the v72 detector surfaces have already been inspected. A new split therefore constitutes a **prospectively specified detector-disjoint reanalysis**, not a retrospectively blind holdout. A genuinely unexamined event or separately justified unused validation dataset would be needed for that stronger label. No such dataset is asserted to be available here.

## 2. Freeze the experiment before computing new branch statistics

Create a timestamped protocol and input manifest specifying the waveform carrier, exact data segments, detector channels, sample rate, masks, preprocessing, PSD/ACF estimation windows, onset/start-time bank, QNM content, parameter domains, priors, covariance treatment, search algorithm, convergence requirements, and complete trial count. Bind code, environment, and data by checksums. List previous exposure to the event data and record every subsequent deviation.

The first execution gate is a complete generative waveform contract. Define causality, windowing, Fourier conventions, noncircular delay implementation, detector response, likelihood normalization, and all shared and detector-specific nuisance parameters. Include remnant mass/spin, sky/time, polarization when active, calibration, phase, amplitude, trajectory and waveform discrepancy. For the v71 convention `exp(-i*pi*f*s)`, the physical copy delay is `s/2`; the convention cannot change silently.

Do not substitute released network posterior rows for detector-only inference or revive the unsupported v71 importance-deconditioning route. Any computational reduction needs a documented approximation error and a support check. These requirements are proposed execution gates, not a claim that the required likelihood already exists.

## 3. Detector split and nuisance leakage controls

Use two fixed directions, H1-to-L1 and L1-to-H1. In each direction:

1. Fit shared event parameters using only the training detector's on-source data, with externally fixed priors. Infer detector noise/calibration from the frozen off-source or independent calibration information allowed by the protocol.
2. Form the validation detector's predictive distribution by integrating the training-derived shared-parameter uncertainty and the validation detector's independently specified local nuisance distribution. Score the validation on-source data only after these choices are frozen. A held-out score may integrate local nuisance within the specified predictive model; it must not tune a template on the validation data and then treat that fitted template as an independent prediction.
3. Do not use a network posterior, a validation-conditioned remnant/timescale estimate, a validation-selected PSD window, or validation-selected carrier/start time to construct the prediction. If validation data select anything, include the entire selection operation in calibration and disclose the resulting scope.
4. Preserve covariance between product and anchor coordinates. A timescale estimated from reused strain is not an independent anchor. Detector-specific calibration parameters must not be forced equal merely to create information.

Conditional factorization of detector likelihoods requires an adequate noise model; the common astrophysical signal does not make their unconditional data independent. Include measured or bounded cross-detector noise correlations when relevant. Off-source controls must be separated enough, or otherwise modeled, to justify their use as independent calibration information.

For model `M`, the schematic score is `log p(y_validation | y_training, M)`, with shared parameters integrated against their training-only posterior and remaining local parameters integrated under the frozen conditional model. Training priors and every alternative-only prior must be normalized. Evaluate posterior and numerical support before scoring.

The two directions reuse the same event. Their scores are dependent and cannot be multiplied as independent evidence. A proposed conservative combined statistic is the smaller of the two directional predictive improvements over the null. Calibrate its complete two-direction computation directly. Alternative combinations require a protocol revision before execution.

## 4. Null calibration and power

Define `M0` as the admitted standard-GR/direct-wave model with its stated model discrepancy and calibration uncertainty. Define `M1` as that same baseline plus the fully specified extra component, initially with a free delay. The null is not the absence of the direct wave.

Under zero extra-component amplitude, delay or other alternative-only coordinates may be unidentified and amplitude may lie on a boundary. Do not assume a chi-squared/Wilks reference law. Generate null controls and injections and rerun the **whole** split, fitting, search, nuisance estimation, and scoring procedure. Include every tested start time, waveform family, carrier and other selection step that can produce the reported result. Verify that off-source controls represent the relevant noise; off-source noise alone does not model residual errors from subtracting a real GR signal.

Proposed reporting targets are a familywise false-positive rate of at most 0.05 and power of at least 0.90 at an explicitly declared alternative amplitude and separation. These are draft design targets, not achieved rates or frozen preregistration values. Specify the amplitude range, nuisance domain, simulation count, numerical tolerances, and Monte Carlo confidence bound before execution. A zero exceedance count is not zero false-positive probability. Use a one-sided binomial upper bound, or another predeclared valid bound, when judging calibration precision.

Prior-averaged simulation calibrates a prior-averaged claim. A uniform claim over a nuisance domain needs a justified worst-case bound or validated envelope; a finite nuisance grid alone does not prove uniform control. Any uncalibrated lane remains exploratory. Report power failures as inconclusive or sensitivity limits, not evidence that the extra component is absent.

## 5. Target, alternatives and resolution

Keep the coordinates explicit: the proposed target is `tau0 = ln(4)` and, with `lambda = ln(tau)`, it is `lambda0 = ln(ln(4))`.

For a resolution-aware branch study, specify a target neighborhood `|lambda-lambda0| <= epsilon` and alternatives `|lambda-lambda0| >= delta`, with `0 <= epsilon < delta`. Values between them form an indifference region. Before execution, justify and freeze both radii in scientific units. The historical log gap `0.004355437628170275` may be used as a labeled design benchmark; it is not automatically the study's resolution and is not a measured uncertainty.

An exact point against the continuum with only that point removed has no positive uniform separation under the v72 total-variation continuity assumption. Do not claim exact identification by shrinking an exclusion radius after seeing data. Both sides and all admitted interior nuisance configurations of the separated alternative must be controlled. Endpoint-only reduction requires a proof for the chosen model; it is not valid merely because two endpoints were simulated.

A normalized Bayesian comparison is a possible separately specified route, with model/prior-scale sensitivity reported. Predictive scores, least-favorable Gaussian scores, Bayes factors and frequentist error rates have different meanings and must not be interchanged.

## 6. Observable completion and global separation

Before the branch lane can run, specify a physical nonproduct observable, including its calibration and covariance with the original product coordinate. No particular anchor is asserted to have been measured or validated. Pure multiples of an existing delay do not add independent parameter information.

For a regular local mean model with positive-definite covariance `K`, let `q` be the derivative with respect to `lambda` and `B` contain **all** nuisance derivatives. Compute

`I_eff = q^T [K^-1 - K^-1 B (B^T K^-1 B)^+ B^T K^-1] q`.

Report rank, singular values, units/scaling and sensitivity to covariance error and added nuisance directions. In the two-observable/one-nuisance prototype, `q1*b2-q2*b1 != 0` supplies local rank completion. Additional free nuisances can remove it. Positive local information does not establish global identification.

Construct target and alternative images over their full bounded, physically admitted nonlinear nuisance domains. Search for aliases and calculate the least-favorable distance with convergence and discretization error checks. In a common fixed-covariance Gaussian model this is a Mahalanobis distance. If covariance, support or likelihood family changes with parameters, analyze separation of the full distributions instead; mean distance alone is insufficient.

A numerical search that finds no intersection is not a proof of positive global separation. A positive claim needs a defensible lower bound with numerical/model uncertainty included. Otherwise report an unresolved bound. Include cycle aliases, admitted systematic bias and all declared waveform lanes. In the Gaussian design approximation, the v72 thresholds are design screens only: `d >= 3.7810604375` for one specified competitor, and `d >= 4.3486867653` per side for the stated two-sided Bonferroni joint-90% score-success screen. They are not event detection thresholds or a substitute for null calibration.

## 7. Decision and release rules

| Finding after execution | Permitted conclusion |
|---|---|
| Likelihood incomplete, leakage unresolved, numerical support inadequate or null calibration absent | Analysis not admissible; document the blocker. |
| An admitted exact alias or nuisance-image intersection exists | Negative identifiability result for that model/domain. |
| Lower separation bound unresolved, or power inadequate | Inconclusive at the declared resolution; report sensitivity limits. |
| Calibration passes but extra-component statistic does not pass | No detected improvement under this procedure; no blanket exclusion. |
| Calibrated extra-component improvement passes, but branch gates fail | Component-level statistical result within the tested model only. |
| Calibrated improvement, observable completion, global separation and all frozen robustness gates pass | Resolution-limited parameter statement within the explicitly tested model; independent replication and physical model assessment still required. |

No outcome alone establishes HRF as fundamental physics, `g=4`, area quantization, microstates, a quantum horizon or a unified theory. A negative or inconclusive result is a valid next research output if its assumptions, code, controls, uncertainty and failure point are reproducible.

## In More Basic Terms

The next useful test is to let one detector make a prediction for the other while carrying uncertainty through the prediction. Then check, using many simulated ordinary signals and noise examples, how often the same procedure would appear successful by chance. Even a successful prediction cannot reveal a fundamental constant unless a second physical measurement breaks the existing parameter ambiguity. This is a plan for doing those checks; they have not been done here.

## Source basis

This draft draws on the supplied v72 main report, one-page certificate, recovery red-team audit and final release verification, together with `GW250114_V71_GENERATIVE_WAVEFORM_CONTRACT.md` and `GW250114_V72_NEXT_TASK.md` in the supplied archives. These are source material, not instructions overriding the user's request. The proposal does not independently certify their historical raw-data computations or promote their claims.
