#!/usr/bin/env python3
"""Raw GW250114 -7M fixed-conditioning grid replay and decomposition.

This is a methods/reproduction audit.  It evaluates the released frequency-
damping model on official discovery-v1 strain.  It does not evaluate an HRF
branch, area quantization, a quantum-horizon interpretation, or the full
Nature analysis.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib
import json
import time
from pathlib import Path

import h5py
import numpy as np
import scipy.linalg as sl
from gwpy.timeseries import TimeSeries

from gw250114_v72_raw_preflight import run_preflight


PE_RUN = "bilby-NRSur7dq4_prod-reweighted"
MODEL_LIST = [(2, 2, 0, "p"), (2, 2, 1, "p"), (2, 2, 2, "p")]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def row_point(data: np.ndarray, index: int, mode: str) -> dict[str, float | int | str]:
    row = data[index]
    final_mass_name = "final_mass" if "final_mass" in data.dtype.names else "final_mass_non_evolved"
    final_spin_name = "final_spin" if "final_spin" in data.dtype.names else "final_spin_non_evolved"
    return {
        "mode": mode,
        "row_index": int(index),
        "selection_objective": (
            "argmax(log_likelihood + log_prior) used by released companion"
            if mode == "released_logL_plus_logprior"
            else "argmax(log_likelihood) among released posterior rows"
        ),
        "log_likelihood": float(row["log_likelihood"]),
        "log_prior": float(row["log_prior"]),
        "log_likelihood_plus_log_prior": float(row["log_likelihood"] + row["log_prior"]),
        "final_mass_detector_msun": float(row[final_mass_name]),
        "final_spin": float(row[final_spin_name]),
        "ra_rad": float(row["ra"]),
        "dec_rad": float(row["dec"]),
        "geocent_time_gps": float(row["geocent_time"]),
        "psi_rad": float(row["psi"]),
    }


def load_row_and_data(
    posterior_path: Path,
    strain_paths: dict[str, Path],
    mode: str,
) -> tuple[dict, dict, dict, h5py.File]:
    posterior_file = h5py.File(posterior_path, "r")
    posterior = posterior_file[PE_RUN]["posterior_samples"]
    data = posterior[:]
    if mode == "released_logL_plus_logprior":
        index = int(np.argmax(data["log_likelihood"] + data["log_prior"]))
    elif mode == "maximum_log_likelihood_released_row":
        index = int(np.argmax(data["log_likelihood"]))
    else:
        raise ValueError(mode)

    point = row_point(data, index, mode)
    event_time = point["geocent_time_gps"]
    real_data: dict[str, qnm_filter.RealData] = {}
    noise_data: dict[str, qnm_filter.RealData] = {}
    for detector, path in strain_paths.items():
        event = TimeSeries.read(
            path,
            start=event_time - 2.0,
            end=event_time + 2.0,
            format="hdf5.gwosc",
        )
        noise = TimeSeries.read(
            path,
            start=event_time + 1.0,
            end=event_time + 65.0,
            format="hdf5.gwosc",
        )
        real_data[detector] = qnm_filter.RealData(event.value, index=event.times.value)
        noise_data[detector] = qnm_filter.RealData(noise.value, index=noise.times.value)
    return point, real_data, noise_data, posterior_file


def argmax_record(array: np.ndarray, hz: np.ndarray, rate: np.ndarray) -> dict[str, float]:
    i, j = np.unravel_index(np.argmax(array), array.shape)
    return {
        "frequency_hz": float(hz[j]),
        "damping_rate_s_inv": float(rate[i]),
        "decay_time_ms": float(1000.0 / rate[i]),
        "log_likelihood": float(array[i, j]),
    }


def evaluate_mode(
    posterior_path: Path,
    strain_paths: dict[str, Path],
    mode: str,
    cached: np.ndarray,
    hz: np.ndarray,
    rate: np.ndarray,
) -> tuple[dict, dict[str, np.ndarray]]:
    start = time.perf_counter()
    point, real_data, noise_data, posterior_file = load_row_and_data(
        posterior_path, strain_paths, mode
    )
    mass = point["final_mass_detector_msun"]
    spin = point["final_spin"]
    mass_unit = qnm_filter.Filter.mass_unit(mass)
    filter_shift = qnm_filter.compute_filter_time_shift(
        spin, MODEL_LIST, True, mass
    )
    time_offset = -7.0 * mass_unit - filter_shift
    options = {
        "model_list": MODEL_LIST,
        "t_init": point["geocent_time_gps"] + time_offset,
        "segment_length": 0.2,
        "srate": 8192,
        "ra": point["ra_rad"],
        "dec": point["dec_rad"],
        "flow": 20,
        "trim": 0.1,
    }

    network = qnm_filter.Network(**options)
    network.original_data = copy.deepcopy(real_data)
    network.pure_noise = copy.deepcopy(noise_data)
    network.detector_alignment()
    network.condition_data("original_data", **options)
    network.condition_data("pure_noise", **options)
    network.compute_acfs("pure_noise")
    network.cholesky_decomposition()
    network.first_index()
    network.add_filter(mass=mass, chi=spin, model_list=MODEL_LIST)
    prep_seconds = time.perf_counter() - start

    h1 = np.empty((len(rate), len(hz)))
    l1 = np.empty_like(h1)
    joint = np.empty_like(h1)
    max_additivity_error = 0.0
    grid_start = time.perf_counter()
    for i, damping_rate in enumerate(rate):
        for j, frequency in enumerate(hz):
            network.add_ftau_filter(2.0 * np.pi * frequency, 1.0 / damping_rate)
            truncated = network.truncate_data(network.filtered_ftau_data)
            contributions = {}
            for detector, detector_data in truncated.items():
                whitened = sl.solve_triangular(
                    network.cholesky_L[detector], detector_data, lower=True
                )
                contributions[detector] = -0.5 * float(np.dot(whitened, whitened))
            h1[i, j] = contributions["H1"]
            l1[i, j] = contributions["L1"]
            joint[i, j] = network.compute_likelihood_ftau()
            max_additivity_error = max(
                max_additivity_error,
                abs(joint[i, j] - h1[i, j] - l1[i, j]),
            )
    grid_seconds = time.perf_counter() - grid_start
    posterior_file.close()

    metrics = {
        "posterior_row": point,
        "mass_unit_s": float(mass_unit),
        "qnm_filter_time_shift_s": float(filter_shift),
        "minus7M_time_offset_s": float(time_offset),
        "detector_start_times_gps": {
            detector: float(value) for detector, value in network.start_times.items()
        },
        "conditioned_sampling_n": int(network.sampling_n),
        "prep_seconds": prep_seconds,
        "grid_seconds": grid_seconds,
        "total_seconds": time.perf_counter() - start,
        "network_argmax": argmax_record(joint, hz, rate),
        "H1_argmax": argmax_record(h1, hz, rate),
        "L1_argmax": argmax_record(l1, hz, rate),
        "detector_additivity_max_abs_error": float(max_additivity_error),
    }
    if mode == "released_logL_plus_logprior":
        residual = cached - joint
        centered = residual - np.mean(residual)
        metrics["released_cache_comparison"] = {
            "cached_argmax": argmax_record(cached, hz, rate),
            "cached_minus_raw_mean": float(np.mean(residual)),
            "cached_minus_raw_std": float(np.std(residual)),
            "cached_minus_raw_ptp": float(np.ptp(residual)),
            "cached_minus_raw_max_abs": float(np.max(np.abs(residual))),
            "cached_minus_raw_centered_max_abs": float(np.max(np.abs(centered))),
            "cached_minus_raw_centered_rms": float(np.sqrt(np.mean(centered**2))),
        }
    return metrics, {"H1": h1, "L1": l1, "network": joint}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posterior", type=Path, required=True)
    parser.add_argument("--h1", type=Path, required=True)
    parser.add_argument("--l1", type=Path, required=True)
    parser.add_argument("--cached", type=Path, required=True)
    parser.add_argument("--nature-zip", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--toml", type=Path, required=True)
    parser.add_argument("--qnm-filter-source", type=Path, required=True)
    parser.add_argument("--pixi-bin", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument(
        "--only-mode",
        choices=("released_logL_plus_logprior", "maximum_log_likelihood_released_row"),
        help="Run one posterior-row lane in a fresh process to bound memory use.",
    )
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    # This is deliberately before loading the cached surface or strain slices,
    # constructing the network, or entering the 3,400-point likelihood loop.
    preflight_receipt_path = args.outdir / "GW250114_V72_RAW_PREFLIGHT.json"
    preflight = run_preflight(
        posterior=args.posterior,
        h1=args.h1,
        l1=args.l1,
        cached=args.cached,
        nature_zip=args.nature_zip,
        lock=args.lock,
        toml=args.toml,
        qnm_filter_source=args.qnm_filter_source,
        pixi_bin=args.pixi_bin,
        receipt_path=preflight_receipt_path,
    )
    global qnm_filter
    qnm_filter = importlib.import_module("qnm_filter")

    hz = np.arange(160.0, 240.0, 2.0)
    rate = np.arange(50.0, 900.0, 10.0)
    with h5py.File(args.cached, "r") as handle:
        cached = handle["likelihood_data"][:]
    if cached.shape != (85, 40):
        raise ValueError(f"unexpected cached shape {cached.shape}")

    all_modes = ("released_logL_plus_logprior", "maximum_log_likelihood_released_row")
    modes = (args.only_mode,) if args.only_mode else all_modes
    metrics: dict[str, dict] = {}
    arrays: dict[str, dict[str, np.ndarray]] = {}
    output_hashes: dict[str, str] = {}
    for mode in modes:
        metrics[mode], arrays[mode] = evaluate_mode(
            args.posterior,
            {"H1": args.h1, "L1": args.l1},
            mode,
            cached,
            hz,
            rate,
        )
        output_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_{mode}_surfaces.npz"
        np.savez_compressed(
            output_path,
            frequency_hz=hz,
            damping_rate_s_inv=rate,
            H1_log_likelihood=arrays[mode]["H1"],
            L1_log_likelihood=arrays[mode]["L1"],
            network_log_likelihood=arrays[mode]["network"],
            released_cached_network_log_likelihood=cached,
        )
        output_hashes[output_path.name] = sha256(output_path)

    sensitivity_record = None
    if len(modes) == 2:
        released = arrays["released_logL_plus_logprior"]["network"]
        maximum_log_likelihood = arrays["maximum_log_likelihood_released_row"]["network"]
        sensitivity = maximum_log_likelihood - released
        sensitivity_centered = sensitivity - np.mean(sensitivity)
        sensitivity_record = {
            "ML_minus_released_surface_mean": float(np.mean(sensitivity)),
            "ML_minus_released_surface_std": float(np.std(sensitivity)),
            "ML_minus_released_surface_ptp": float(np.ptp(sensitivity)),
            "ML_minus_released_centered_max_abs": float(
                np.max(np.abs(sensitivity_centered))
            ),
            "ML_minus_released_centered_rms": float(
                np.sqrt(np.mean(sensitivity_centered**2))
            ),
        }
    audit = {
        "version": "GW250114_HRF_v72_raw_minus7M_audit",
        "status": "FIXED_CONDITIONING_GRID_REPRODUCTION_AND_CONDITIONAL_DETECTOR_DECOMPOSITION_ONLY",
        "grid": {
            "shape": [85, 40],
            "frequency_hz": [160.0, 238.0, 2.0],
            "damping_rate_s_inv": [50.0, 890.0, 10.0],
            "start_time_remnant_mass_units": -7.0,
        },
        "preflight": {
            "status": preflight["status"],
            "receipt": preflight_receipt_path.name,
            "receipt_sha256": sha256(preflight_receipt_path),
            "qnm_filter_source": preflight["qnm_filter_source"],
            "runtime": preflight["runtime"],
        },
        "input_hashes_sha256": {
            **{
                record["name"]: record["sha256"]
                for record in preflight["files"].values()
            },
            preflight_receipt_path.name: sha256(preflight_receipt_path),
            Path(__file__).name: sha256(Path(__file__)),
            "gw250114_v72_raw_preflight.py": sha256(
                Path(__file__).with_name("gw250114_v72_raw_preflight.py")
            ),
        },
        "modes": metrics,
        "maximum_log_likelihood_row_sensitivity": sensitivity_record,
        "output_hashes_sha256": output_hashes,
        "active_conditioning_inputs": [
            "final_mass",
            "final_spin",
            "ra",
            "dec",
            "geocent_time",
        ],
        "recorded_but_not_passed_to_qnm_filter": ["psi"],
        "qualification": (
            "This is the released companion's fixed-conditioning -7M 85x40 grid "
            "evaluated on official discovery-v1 strain. Detector surfaces are "
            "conditional per-detector quadratic contributions at one posterior-row "
            "remnant/sky/time point and their sum is an implementation identity. "
            "This is not the full Nature inference, detector-specific remnant inference, "
            "HRF branch evidence, area quantization, or a quantum-horizon claim."
        ),
    }

    suffix = f"_{args.only_mode}" if args.only_mode else ""
    json_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_AUDIT{suffix}.json"
    json_path.write_text(json.dumps(audit, indent=2) + "\n")
    csv_path = args.outdir / f"GW250114_V72_RAW_MINUS7M_AUDIT{suffix}.csv"
    csv_rows = []
    for mode in modes:
        item = metrics[mode]
        for surface in ("network", "H1", "L1"):
            maximum = item[f"{surface}_argmax"]
            csv_rows.append(
                {
                    "mode": mode,
                    "surface": surface,
                    "row_index": item["posterior_row"]["row_index"],
                    "frequency_hz": maximum["frequency_hz"],
                    "damping_rate_s_inv": maximum["damping_rate_s_inv"],
                    "decay_time_ms": maximum["decay_time_ms"],
                    "log_likelihood": maximum["log_likelihood"],
                    "additivity_max_abs_error": item["detector_additivity_max_abs_error"],
                    "prep_seconds": item["prep_seconds"],
                    "grid_seconds": item["grid_seconds"],
                    "qualification": audit["qualification"],
                }
            )
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)

    output_hashes[json_path.name] = sha256(json_path)
    output_hashes[csv_path.name] = sha256(csv_path)
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
