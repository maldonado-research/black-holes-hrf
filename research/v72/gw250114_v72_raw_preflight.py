#!/usr/bin/env python3
"""Fail-closed provenance preflight for the GW250114 v72 raw -7M replay.

The receipt deliberately contains no wall-clock times or absolute input paths.
Given the same frozen inputs, source tree, and runtime, its JSON bytes are
reproducible.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import h5py
import numpy as np


PE_RUN = "bilby-NRSur7dq4_prod-reweighted"
POSTERIOR_DATASET = f"{PE_RUN}/posterior_samples"
EXPECTED_QNM_COMMIT = "55f14436d4ea510b71754b95da9701009e8a1c12"
EXPECTED_QNM_TREE = "377f807dd345a138c32d274f3cb746f60dd0cecf"
EXPECTED_FILE_DIGESTS = {
    "nature_zip": {
        "sha256": "752eb33b21ee1a332ad7282eb5ddee695d6cc1ec2859120c779e17fbfcd7c862",
        "md5": "4874fef35088209c9fa4073f15a27a78",
    },
    "posterior": {
        "sha256": "55b4a47c2c71580e9ef0cd1ff9fa9d32e64813657e9ea31f32e24cda53922d62",
        "md5": "9b115931b66439a1d5649a2b7b7aa143",
    },
    "h1": {
        "sha256": "23e20dda953d2ede852f4991c018b0f1128f35f2cec7153d835a312be363d19d",
    },
    "l1": {
        "sha256": "355dbcaece2b63b5ded9aa353e34b59a672edfd7845b0aa1b9bf73c5439bb825",
    },
    "cached": {
        "sha256": "c2f44f586ce256d053f564b512125ea857f519a556f79cbc9c1526da557f0667",
    },
}
REQUIRED_POSTERIOR_FIELDS = (
    "log_likelihood",
    "log_prior",
    "final_mass",
    "final_spin",
    "ra",
    "dec",
    "geocent_time",
    "psi",
)
PACKAGE_DISTRIBUTIONS = (
    "numpy",
    "scipy",
    "h5py",
    "matplotlib",
    "astropy",
    "gwpy",
    "gwsurrogate",
    "qnm-filter",
)


def file_digest(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256(path: Path) -> str:
    return file_digest(path, "sha256")


def _run(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def _decode_scalar(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, np.generic):
        return value.item()
    return value


def _record_frozen_file(role: str, path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"{role}: missing file: {path}")
    expected = EXPECTED_FILE_DIGESTS[role]
    record: dict[str, Any] = {
        "name": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    if "md5" in expected:
        record["md5"] = file_digest(path, "md5")
    for algorithm, expected_value in expected.items():
        if record[algorithm] != expected_value:
            raise RuntimeError(
                f"{role}: {algorithm} mismatch: {record[algorithm]} != {expected_value}"
            )
    return record


def _validate_posterior(path: Path) -> dict[str, Any]:
    with h5py.File(path, "r") as handle:
        if POSTERIOR_DATASET not in handle:
            raise RuntimeError(f"missing posterior dataset: {POSTERIOR_DATASET}")
        dataset = handle[POSTERIOR_DATASET]
        fields = tuple(dataset.dtype.names or ())
        missing = sorted(set(REQUIRED_POSTERIOR_FIELDS) - set(fields))
        if dataset.shape != (19990,):
            raise RuntimeError(f"unexpected posterior shape: {dataset.shape}")
        if missing:
            raise RuntimeError(f"missing posterior fields: {missing}")
        if any(dataset.dtype.fields[name][0] != np.dtype("<f8") for name in REQUIRED_POSTERIOR_FIELDS):
            raise RuntimeError("posterior replay fields are not little-endian float64")
    return {
        "dataset": POSTERIOR_DATASET,
        "shape": [19990],
        "required_fields": list(REQUIRED_POSTERIOR_FIELDS),
        "required_field_dtype": "float64-little-endian",
    }


def _validate_strain(path: Path, detector: str) -> dict[str, Any]:
    with h5py.File(path, "r") as handle:
        required = (
            "meta/Detector",
            "meta/Duration",
            "meta/GPSstart",
            "strain/Strain",
        )
        missing = [name for name in required if name not in handle]
        if missing:
            raise RuntimeError(f"{detector}: missing HDF5 objects: {missing}")
        dataset = handle["strain/Strain"]
        metadata = {
            "detector": _decode_scalar(handle["meta/Detector"][()]),
            "duration_s": int(handle["meta/Duration"][()]),
            "gps_start": int(handle["meta/GPSstart"][()]),
            "shape": list(dataset.shape),
            "dtype": str(dataset.dtype),
            "x_start": int(dataset.attrs["Xstart"]),
            "x_spacing_s": float(dataset.attrs["Xspacing"]),
            "n_points_attr": int(dataset.attrs["Npoints"]),
        }
    expected = {
        "detector": detector,
        "duration_s": 4096,
        "gps_start": 1420877824,
        "shape": [67108864],
        "dtype": "float64",
        "x_start": 1420877824,
        "x_spacing_s": 1.0 / 16384.0,
        "n_points_attr": 67108864,
    }
    if metadata != expected:
        raise RuntimeError(f"{detector}: unexpected strain schema: {metadata}")
    return metadata


def _validate_cached(path: Path) -> dict[str, Any]:
    with h5py.File(path, "r") as handle:
        if "likelihood_data" not in handle:
            raise RuntimeError("cached file lacks likelihood_data")
        dataset = handle["likelihood_data"]
        record = {
            "dataset": "likelihood_data",
            "shape": list(dataset.shape),
            "dtype": str(dataset.dtype),
            "all_finite": bool(np.all(np.isfinite(dataset[:]))),
            "frequency_bounds_hz": [float(value) for value in dataset.attrs["hz_bounds"]],
            "damping_rate_bounds_s_inv": [
                int(value) for value in dataset.attrs["invTau_bounds"]
            ],
            "delta_frequency_hz": int(dataset.attrs["delta_hz"]),
            "delta_damping_rate_s_inv": int(dataset.attrs["delta_invTau"]),
            "start_time_remnant_mass_units": float(dataset.attrs["time"]),
        }
    expected = {
        "dataset": "likelihood_data",
        "shape": [85, 40],
        "dtype": "float64",
        "all_finite": True,
        "frequency_bounds_hz": [160.0, 238.0],
        "damping_rate_bounds_s_inv": [50, 890],
        "delta_frequency_hz": 2,
        "delta_damping_rate_s_inv": 10,
        "start_time_remnant_mass_units": -7.0,
    }
    if record != expected:
        raise RuntimeError(f"unexpected cached likelihood schema: {record}")
    return record


def _validate_qnm_source(source: Path) -> dict[str, Any]:
    source = source.resolve()
    if not (source / ".git").is_dir():
        raise RuntimeError(f"qnm_filter source is not a Git worktree: {source}")
    commit = _run(["git", "-C", str(source), "rev-parse", "HEAD"])
    tree = _run(["git", "-C", str(source), "rev-parse", "HEAD^{tree}"])
    status = _run(["git", "-C", str(source), "status", "--porcelain=v1"])
    if commit != EXPECTED_QNM_COMMIT:
        raise RuntimeError(f"qnm_filter commit mismatch: {commit}")
    if tree != EXPECTED_QNM_TREE:
        raise RuntimeError(f"qnm_filter tree mismatch: {tree}")
    if status:
        raise RuntimeError("qnm_filter worktree is not clean")

    source_text = str(source)
    if source_text not in sys.path:
        sys.path.insert(0, source_text)
    importlib.invalidate_caches()
    module = importlib.import_module("qnm_filter")
    module_file = Path(module.__file__).resolve()
    try:
        relative_module_file = module_file.relative_to(source)
    except ValueError as error:
        raise RuntimeError(
            f"qnm_filter imported outside supplied source: {module_file}"
        ) from error
    return {
        "git_commit": commit,
        "git_tree": tree,
        "worktree_clean": True,
        "import_module_relative_path": relative_module_file.as_posix(),
    }


def _runtime_record(pixi_bin: Path) -> dict[str, Any]:
    if sys.version_info[:2] != (3, 11):
        raise RuntimeError(
            f"Python 3.11 is required; running {sys.version_info.major}.{sys.version_info.minor}"
        )
    if not pixi_bin.is_file():
        raise FileNotFoundError(f"missing Pixi executable: {pixi_bin}")
    pixi_version_output = _run([str(pixi_bin), "--version"])
    package_versions: dict[str, str] = {}
    for distribution in PACKAGE_DISTRIBUTIONS:
        try:
            package_versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError as error:
            raise RuntimeError(f"required distribution is unavailable: {distribution}") from error
    return {
        "python": {
            "implementation": sys.implementation.name,
            "version": ".".join(str(value) for value in sys.version_info[:3]),
            "major_minor": "3.11",
        },
        "pixi_version_output": pixi_version_output,
        "package_versions": package_versions,
    }


def run_preflight(
    *,
    posterior: Path,
    h1: Path,
    l1: Path,
    cached: Path,
    nature_zip: Path,
    lock: Path,
    toml: Path,
    qnm_filter_source: Path,
    pixi_bin: Path,
    receipt_path: Path | None,
) -> dict[str, Any]:
    """Validate every frozen dependency and optionally write the receipt."""
    paths = {
        "nature_zip": nature_zip,
        "posterior": posterior,
        "h1": h1,
        "l1": l1,
        "cached": cached,
    }
    files = {role: _record_frozen_file(role, path) for role, path in paths.items()}
    for role, path in (("pixi_lock", lock), ("pixi_toml", toml)):
        if not path.is_file():
            raise FileNotFoundError(f"{role}: missing file: {path}")
        files[role] = {
            "name": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }

    schemas = {
        "posterior": _validate_posterior(posterior),
        "h1_strain": _validate_strain(h1, "H1"),
        "l1_strain": _validate_strain(l1, "L1"),
        "released_minus7M_cache": _validate_cached(cached),
    }
    qnm_source = _validate_qnm_source(qnm_filter_source)
    runtime = _runtime_record(pixi_bin)
    tests = [
        {"test": "frozen_file_sha256_match", "pass": True},
        {"test": "official_md5_match_for_nature_zip_and_posterior", "pass": True},
        {"test": "posterior_hdf5_schema", "pass": True},
        {"test": "gwosc_h1_hdf5_schema", "pass": True},
        {"test": "gwosc_l1_hdf5_schema", "pass": True},
        {"test": "released_minus7M_cache_hdf5_schema", "pass": True},
        {"test": "python_runtime_is_3_11", "pass": True},
        {"test": "qnm_filter_commit_tree_clean_and_imported_from_supplied_source", "pass": True},
        {"test": "pixi_and_required_package_versions_queried", "pass": True},
    ]
    receipt = {
        "version": "GW250114_HRF_v72_raw_preflight_v1",
        "status": "PASS",
        "scope": "FIXED_CONDITIONING_MINUS7M_85_BY_40_GRID_ONLY",
        "files": files,
        "schemas": schemas,
        "qnm_filter_source": qnm_source,
        "runtime": runtime,
        "self_test": {"passed": len(tests), "total": len(tests), "tests": tests},
        "qualification": (
            "This preflight authenticates inputs, source, schemas, and runtime for the "
            "fixed-conditioning -7M grid replay. It does not reproduce the full Nature "
            "analysis or establish HRF, area-quantization, or quantum-horizon evidence."
        ),
    }
    if receipt_path is not None:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fail-closed provenance preflight for the v72 fixed-conditioning raw replay."
    )
    parser.add_argument("--posterior", type=Path, required=True)
    parser.add_argument("--h1", type=Path, required=True)
    parser.add_argument("--l1", type=Path, required=True)
    parser.add_argument("--cached", type=Path, required=True)
    parser.add_argument("--nature-zip", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--toml", type=Path, required=True)
    parser.add_argument("--qnm-filter-source", type=Path, required=True)
    parser.add_argument("--pixi-bin", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    receipt = run_preflight(
        posterior=args.posterior,
        h1=args.h1,
        l1=args.l1,
        cached=args.cached,
        nature_zip=args.nature_zip,
        lock=args.lock,
        toml=args.toml,
        qnm_filter_source=args.qnm_filter_source,
        pixi_bin=args.pixi_bin,
        receipt_path=args.out,
    )
    print(json.dumps({"status": receipt["status"], "receipt": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
