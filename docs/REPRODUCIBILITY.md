# Reproducibility: what can be checked here

## Offline integrity check

Run from the repository root:

```sh
python3 tools/verify_release.py
```

Python 3.9 or later is sufficient; no third-party package is needed. The check reads files without modifying or executing the scientific package. It verifies:

1. The exact membership and SHA-256 of the 15 files in `release/v5.3/`, using the repository's `MANIFEST.sha256`.
2. The exact membership and bytes of the 57 files in `research/v72/` against the preserved focused ZIP.
3. ZIP integrity as focused members are read.

A passing result establishes agreement with the supplied manifest and archive. It is not independent authentication if someone changes both the manifest and files. Compare the originals with the [published Zenodo deposit](https://zenodo.org/records/22400638) when provenance matters.

## Mathematical and saved-array checks

The original focused package contains theorem proofs, numerical design code, saved arrays, package audits, requirements, and recorded environment information. These are preserved, including their historical dates and defaults. The [September 5 audit](../release/v5.3/GW250114_V72_PUBLICATION_AUDIT_2026-09-05.md) specifies which checks were actually repeated then and which raw-workflow receipts were inherited.

For the September offline mathematical/saved-surface checking workflow, extract `release/v5.3/GW250114_V5_3_PUBLICATION_VERIFICATION_SUPPLEMENT.zip` into a separate working directory and read its included instructions. Its numerical checks have their own dependencies and scope. They do not rerun the strain pipeline.

Preserve this repository's original publication and focused directories. If running scientific generators, use a separate working copy and configure input/output directories according to the scripts' command-line help. Some archived defaults use `/mnt/data`; those reflect the historical environment. Do not assume that path exists on your computer, or replace preserved outputs with a fresh run.

## A new raw replay needs external inputs

The repository does not bundle the official H1/L1 strain, posterior HDF5, original companion archive/checkout, or imported `qnm_filter` source snapshot. Acquisition references and recorded checksums are in [SOURCES.md](../research/v72/SOURCES.md), [package provenance](../research/v72/PACKAGE_PROVENANCE.md), and the original preflight records. The archived raw-replay scripts and Pixi environment are starting documentation, not a promise that downloading this repository alone recreates the full workflow.

A new raw run must acquire the referenced inputs, satisfy the original provenance/preflight requirements, and record its own environment and receipts. Never substitute passing archived receipts for checks of a newly acquired environment. The GitHub publication work did not perform a new raw fit or execute the historical research scripts.

## What a scientific advance would require

The [next-analysis protocol](../release/v5.3/NEXT_ANALYSIS_PROTOCOL_DRAFT.md) is a draft, not a preregistration or executed study. The open work includes a physically defined additional observable, a full joint likelihood, admitted nuisance and calibration uncertainty, global separation, and full-search null calibration. Existing event data have already been inspected; a later reanalysis does not make those observations retrospectively blind.

Integrity, arithmetic consistency, repeatable numerical output, and physical inference answer different questions. Report which one a check addresses.
