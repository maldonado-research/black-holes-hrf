# Black Holes: Quantized Horizon Response (HRF)

[Readable project overview](https://maldonado-research.github.io/projects/black-holes-hrf/) · [All research projects](https://maldonado-research.github.io/)


**A research hypothesis, its statistical limits, and reproducible methods for GW250114.**

By [Ricardo Maldonado](https://orcid.org/0009-0009-3937-6527). This repository distributes the published **Zenodo v5.3 / research package v72**, with readable source files and an offline integrity check. The GitHub companion was prepared on September 30, 2026; the scientific archives remain unchanged.

[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22400638-blue)](https://doi.org/10.5281/zenodo.22400638)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey)](LICENSE)

## In More Basic Terms

When two black holes merge, the new black hole settles down by sending out gravitational waves. Think of the fading sound of a bell after it is struck. Here, the question is whether that signal could help us test a proposed response at a black hole's horizon.

Before treating an unusual result as new physics, we need to know whether the calculation can be repeated and whether different explanations can actually be told apart. This release works on those questions. An archived calculation closely matches a reference grid when the chosen assumptions are fixed. Changing the selected input row, however, moves the best-fitting damping rate enough to matter.

There is also a basic limit to an exact-value test. If nearby values produce increasingly similar measurements, one finite experiment cannot reliably separate one exact number from every number arbitrarily close to it. A useful test needs clearly defined competing possibilities and an honest treatment of uncertainty.

The progress is a clearer, more reproducible test. **The release does not establish an HRF detection, a quantum horizon, or a unified theory of everything.**

## Start here

| For | Read |
|---|---|
| A short explanation and reading order | [Reader guide (PDF)](release/v5.3/GW250114_V5_3_READER_GUIDE.pdf) |
| Current scope, corrections, and qualifications | [September publication audit](release/v5.3/GW250114_V72_PUBLICATION_AUDIT_2026-09-05.md) |
| The mathematical argument | [Theorem and proof](research/v72/GW250114_V72_THEOREM_AND_PROOF.md) |
| Archived calculation and numerical evidence | [Main v72 report](research/v72/GW250114_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.md) |
| Source code, tables, figures, and saved surfaces | [Browsable v72 package](research/v72/) |
| Exact published files and cumulative history | [Original v5.3 publication files](release/v5.3/) |
| Integrity checking and reproduction limits | [Reproducibility guide](docs/REPRODUCIBILITY.md) |
| Proposed next scientific work | [Next-analysis protocol — draft](release/v5.3/NEXT_ANALYSIS_PROTOCOL_DRAFT.md) |

## What the work reports

- Under the stated total-variation continuity condition, an exact point target has zero uniform separation from alternatives approaching that point. The stated randomized minimax maximum error is one half. This does not rule out learning about fixed, separated alternatives.
- The stipulated Gaussian design gives a distance of **3.7810604375** for one named competitor and **4.3486867653 per endpoint** for the corrected two-endpoint procedure. The associated historical-gap widths, **0.115190902%** and **0.100155239%**, are design requirements, not measured GW250114 precision. These procedures are distinct; an endpoint score is not automatically a composite Bayes factor.
- The archived fixed-conditioning −7M replay contains an **85 × 40** grid. Its released-row network maximum is **200 Hz, 450 s⁻¹**; the alternate released row gives **200 Hz, 420 s⁻¹**. Several quantities change together, so the comparison does not isolate one parameter's causal effect.
- The archived centered cache-to-raw maximum discrepancy is below **7.8 × 10⁻⁵ log-likelihood units**. This is evidence about the specified computation, not independent astrophysical confirmation.

Read each result with the assumptions in the [publication audit](release/v5.3/GW250114_V72_PUBLICATION_AUDIT_2026-09-05.md). Full nuisance, calibration, global-identification, and search-null calibration questions remain unresolved. No exact ln(4) or g = 4 identification, area quantization, or black-hole microstate inference is established.

## Check the preserved files

From a downloaded or cloned repository, run:

```sh
python3 tools/verify_release.py
```

This uses only the Python standard library and works offline. It checks all **15 original publication files** against `MANIFEST.sha256` and all **57 browsable focused-package files** against the preserved ZIP. It does not run a new raw-strain analysis. For scientific reproduction, see [the guide](docs/REPRODUCIBILITY.md).

## Versions and provenance

- **v72** is the internal research checkpoint, sealed August 17, 2026. Some historical generated documents carry July 12 dates.
- **v5.3** is the Zenodo publication version, published September 5, 2026: [record 22400638](https://zenodo.org/records/22400638).
- **GitHub v5.3** is a companion distribution of those bytes, with new navigation, citation, and integrity-checking documentation. It does not denote a new scientific analysis.

Historical files retain their original preparation language, recommendations, and recorded results. Their publication-status wording is superseded by the published Zenodo record; the September audit supplies the documented residual-sign correction. See [provenance and corrections](docs/PROVENANCE.md).

## Cite and reuse

Maldonado, Ricardo. (2026). *Quantized Horizon Response (HRF): Composite-Alternative Separation and Fixed-Conditioning GW250114 Replay — v5.3*. Zenodo. https://doi.org/10.5281/zenodo.22400638

Machine-readable citation: [CITATION.cff](CITATION.cff). The version-independent series DOI is [10.5281/zenodo.18050128](https://doi.org/10.5281/zenodo.18050128).

The author's release retains [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), matching Zenodo. External data, publications, and dependencies retain their own rights and attribution; see [external sources](docs/THIRD_PARTY.md).

AI assistance was used for release documentation, packaging, and stated local checks. Those checks and public hosting are not independent peer review. Questions, reproducibility reports, and specific mathematical critiques are welcome through this repository's Issues page; please identify the file, version, and assumptions involved.
