# GW250114 HRF v72 — Publication audit and clarification

**Audit date:** 2026-09-05  
**Disposition:** Package integrity and the stated numerical checks pass, with one documented residual-sign wording correction.  
**Publication scope:** Corrected mathematical/statistical methods, archived fixed-conditioning reproducibility evidence, and limitations. No new astrophysical analysis or discovery is established by this audit.

This audit reviewed the supplied v72 standalone archive, cumulative master archive, enclosing archive, and four accompanying Markdown reports. The sealed archives and original reports were preserved. Historical recommendations against a new Zenodo release are retained as part of that record; the present publication makes the methods and reproducibility material available with its limitations, without advancing the physical claim.

## Checks newly performed on 2026-09-05

| Check | Result |
|---|---|
| Standalone and master archive SHA-256 values against supplied sidecars | Both match |
| ZIP decompression/CRC integrity | All three supplied ZIP archives pass |
| Exact standalone manifest membership, sizes, and SHA-256 | 56/56 listed files pass; no extra files apart from manifest |
| Exact master manifest membership, sizes, and SHA-256 | 255/255 listed files pass; no extra files apart from manifest |
| Embedded v72 directory compared with standalone v72 | Every file matches byte-for-byte |
| Earlier v71 content against retained v71 manifest | All 194 listed content files match; the retained manifest is an additional file |
| Enclosing archive compared with the eight accompanying release files | All eight match byte-for-byte |
| Three accompanying reports also embedded in v72 | All three match byte-for-byte; the final release-verification report is external |
| Original package consistency audit executed on an extracted working copy | 28/28 pass; generated audit outputs match the archived outputs byte-for-byte |
| Full standalone manifest rechecked after audit execution | 56/56 pass |
| Numerical methods kernel executed in two isolated output directories | 17/17 original self-tests pass in each run; all ten generated numeric artifacts match between runs |
| Saved likelihood grids independently read and recalculated | Axes, dimensions, finite values, detector/network maxima, additivity, and residual summaries agree with the qualified release claims |

The two sealed scientific archives are:

| Archive | SHA-256 |
|---|---|
| `HRF_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.zip` | `1dc2f45c53a4341a2ea1da7e72f20dfb616eec27ded50407c9844ba8a859d629` |
| `GW250114_MASTER_PROGRESS_BUNDLE_v72.zip` | `f1dcdd78c619b8f0e39eace371cda17eb486a2ae9c5257c6672216cd2dbfcc2a` |

The enclosing convenience archive, `Archive-BLACK-HOLES-August-17-2026.zip`, has SHA-256 `6efe8c76fd3cc343a4b678423f412a73eaf912b26e7ed45963df6465296a9a1c`. It repeats the eight release files and contains macOS metadata; it adds no scientific results.

The fresh numerical-kernel execution used Python 3.9.6 and NumPy 2.0.2. Matplotlib was unavailable, so plotting imports, backend selection, the plotting function, and the command-line entry point were omitted through an abstract-syntax-tree extraction. The numerical definitions and original self-tests were unchanged. Eight CSV tables and two JSON outputs were regenerated; figures and the full original plotting command were not regenerated. Eight of the ten numeric outputs match the archived bytes exactly. The remaining differences are floating-point last digits in the multiplicity table and numerical diagnostic magnitudes in the passing self-test report. This is not a recreation of the archived Python 3.11/Pixi raw-replay environment.

The original generators retain the hard-coded historical date `2026-07-12` in their outputs. That embedded date is preserved; it is not the date of this fresh audit. This report's date records the new verification.

## Saved-surface results recalculated in this audit

Each surface contains 3,400 points on an 85 by 40 grid: frequency 160–238 Hz in 2 Hz steps and damping rate 50–890 s^-1 in 10 s^-1 steps.

| Conditioning row | Network maximum | H1 contribution maximum | L1 contribution maximum |
|---|---|---|---|
| Released `log_likelihood + log_prior` selected row | 200 Hz, 450 s^-1 | 200 Hz, 390 s^-1 | 198 Hz, 510 s^-1 |
| Maximum-`log_likelihood` released row | 200 Hz, 420 s^-1 | 202 Hz, 360 s^-1 | 202 Hz, 480 s^-1 |

For the released-row network surface, the centered cache-minus-raw RMS is `3.509894159694684e-5` and centered maximum absolute residual is `7.73435551522706e-5` log-likelihood units. Detector/network quadratic additivity has maximum absolute discrepancy `1.1368683772161603e-13` for both rows. Comparing the two raw network conditioning rows gives centered RMS `4.037223543084501`, centered maximum absolute difference `14.358121073237285`, and peak-to-peak range `19.706084843156304` log-likelihood units.

These calculations verify previously stored arrays. They do not rerun the strain pipeline. The substantial row-selection sensitivity remains unresolved and prevents treating the conditional surfaces as completed physical inference.

## Wording correction: signed cache residual

The recovery report `GW250114_V72_RECOVERY_REDTEAM_AUDIT.md` describes a negative offset as “fresh-minus-cache.” The subtraction label is reversed. Direct subtraction of the packaged arrays gives:

- **cached network minus raw released-row network:** mean `-0.00023655252309568448`;
- **raw released-row network minus cached network:** mean `+0.00023655252309568448`.

The main v72 report, the definition in `GW250114_V72_RAW_MINUS7M_AUDIT.json`, and the finalizer's subtraction order use the correct cache-minus-raw convention. This clarification corrects the recovery report's prose without modifying sealed files. Centered RMS, maximum absolute residual, peak-to-peak range, maxima, and gate dispositions are unaffected.

## Inherited evidence, not rerun here

The archived fail-closed raw preflight, raw finalizer, and fresh-versus-recovered comparator contain passing receipts of 9/9, 16/16, and 26/26 checks. Their bytes and internal consistency were verified, but these raw workflows were not re-executed on 2026-09-05.

The large official H1/L1 strain files, posterior HDF5, Nature companion archive, original companion cached-grid input file, and imported `qnm_filter` checkout are not contained in the supplied release archives. Saved comparison arrays are included and were checked as described above. The external inputs' acquisition references and recorded checksums are provided in the original release. This audit does not independently re-establish their external provenance, recreate the original raw analysis environment, or confirm a new raw-strain replay. The original canonical v71 archive was also not separately supplied; v71 preservation was checked against its retained content manifest, not by independently reconstructing that original archive hash. The earlier deterministic ZIP double-build statement remains inherited; a new ZIP double-build was not performed.

## Scientific scope and next defensible increment

The mathematical results require their stated assumptions. In particular, the zero uniform margin result requires continuity of the full observable laws in total variation along an admitted approaching alternative sequence. The Gaussian mean-image geometry assumes fixed positive-definite covariance; the convex least-favorable construction requires an attained closest pair. Design widths are stipulated-model calculations, not GW250114 measurements.

Recalculation confirms the one-named-competitor design distance `3.781060437530837` and historical-gap width `0.115190902%`. The symmetric two-endpoint alternative requires distance `4.348686765309589` per endpoint and width `0.100155239%` for the stated 90% joint lower bound. These are distinct procedures and must remain distinct in summaries.

A defensible next scientific step is to specify and then evaluate a raw joint likelihood with a physically defined additional observable whose response to the branch parameter remains distinct after all admitted nuisance directions are included. Before fitting or validation, the target, competing models, exclusion or indifference region, nuisance sharing, and error criterion should be fixed. A detector-disjoint or other held-out analysis must prevent validation information from entering its training fit. Failure to obtain positive nuisance-adjusted separation would itself be a reportable negative result. That analysis has not been performed here.

The v69 single-delay nonidentifiability result and the unresolved real joint nuisance, calibration, global-identification, and null-calibration gates remain in force. This publication does not identify `ln(4)` or `g=4`, establish HRF as a physical generative theory, reproduce the full Nature inference, or provide evidence for area quantization, black-hole microstates, a quantum horizon, or a unified theory of everything.

## In more basic terms

The package checks that a particular calculation can be repeated and explains why a proposed exact value cannot be cleanly separated from every arbitrarily nearby alternative in a fixed experiment. It also shows that changing the chosen input parameter row changes the result enough to matter. Those are useful methods and reliability findings. A physical conclusion requires additional, independently informative measurements and a fuller treatment of uncertainty.
