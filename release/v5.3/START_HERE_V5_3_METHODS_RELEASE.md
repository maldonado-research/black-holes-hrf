# GW250114 HRF: v5.3 methods and reproducibility release

**Author:** Ricardo Maldonado  
**Prepared:** 2026-09-05  
**Research package:** v72, sealed 2026-08-17  
**Intended series:** next version of Zenodo record 20192925 (locally documented as v5.2). Online version history must be checked before publication.

## In More Basic Terms

After two black holes merge, the resulting black hole settles down through gravitational waves, somewhat like a struck bell ringing down. This project investigates whether a proposed horizon-response model could eventually be tested with those signals.

This release improves the reliability of the test. The archived v72 analysis reports that, when specified assumptions are held fixed, its calculation closely reproduces an existing reference grid. But using a different released set of assumptions moves the best-fitting damping rate. That means reproducing the calculation does not, by itself, establish a new physical effect.

The mathematics also explains a limit of measurement: a finite experiment cannot uniformly separate one exact value from every value arbitrarily close to it when the observable distributions vary continuously in the stated sense. A useful test must define how far apart alternatives must be, or use a clearly specified interval or Bayesian comparison. Checking two alternatives at once also requires stricter control than checking just one.

The progress here is a more reproducible calculation, corrected statistical comparison rules, and a clearer account of what remains untested. It does not establish a unified theory of everything, quantum structure at a black-hole horizon, or detection of the proposed HRF effect.

## What this release makes available

The preserved v72 package contains the composite-alternative closure argument, least-favorable Gaussian separation and design calculations, numerical surfaces and receipts from the fixed-conditioning GW250114 replay, and recovery/release audits. The master archive preserves the preceding methods packages as historical context. This publication adds a reader guide, a dated local verification report, and a proposed next-analysis protocol explicitly marked as a draft.

The research numbering (v72) and Zenodo publication numbering (proposed v5.3) describe different things. No new raw-strain fit or discovery is implied by the publication version. This September preparation preserves the original sealed research archives and their SHA-256 sidecars.

## Key results and their limits

- Under the stated total-variation continuity condition, an exact point target has zero uniform separation from a continuous alternative that excludes only that point. With randomized tests, the stated minimax maximum error is one half. This does not prohibit consistency against each fixed separated alternative.
- In the stipulated Gaussian design model, one preregistered named competitor requires distance at least 3.7810604375 for a score greater than ln(10) with target-side probability at least 0.90. At the historical log gap, the corresponding effective width is at most 0.115190902%.
- For the symmetric two-endpoint exclusion rule, the corrected distance is at least 4.3486867653 per endpoint, giving a 90% joint-success lower bound and effective width at most 0.100155239%. These widths are design screens, not measured uncertainty for GW250114. The endpoint score is not automatically a composite Bayes factor.
- The archived fixed-conditioning -7M replay evaluates an 85 x 40 grid. Its released-row network maximum is 200 Hz and 450 inverse seconds. The alternate released row gives 200 Hz and 420 inverse seconds. Several active parameters change together; this is a joint conditioning sensitivity check, not a measurement of one parameter's causal effect.
- The archived centered cache-to-raw discrepancy is below 7.8e-5 log-likelihood units. Detector/network quadratic additivity is an arithmetic implementation check, not independent astrophysical validation.

For the target tau = ln(4), the log coordinate is lambda = ln(tau), so lambda_0 = ln(ln(4)). These coordinates must not be conflated.

## What was checked for this publication

The September 2026 publication audit distinguishes checks performed on the supplied local files from results recorded in the August package. The official strain, posterior data, and external source checkout required for a new raw replay are not contained in the supplied release. Therefore historical raw preflight, finalizer, and comparison receipts are evidence preserved from that workflow, not a newly executed raw analysis in this preparation.

See `GW250114_V72_PUBLICATION_AUDIT_2026-09-05.md` for the exact fresh checks, limitations, and any corrections to the explanatory prose. Its dated verification statements supplement the historical reports without silently rewriting them.

## What remains unresolved

A real joint likelihood that completes the observable information, detector-aware remnant and quasinormal-mode inference, nuisance and calibration uncertainty, global target-to-alternative separation, and full-search null calibration remain unresolved. The existing conditional detector surfaces are not detector-only validation results. Both detectors' event data have already been inspected; a new detector-disjoint reanalysis does not retroactively make them blind validation data.

The accompanying next-analysis document is a planning draft. It is not a preregistration, an executed experiment, or a new result. All physical interpretation gates remain closed. No HRF detection, exact ln(4) or g=4 identification, area quantization, black-hole microstate inference, or quantum-horizon claim is admitted.

## Read the files in this order

1. This guide or `GW250114_V5_3_READER_GUIDE.pdf` for the scope and plain-language explanation.
2. `GW250114_V72_PUBLICATION_AUDIT_2026-09-05.md` for newly performed verification and caveats.
3. `GW250114_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.md` and `GW250114_V72_ONE_PAGE_CERTIFICATE.md` for the detailed methods and historical results.
4. `HRF_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.zip` for the focused computational release, with its `.sha256` file.
5. `GW250114_MASTER_PROGRESS_BUNDLE_v72.zip` for the cumulative research history, with its `.sha256` file. Earlier claims in historical files must be read through the current v72 qualifications.
6. The original recovery audit and final release verification for the August chain of custody; `NEXT_ANALYSIS_PROTOCOL_DRAFT.md` for proposed future work.
7. `GW250114_V5_3_PUBLICATION_VERIFICATION_SUPPLEMENT.zip` for a portable offline verifier, its instructions and dated machine-readable results. It rechecks the focused package, numerical kernel and saved surfaces; it does not execute a new raw-strain analysis. `PUBLICATION_FILES_MANIFEST.json` and `SHA256SUMS.txt` cover the selected publication files.

The original reports carry both July 12 document dates and August 17 recovery/release dates. They are preserved as supplied; the preparation date above does not relabel the historical computations. Historical reports recommended deferring another Zenodo release until an observable-complete analysis or documented negative outcome. At the author's request, this preparation is scoped as a methods/reproducibility deposit with no physical promotion.

## Provenance and acknowledgments

The prior version is identified in the local project history as [Zenodo record 20192925](https://zenodo.org/records/20192925), with series concept DOI [10.5281/zenodo.18050128](https://doi.org/10.5281/zenodo.18050128). These local records require live confirmation before a new version is published. The v72 package's `SOURCES.md` identifies the external scientific inputs and their provenance.

The September reader guide, packaging, and local verification were prepared with AI assistance in Codex. Automated checks establish their stated computational scope; they do not constitute independent peer review. The original research archives are retained byte-for-byte.
