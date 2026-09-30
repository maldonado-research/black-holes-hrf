#!/usr/bin/env python3
"""Finalize and validate the v72 raw -7M replay artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from gw250114_v72_raw_preflight import run_preflight


RELEASED_MODE = "released_logL_plus_logprior"
ML_MODE = "maximum_log_likelihood_released_row"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def maximum(array: np.ndarray, hz: np.ndarray, rate: np.ndarray) -> dict[str, float]:
    i, j = np.unravel_index(np.argmax(array), array.shape)
    return {
        "frequency_hz": float(hz[j]),
        "damping_rate_s_inv": float(rate[i]),
        "decay_time_ms": float(1000.0 / rate[i]),
        "log_likelihood": float(array[i, j]),
    }


def centered_metrics(first: np.ndarray, second: np.ndarray, label: str) -> dict[str, float | str]:
    difference = first - second
    centered = difference - np.mean(difference)
    return {
        "definition": label,
        "mean_additive_offset": float(np.mean(difference)),
        "standard_deviation": float(np.std(difference)),
        "peak_to_peak": float(np.ptp(difference)),
        "centered_max_abs": float(np.max(np.abs(centered))),
        "centered_rms": float(np.sqrt(np.mean(centered**2))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--nature-zip", type=Path, required=True)
    parser.add_argument("--posterior", type=Path, required=True)
    parser.add_argument("--h1", type=Path, required=True)
    parser.add_argument("--l1", type=Path, required=True)
    parser.add_argument("--cached", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--toml", type=Path, required=True)
    parser.add_argument("--qnm-filter-source", type=Path, required=True)
    parser.add_argument("--pixi-bin", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    args = parser.parse_args()

    stored_preflight = json.loads(args.preflight.read_text())
    current_preflight = run_preflight(
        posterior=args.posterior,
        h1=args.h1,
        l1=args.l1,
        cached=args.cached,
        nature_zip=args.nature_zip,
        lock=args.lock,
        toml=args.toml,
        qnm_filter_source=args.qnm_filter_source,
        pixi_bin=args.pixi_bin,
        receipt_path=None,
    )
    if stored_preflight != current_preflight:
        raise RuntimeError(
            "stored preflight receipt does not match the current inputs/source/runtime"
        )

    released_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_{RELEASED_MODE}_surfaces.npz"
    ml_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_{ML_MODE}_surfaces.npz"
    released_audit_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_AUDIT_{RELEASED_MODE}.json"
    ml_audit_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_AUDIT_{ML_MODE}.json"
    replay_script = args.outdir / "gw250114_v72_raw_minus7m_replay.py"
    preflight_script = args.outdir / "gw250114_v72_raw_preflight.py"
    finalizer_script = Path(__file__)
    lock_path = args.lock
    toml_path = args.toml

    released_npz = np.load(released_path)
    ml_npz = np.load(ml_path)
    hz = released_npz["frequency_hz"]
    rate = released_npz["damping_rate_s_inv"]
    released = {key: released_npz[f"{key}_log_likelihood"] for key in ("H1", "L1", "network")}
    ml = {key: ml_npz[f"{key}_log_likelihood"] for key in ("H1", "L1", "network")}
    cached = released_npz["released_cached_network_log_likelihood"]
    ml_cached = ml_npz["released_cached_network_log_likelihood"]
    released_mode_audit = json.loads(released_audit_path.read_text())
    ml_mode_audit = json.loads(ml_audit_path.read_text())
    released_record = released_mode_audit["modes"][RELEASED_MODE]
    ml_record = ml_mode_audit["modes"][ML_MODE]

    released_additivity = released["network"] - released["H1"] - released["L1"]
    ml_additivity = ml["network"] - ml["H1"] - ml["L1"]
    cache_comparison = centered_metrics(
        cached,
        released["network"],
        "released cached network logL minus raw released-row network logL",
    )
    row_sensitivity = centered_metrics(
        ml["network"],
        released["network"],
        "maximum-log-likelihood-row network logL minus released-logL+logPrior-row network logL",
    )

    maxima = {
        RELEASED_MODE: {surface: maximum(array, hz, rate) for surface, array in released.items()},
        ML_MODE: {surface: maximum(array, hz, rate) for surface, array in ml.items()},
        "released_cached_network": maximum(cached, hz, rate),
    }

    extent = [float(hz[0]), float(hz[-1]), float(rate[0]), float(rate[-1])]
    fig, axes = plt.subplots(2, 3, figsize=(12.0, 7.2), constrained_layout=True)
    panels = [
        (released["H1"] - np.max(released["H1"]), "Released row: H1 relative logL", "viridis"),
        (released["L1"] - np.max(released["L1"]), "Released row: L1 relative logL", "viridis"),
        (released["network"] - np.max(released["network"]), "Released row: H1+L1 relative logL", "viridis"),
        (cached - released["network"] - np.mean(cached - released["network"]), "Cached - raw, additive offset removed", "coolwarm"),
        (ml["network"] - np.max(ml["network"]), "Maximum-logL row: network relative logL", "viridis"),
        (ml["network"] - released["network"] - np.mean(ml["network"] - released["network"]), "Maximum-logL row - released row, centered", "coolwarm"),
    ]
    for axis, (data, title, cmap) in zip(axes.flat, panels):
        if cmap == "viridis":
            image = axis.imshow(
                np.maximum(data, -12.0), origin="lower", aspect="auto", extent=extent,
                cmap=cmap, vmin=-12.0, vmax=0.0,
            )
        else:
            bound = float(np.max(np.abs(data)))
            image = axis.imshow(
                data, origin="lower", aspect="auto", extent=extent,
                cmap=cmap, vmin=-bound, vmax=bound,
            )
        axis.set_title(title, fontsize=9)
        axis.set_xlabel("frequency [Hz]")
        axis.set_ylabel("damping rate [s$^{-1}$]")
        fig.colorbar(image, ax=axis, shrink=0.84)
    figure_path = args.outdir / "GW250114_V72_RAW_MINUS7M_DETECTOR_NETWORK_AUDIT.png"
    fig.savefig(
        figure_path,
        dpi=180,
        metadata={"Software": "GW250114 HRF v72 raw replay audit"},
    )
    plt.close(fig)

    actual_input_hashes = {
        **{
            record["name"]: record["sha256"]
            for record in current_preflight["files"].values()
        },
        args.preflight.name: sha256(args.preflight),
        replay_script.name: sha256(replay_script),
        preflight_script.name: sha256(preflight_script),
        finalizer_script.name: sha256(finalizer_script),
    }

    tests = [
        {"test": "stored_preflight_receipt_is_current_and_passed", "pass": stored_preflight == current_preflight and current_preflight["status"] == "PASS"},
        {"test": "preflight_scope_is_fixed_conditioning_minus7M_grid", "pass": current_preflight["scope"] == "FIXED_CONDITIONING_MINUS7M_85_BY_40_GRID_ONLY"},
        {"test": "preflight_qnm_source_is_frozen_and_clean", "pass": current_preflight["qnm_filter_source"]["git_commit"] == "55f14436d4ea510b71754b95da9701009e8a1c12" and current_preflight["qnm_filter_source"]["git_tree"] == "377f807dd345a138c32d274f3cb746f60dd0cecf" and current_preflight["qnm_filter_source"]["worktree_clean"] is True},
        {"test": "preflight_runtime_is_actual_python_3_11", "pass": current_preflight["runtime"]["python"]["major_minor"] == "3.11"},
        {"test": "grid_shape_is_85_by_40", "pass": all(array.shape == (85, 40) for array in (*released.values(), *ml.values(), cached))},
        {"test": "grid_axes_exact", "pass": bool(np.array_equal(hz, np.arange(160.0, 240.0, 2.0)) and np.array_equal(rate, np.arange(50.0, 900.0, 10.0)))},
        {"test": "all_surfaces_finite", "pass": all(bool(np.all(np.isfinite(array))) for array in (*released.values(), *ml.values(), cached))},
        {"test": "released_detector_additivity", "pass": bool(np.max(np.abs(released_additivity)) < 1e-10)},
        {"test": "maximum_logL_row_detector_additivity", "pass": bool(np.max(np.abs(ml_additivity)) < 1e-10)},
        {"test": "released_cache_and_raw_have_same_grid_maximum", "pass": maxima[RELEASED_MODE]["network"]["frequency_hz"] == maxima["released_cached_network"]["frequency_hz"] and maxima[RELEASED_MODE]["network"]["damping_rate_s_inv"] == maxima["released_cached_network"]["damping_rate_s_inv"]},
        {"test": "released_cache_centered_residual_below_1e-3_logL", "pass": cache_comparison["centered_max_abs"] < 1e-3},
        {"test": "released_row_index_exact", "pass": released_record["posterior_row"]["row_index"] == 10740},
        {"test": "maximum_logL_row_index_exact", "pass": ml_record["posterior_row"]["row_index"] == 19989},
        {"test": "single_mode_audits_match_current_replay_and_preflight_scripts", "pass": released_mode_audit["input_hashes_sha256"][replay_script.name] == actual_input_hashes[replay_script.name] and ml_mode_audit["input_hashes_sha256"][replay_script.name] == actual_input_hashes[replay_script.name] and released_mode_audit["input_hashes_sha256"][preflight_script.name] == actual_input_hashes[preflight_script.name] and ml_mode_audit["input_hashes_sha256"][preflight_script.name] == actual_input_hashes[preflight_script.name]},
        {"test": "single_mode_audits_match_current_preflight_receipt", "pass": released_mode_audit["preflight"]["receipt_sha256"] == actual_input_hashes[args.preflight.name] and ml_mode_audit["preflight"]["receipt_sha256"] == actual_input_hashes[args.preflight.name]},
        {"test": "single_mode_surface_hashes_match", "pass": released_mode_audit["output_hashes_sha256"][released_path.name] == sha256(released_path) and ml_mode_audit["output_hashes_sha256"][ml_path.name] == sha256(ml_path)},
    ]
    passed = sum(bool(item["pass"]) for item in tests)
    if passed != len(tests):
        raise RuntimeError(f"self-test failed: {passed}/{len(tests)}")

    audit = {
        "version": "GW250114_HRF_v72_raw_minus7M_final_audit",
        "status": "FIXED_CONDITIONING_GRID_REPRODUCTION_AND_CONDITIONAL_DETECTOR_DECOMPOSITION_ONLY",
        "verdict": "RAW_MINUS7M_FIXED_GRID_REPRODUCED_DETECTOR_ADDITIVITY_IDENTITY_PASS_ROW_SENSITIVITY_LARGE",
        "grid": {"shape": [85, 40], "frequency_hz": [160.0, 238.0, 2.0], "damping_rate_s_inv": [50.0, 890.0, 10.0], "start_time_remnant_mass_units": -7.0},
        "environment": {
            **current_preflight["runtime"],
            "pixi_lock_sha256": actual_input_hashes[lock_path.name],
            "pixi_toml_sha256": actual_input_hashes[toml_path.name],
            "qnm_filter_source": current_preflight["qnm_filter_source"],
            "note": "Runtime values were queried by the validated preflight; no hard-coded version string is used.",
        },
        "preflight": {
            "receipt": args.preflight.name,
            "receipt_sha256": actual_input_hashes[args.preflight.name],
            "self_test": current_preflight["self_test"],
        },
        "input_hashes_sha256": actual_input_hashes,
        "posterior_rows": {RELEASED_MODE: released_record["posterior_row"], ML_MODE: ml_record["posterior_row"]},
        "maxima": maxima,
        "detector_additivity": {RELEASED_MODE: {"max_abs_error": float(np.max(np.abs(released_additivity)))}, ML_MODE: {"max_abs_error": float(np.max(np.abs(ml_additivity)))}},
        "released_cache_comparison_up_to_additive_constant": cache_comparison,
        "maximum_log_likelihood_row_sensitivity": row_sensitivity,
        "timings_seconds": {RELEASED_MODE: {key: released_record[key] for key in ("prep_seconds", "grid_seconds", "total_seconds")}, ML_MODE: {key: ml_record[key] for key in ("prep_seconds", "grid_seconds", "total_seconds")}},
        "artifact_hashes_sha256": {released_path.name: sha256(released_path), ml_path.name: sha256(ml_path), figure_path.name: sha256(figure_path), released_audit_path.name: sha256(released_audit_path), ml_audit_path.name: sha256(ml_audit_path), args.preflight.name: sha256(args.preflight)},
        "self_test": {"passed": passed, "total": len(tests)},
        "qualification": "This audit covers the released companion's fixed-conditioning -7M 85x40 grid, not the full Nature inference. The detector surfaces are conditional per-detector quadratic contributions at one released posterior-row remnant/sky/time point, and additivity is an implementation identity rather than independent validation. They are not detector-specific remnant inference, HRF branch evidence, area quantization, or a quantum-horizon claim. The maximum-log-likelihood-row lane is a sensitivity audit among released rows, not a continuous maximum-likelihood optimization.",
    }
    audit_path = args.outdir / "GW250114_V72_RAW_MINUS7M_AUDIT.json"
    audit_path.write_text(json.dumps(audit, indent=2) + "\n")

    csv_path = args.outdir / "GW250114_V72_RAW_MINUS7M_AUDIT.csv"
    rows = []
    for mode, surfaces in ((RELEASED_MODE, released), (ML_MODE, ml)):
        for surface, array in surfaces.items():
            item = maximum(array, hz, rate)
            rows.append({"mode": mode, "surface": surface, **item, "posterior_row_index": audit["posterior_rows"][mode]["row_index"], "conditional_only": True})
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    self_test_path = args.outdir / "GW250114_V72_RAW_MINUS7M_SELF_TEST.json"
    self_test_path.write_text(json.dumps({"passed": passed, "total": len(tests), "tests": tests}, indent=2) + "\n")

    manifest_entries = []
    manifest_path = args.outdir / "GW250114_V72_RAW_MINUS7M_MANIFEST.json"
    for path in sorted(args.outdir.iterdir()):
        if path.is_file() and path != manifest_path:
            manifest_entries.append({"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest_path.write_text(json.dumps({"version": audit["version"], "files": manifest_entries}, indent=2) + "\n")
    print(json.dumps({"verdict": audit["verdict"], "self_test": audit["self_test"], "manifest_files": len(manifest_entries)}, indent=2))


if __name__ == "__main__":
    main()
