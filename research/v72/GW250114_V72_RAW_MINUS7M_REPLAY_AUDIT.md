# GW250114 HRF v72 — Official raw `-7M` replay audit

**Scope:** reproduction of the complete released fixed-conditioning `-7M`, `85x40` frequency–damping grid and detector arithmetic. It is not the full Nature inference and not an HRF branch analysis.

## Inputs

| Input | SHA-256 |
|---|---|
| `GW250114_horizon_signatures.zip` | `752eb33b21ee1a332ad7282eb5ddee695d6cc1ec2859120c779e17fbfcd7c862` |
| `posterior_samples_NRSur7dq4.h5` | `55b4a47c2c71580e9ef0cd1ff9fa9d32e64813657e9ea31f32e24cda53922d62` |
| H1 16-kHz discovery-v1 strain | `23e20dda953d2ede852f4991c018b0f1128f35f2cec7153d835a312be363d19d` |
| L1 16-kHz discovery-v1 strain | `355dbcaece2b63b5ded9aa353e34b59a672edfd7845b0aa1b9bf73c5439bb825` |
| released cached `DW_ftau_-7.0M.h5` | `c2f44f586ce256d053f564b512125ea857f519a556f79cbc9c1526da557f0667` |
| generated `pixi.lock` | `c03b7bc6f4ef5e05e7d0d745c2abbe7c121d323a2e07eb104291340edb56b612` |
| augmented `pixi.toml` | `a0ebdd9478cec8fdf8d714ac15d4cd205250f987cc38a1d1617387570d32b6fd` |

The official Zenodo MD5 values also match: `4874fef35088209c9fa4073f15a27a78` for the Nature ZIP and `9b115931b66439a1d5649a2b7b7aa143` for the NRSur7dq4 posterior.

The Nature companion's `pixi.toml` requests Python 3.11, `gwpy<4`, `gwsurrogate>=1.1.8,<2`, Astropy below 6, SciPy below 1.15, `natsort`, and the bundled editable `qnm_filter`. It did not include `pixi.lock`; v72 generated the packaged lock from that contract. The preflight now verifies the actually imported module path, commit `55f14436d4ea510b71754b95da9701009e8a1c12`, Git tree `377f807dd345a138c32d274f3cb746f60dd0cecf`, and clean tracked state before any grid evaluation. The separate NRSur7dq4 waveform asset is not used by this calculation and is no longer claimed as part of the certified replay.

Official raw binaries and the unused NRSur waveform asset are intentionally not repackaged.

## Fail-closed runtime receipt

Before either grid was evaluated, the packaged preflight passed `9/9` checks. It queried Python `3.11.15`, Pixi `0.76.2`, NumPy `1.26.4`, SciPy `1.14.1`, h5py `3.16.0`, Matplotlib `3.11.0`, Astropy `5.3.4`, GWpy `3.0.14`, gwsurrogate `1.1.8`, and `qnm-filter` `0.1`; none of these version strings was hard-coded into the result. The finalizer then passed `16/16` artifact/provenance checks.

## Frozen calculation

- released start-time lane: `-7M`;
- direct-wave QNM filter list: `(2,2,0,+)`, `(2,2,1,+)`, `(2,2,2,+)`;
- frequency grid: `160–238 Hz`, step `2 Hz`, 40 values;
- damping-rate grid: `50–890 s^-1`, step `10 s^-1`, 85 values;
- total: 3400 points per surface;
- event window: 4 seconds;
- ACF/noise window: event time `+1` to `+65` seconds;
- conditioning rate: 8192 Hz;
- flow: 20 Hz;
- segment: 0.2 seconds;
- trim: 0.1 seconds.

The calculation evaluates the network likelihood and, at every point, the separate H1 and L1 whitened quadratic contributions using the same conditioning objects. The pointwise additivity audit is performed before any centering.

## Released-point reproduction

The released implementation selects posterior row `10740`, which maximizes `log_likelihood+log_prior` among the released NRSur7dq4 samples. Its relevant values are:

- remnant detector-frame mass: `67.9279907026 Msun`;
- remnant spin: `0.67250922944`;
- geocentric time: `1420878141.236719`;
- mass unit: `0.3345787033 ms`;
- QNM-filter shift: `2.7894715078 ms`;
- total `-7M` time offset including shift: `-5.1315224309 ms`.

Results:

| Surface | Maximum |
|---|---|
| released cached network | `200 Hz, 450 s^-1` |
| raw network | `200 Hz, 450 s^-1` |
| raw H1 contribution | `200 Hz, 390 s^-1` |
| raw L1 contribution | `198 Hz, 510 s^-1` |

For the released cached network minus the raw network:

| Diagnostic | Value |
|---|---:|
| mean offset | `-2.36552523e-4` |
| standard deviation / centered RMS | `3.50989416e-5` |
| centered maximum absolute residual | `7.73435552e-5` |
| point-to-point range | `1.50174969e-4` |

The raw detector-additivity maximum absolute error is `1.13686838e-13`.

The small nonconstant cache residual is consistent with numerical/environment differences. The fail-closed Python 3.11 replay reproduced the same grid maxima. Its `26/26` comparator checks preserved every axis and maximum index, with largest fresh-versus-recovered centered surface difference `3.07161e-7`, below the declared `1e-5` numerical-replay threshold. The cache residual is below the separate `1e-3` log-likelihood cache-reproduction tolerance. No topology or downstream astrophysical-impact metric is asserted.

## Released-row objective sensitivity

Row `19989` has the largest `log_likelihood` among released posterior rows. The active replay inputs differ in remnant mass/spin, right ascension, declination, and geocentric time. `psi` is recorded but is not passed into `qnm_filter`. Re-running the same raw grid yields:

| Surface | Maximum |
|---|---|
| raw network | `200 Hz, 420 s^-1` |
| raw H1 contribution | `202 Hz, 360 s^-1` |
| raw L1 contribution | `202 Hz, 480 s^-1` |

After mean-centering the maximum-log-likelihood-row minus released-proxy-row network surfaces:

| Diagnostic | Value |
|---|---:|
| centered RMS | `4.03722354` |
| centered maximum absolute difference | `14.3581211` |
| point-to-point range | `19.7060848` |

This is a sensitivity diagnostic between two released posterior samples, not a continuous optimization and not a calibrated systematic distribution. Because the active inputs move together, it cannot attribute the shift to any one nuisance. It is large enough to keep the point-selection/remnant-conditioning gate open.

## Gates

```text
OFFICIAL_INPUT_INTEGRITY_PASS
RUNTIME_AND_QNM_SOURCE_FAIL_CLOSED_PREFLIGHT_PASS
FRESH_REPLAY_TOLERANCE_COMPARATOR_PASS
FIXED_CONDITIONING_RAW_MINUS7M_GRID_CACHE_REPRODUCTION_PASS
CONDITIONAL_RAW_POINTWISE_DETECTOR_QUADRATIC_ARITHMETIC_PASS
CONDITIONAL_DETECTOR_SURFACES_GENERATED
RELEASED_POINT_SELECTION_SENSITIVITY_MATERIAL_NOT_RESOLVED
DETECTOR_SPECIFIC_REMNANT_QNM_INFERENCE_NOT_EXECUTED
RAW_HRF_BRANCH_LIKELIHOOD_NOT_EXECUTED
```

## Interpretation boundary

The raw replay confirms that the released fixed-conditioning `-7M` frequency–damping grid can be reproduced from official open strain in the v72 runtime. Detector additivity is an implementation identity for the independent-detector quadratic objective, not independent physical validation. The replay does not reproduce the full Nature marginalization or establish that the frequency tracks horizon angular velocity or surface gravity, that the damping time is constant, that an extra HRF component exists, or that any lattice branch is selected.
