#!/usr/bin/env python3
"""Tolerance-based comparison of two v72 raw -7M replay surface sets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


MODES = (
    "released_logL_plus_logprior",
    "maximum_log_likelihood_released_row",
)
SURFACES = ("H1", "L1", "network")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _path(directory: Path, mode: str) -> Path:
    return directory / f"GW250114_V72_RAW_MINUS7M_{mode}_surfaces.npz"


def _load(path: Path) -> dict[str, np.ndarray]:
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def _argmax_index(array: np.ndarray) -> list[int]:
    return [int(value) for value in np.unravel_index(np.argmax(array), array.shape)]


def _difference(candidate: np.ndarray, baseline: np.ndarray) -> dict[str, float]:
    difference = candidate - baseline
    centered = difference - np.mean(difference)
    return {
        "mean_additive_offset": float(np.mean(difference)),
        "standard_deviation": float(np.std(difference)),
        "peak_to_peak": float(np.ptp(difference)),
        "max_abs_without_offset_removal": float(np.max(np.abs(difference))),
        "centered_max_abs": float(np.max(np.abs(centered))),
        "centered_rms": float(np.sqrt(np.mean(centered**2))),
    }


def _validate_hex_digest(value: str, label: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare baseline and fresh fixed-conditioning -7M grid surfaces."
    )
    parser.add_argument("--baseline-dir", type=Path, required=True)
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--baseline-bundle-sha256", required=True)
    parser.add_argument("--candidate-preflight", type=Path, required=True)
    parser.add_argument("--centered-max-abs-tolerance", type=float, default=1e-5)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    _validate_hex_digest(args.baseline_bundle_sha256, "baseline bundle digest")
    if args.centered_max_abs_tolerance <= 0.0:
        raise ValueError("centered tolerance must be positive")

    preflight = json.loads(args.candidate_preflight.read_text())
    baseline = {mode: _load(_path(args.baseline_dir, mode)) for mode in MODES}
    candidate = {mode: _load(_path(args.candidate_dir, mode)) for mode in MODES}

    comparisons: dict[str, Any] = {}
    tests: list[dict[str, Any]] = [
        {
            "test": "candidate_preflight_passed",
            "pass": preflight.get("status") == "PASS",
        },
        {
            "test": "candidate_preflight_fixed_conditioning_scope",
            "pass": preflight.get("scope")
            == "FIXED_CONDITIONING_MINUS7M_85_BY_40_GRID_ONLY",
        },
    ]
    for mode in MODES:
        base = baseline[mode]
        fresh = candidate[mode]
        axes_exact = bool(
            np.array_equal(base["frequency_hz"], fresh["frequency_hz"])
            and np.array_equal(
                base["damping_rate_s_inv"], fresh["damping_rate_s_inv"]
            )
        )
        tests.append({"test": f"{mode}_axes_exact", "pass": axes_exact})
        mode_record: dict[str, Any] = {
            "baseline_file": {
                "name": _path(args.baseline_dir, mode).name,
                "sha256": sha256(_path(args.baseline_dir, mode)),
            },
            "candidate_file": {
                "name": _path(args.candidate_dir, mode).name,
                "sha256": sha256(_path(args.candidate_dir, mode)),
            },
            "axes_exact": axes_exact,
            "surfaces": {},
        }
        for surface in SURFACES:
            key = f"{surface}_log_likelihood"
            base_array = base[key]
            fresh_array = fresh[key]
            shape_and_finite = bool(
                base_array.shape == (85, 40)
                and fresh_array.shape == (85, 40)
                and np.all(np.isfinite(base_array))
                and np.all(np.isfinite(fresh_array))
            )
            maximum_exact = _argmax_index(base_array) == _argmax_index(fresh_array)
            difference = _difference(fresh_array, base_array)
            within_tolerance = (
                difference["centered_max_abs"]
                <= args.centered_max_abs_tolerance
            )
            mode_record["surfaces"][surface] = {
                "shape_and_finite": shape_and_finite,
                "baseline_argmax_index": _argmax_index(base_array),
                "candidate_argmax_index": _argmax_index(fresh_array),
                "argmax_exact": maximum_exact,
                "candidate_minus_baseline": difference,
                "centered_difference_within_tolerance": within_tolerance,
            }
            tests.extend(
                [
                    {
                        "test": f"{mode}_{surface}_shape_and_finite",
                        "pass": shape_and_finite,
                    },
                    {
                        "test": f"{mode}_{surface}_argmax_exact",
                        "pass": maximum_exact,
                    },
                    {
                        "test": f"{mode}_{surface}_centered_difference_within_tolerance",
                        "pass": within_tolerance,
                    },
                ]
            )

        base_additivity = (
            base["network_log_likelihood"]
            - base["H1_log_likelihood"]
            - base["L1_log_likelihood"]
        )
        fresh_additivity = (
            fresh["network_log_likelihood"]
            - fresh["H1_log_likelihood"]
            - fresh["L1_log_likelihood"]
        )
        additivity = {
            "baseline_max_abs": float(np.max(np.abs(base_additivity))),
            "candidate_max_abs": float(np.max(np.abs(fresh_additivity))),
            "threshold": 1e-10,
        }
        additivity_pass = bool(
            additivity["baseline_max_abs"] < additivity["threshold"]
            and additivity["candidate_max_abs"] < additivity["threshold"]
        )
        mode_record["detector_additivity_implementation_identity"] = additivity
        tests.append(
            {
                "test": f"{mode}_detector_additivity_identity",
                "pass": additivity_pass,
            }
        )

        cached_exact = bool(
            np.array_equal(
                base["released_cached_network_log_likelihood"],
                fresh["released_cached_network_log_likelihood"],
            )
        )
        mode_record["released_cached_surface_exact"] = cached_exact
        tests.append(
            {"test": f"{mode}_released_cached_surface_exact", "pass": cached_exact}
        )
        comparisons[mode] = mode_record

    passed = sum(bool(test["pass"]) for test in tests)
    receipt = {
        "version": "GW250114_HRF_v72_raw_surface_comparison_v1",
        "status": "PASS" if passed == len(tests) else "FAIL",
        "scope": "FIXED_CONDITIONING_MINUS7M_85_BY_40_GRID_ONLY",
        "baseline_bundle_sha256": args.baseline_bundle_sha256,
        "candidate_preflight": {
            "name": args.candidate_preflight.name,
            "sha256": sha256(args.candidate_preflight),
            "qnm_filter_source": preflight.get("qnm_filter_source"),
            "runtime": preflight.get("runtime"),
        },
        "comparison_rule": {
            "log_likelihood_additive_offset_removed": True,
            "centered_max_abs_tolerance": args.centered_max_abs_tolerance,
            "grid_axes_and_argmax_indices_must_be_exact": True,
        },
        "comparisons": comparisons,
        "self_test": {"passed": passed, "total": len(tests), "tests": tests},
        "qualification": (
            "This receipt compares numerical replay surfaces for the fixed-conditioning "
            "-7M grid up to an irrelevant additive log-likelihood constant. It does not "
            "reproduce the full Nature inference or establish HRF, area-quantization, "
            "or quantum-horizon evidence."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "self_test": receipt["self_test"]}, indent=2))
    if receipt["status"] != "PASS":
        raise RuntimeError(f"surface comparison failed: {passed}/{len(tests)}")


if __name__ == "__main__":
    main()
