# Sources

## Official GW250114 data and analysis products

1. GWOSC, **GW250114_082203 event page**, discovery-paper release v1. Provides public H1/L1 strain links and event metadata.  
   https://gwosc.org/eventapi/html/O4_Discovery_Papers/GW250114_082203/v1/

2. LVK, **GW250114 discovery paper figure scripts**, Zenodo record 16877102. The release also provides the parameter-estimation HDF5 products including `posterior_samples_NRSur7dq4.h5`.  
   https://zenodo.org/records/16877102

3. **GW250114 horizon-signatures companion archive**, Zenodo record 20017347, published 2026-06-24. Provides `GW250114_horizon_signatures.zip`, plotting/analysis code, cached likelihood grids, and the embedded `qnm_filter` source snapshot.  
   https://zenodo.org/records/20017347

4. Companion `README.md` inside `GW250114_horizon_signatures.zip`. It identifies arXiv:2510.01001, documents the Pixi execution route, and records embedded `qnm_filter` commit `55f14436d4ea510b71754b95da9701009e8a1c12`.

## Statistical references

5. Standard results used explicitly: total-variation continuity of test expectations; convex projection/supporting-hyperplane inequalities; Gaussian likelihood-ratio testing; generalized least squares and Moore–Penrose projection; Schur-complement efficient Fisher information; Bonferroni/union bound. The v72 theorem document supplies self-contained proofs for the exact statements used.

## Project lineage

6. `GW250114_MASTER_PROGRESS_BUNDLE_v71.zip`, SHA-256 `a491c495c6ae4910fe747254af60246ae18ca22762a4b4ec35b4872dc0690b3a`, is the canonical parent checkpoint.

7. `HRF_V71_NUISANCE_QUOTIENT_COVARIANCE_AND_DECONDITIONING_GATE.zip`, SHA-256 `efe2dcceebc344234eb6d6678f990bc611223219ec2ea3906946fc76fd8abb0b`, is the standalone mathematical/statistical parent.

## Scope note

Cross-project TOE, dark-sector, antimatter, HDBLAST, PTA, and other hypothesis archives were available only as methodological reference. No claims, equations, priors, or physical assumptions from those projects were imported into the v72 black-hole calculation.
