#!/usr/bin/env python3
"""Fail-closed package audit for GW250114 HRF v72.

This checks internal artifact consistency only.  It is not an independent
astrophysical analysis and cannot promote any physical claim.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUDIT_DIR = ROOT / "audits"
AUDIT_JSON = AUDIT_DIR / "GW250114_V72_REPRODUCIBILITY_AUDIT.json"
AUDIT_MD = AUDIT_DIR / "GW250114_V72_REPRODUCIBILITY_AUDIT.md"

ONE_COMPETITOR_DISTANCE = 3.7810604375308374
ONE_COMPETITOR_Q_PERCENT = 0.11519090213259128
TWO_SIDED_DISTANCE = 4.348686765309589
TWO_SIDED_Q_PERCENT = 0.100155239115278


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def near(a: float, b: float, atol: float = 1e-12, rtol: float = 1e-10) -> bool:
    return math.isclose(float(a), float(b), abs_tol=atol, rel_tol=rtol)


def check_manifest(path: Path, key: str) -> tuple[bool, str]:
    if not path.is_file():
        return False, f"{path.name}:missing"
    manifest = json.loads(path.read_text())
    errors: list[str] = []
    seen: set[str] = set()
    for item in manifest.get("files", []):
        rel = item[key]
        if rel in seen:
            errors.append(rel + ":duplicate")
            continue
        seen.add(rel)
        candidate = Path(rel)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(rel + ":unsafe")
            continue
        target = ROOT / rel
        if not target.is_file():
            errors.append(rel + ":missing")
            continue
        if target.stat().st_size != int(item["bytes"]):
            errors.append(rel + ":size")
        if sha256(target) != item["sha256"]:
            errors.append(rel + ":sha256")
    return not errors, "ok" if not errors else ",".join(errors)


def receipt_pass(path: Path) -> tuple[bool, str]:
    """Accept a deterministic PASS receipt while checking any supplied counts/tests."""
    if not path.is_file():
        return False, f"{path.name}:missing"
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        return False, f"{path.name}:invalid JSON ({exc})"
    if not isinstance(data, dict):
        return False, f"{path.name}:top level is not an object"

    status = str(data.get("status", "")).upper()
    ok = status == "PASS"
    details = [f"status={status or 'missing'}"]

    count_pairs = (("passed", "total"), ("n_passed", "n_tests"))
    for passed_key, total_key in count_pairs:
        if passed_key in data or total_key in data:
            count_ok = (
                isinstance(data.get(passed_key), int)
                and isinstance(data.get(total_key), int)
                and data[passed_key] == data[total_key]
                and data[total_key] > 0
            )
            ok &= count_ok
            details.append(f"{passed_key}/{total_key}={data.get(passed_key)}/{data.get(total_key)}")

    if isinstance(data.get("tests"), list):
        test_flags: list[bool] = []
        for test in data["tests"]:
            if not isinstance(test, dict):
                test_flags.append(False)
            elif "passed" in test:
                test_flags.append(test["passed"] is True)
            elif "pass" in test:
                test_flags.append(test["pass"] is True)
        if test_flags:
            ok &= all(test_flags)
            details.append(f"tests={sum(test_flags)}/{len(test_flags)}")
    return ok, "; ".join(details)


def filter_calls_use_polarization(path: Path) -> tuple[bool, str]:
    """Reject an executed filter call that explicitly receives psi/polarization."""
    try:
        tree = ast.parse(path.read_text())
    except Exception as exc:
        return True, f"cannot parse replay source ({exc})"
    bad: list[str] = []
    names = {"psi", "psi_rad", "polarization", "polarization_angle"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = ast.unparse(node.func).lower()
        if "filter" not in func and "network" not in func:
            continue
        explicit = {keyword.arg for keyword in node.keywords if keyword.arg}
        if explicit & names:
            bad.append(f"line {node.lineno}: {sorted(explicit & names)}")
        call_tokens = {
            child.id
            for child in ast.walk(node)
            if isinstance(child, ast.Name)
        }
        call_tokens.update(
            child.value
            for child in ast.walk(node)
            if isinstance(child, ast.Constant) and isinstance(child.value, str)
        )
        if call_tokens & names:
            bad.append(f"line {node.lineno}: call tokens {sorted(call_tokens & names)}")
    return bool(bad), "none" if not bad else "; ".join(bad)


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")
    return struct.unpack(">II", header[16:24])


def main() -> None:
    tests: list[dict[str, object]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        tests.append({"name": name, "passed": bool(passed), "detail": detail})

    math_test = json.loads((ROOT / "GW250114_V72_math_self_test.json").read_text())
    raw_test = json.loads((ROOT / "GW250114_V72_RAW_MINUS7M_SELF_TEST.json").read_text())
    math_summary = json.loads((ROOT / "GW250114_V72_math_summary.json").read_text())
    raw = json.loads((ROOT / "GW250114_V72_RAW_MINUS7M_AUDIT.json").read_text())
    summary = json.loads((ROOT / "GW250114_V72_summary.json").read_text())

    add("math_self_tests", math_test["status"] == "PASS"
        and math_test["n_passed"] == math_test["n_tests"] == 17,
        f"{math_test['n_passed']}/{math_test['n_tests']}")
    add("raw_self_tests", raw_test["passed"] == raw_test["total"] and raw_test["total"] >= 12,
        f"{raw_test['passed']}/{raw_test['total']}")

    ok, detail = check_manifest(ROOT / "GW250114_V72_math_manifest.json", "name")
    add("math_submanifest", ok, detail)
    math_manifest = json.loads((ROOT / "GW250114_V72_math_manifest.json").read_text())
    math_generator = ROOT / math_manifest["generator"]["name"]
    generator_ok = math_generator.is_file() and sha256(math_generator) == math_manifest["generator"]["sha256"]
    add("math_generator_hash", generator_ok,
        f"name={math_generator.name}, sha256={sha256(math_generator) if math_generator.is_file() else 'missing'}")
    ok, detail = check_manifest(ROOT / "GW250114_V72_RAW_MINUS7M_MANIFEST.json", "path")
    add("raw_submanifest", ok, detail)

    closure = math_summary["continuous_alternative"]
    add("continuous_closure_exact_values",
        closure["unrestricted_punctured_continuum_uniform_distance"] == 0.0
        and closure["uniform_minimax_max_error"] == 0.5,
        f"distance={closure['unrestricted_punctured_continuum_uniform_distance']}, "
        f"error={closure['uniform_minimax_max_error']}")

    strict = math_summary["strict_least_favourable_gate"]
    add("one_competitor_strict_distance",
        strict.get("scope") == "one preregistered named competitor"
        and near(strict["required_distance"], ONE_COMPETITOR_DISTANCE),
        f"scope={strict.get('scope')}; D={strict['required_distance']}")
    add("one_competitor_historical_gap_width",
        near(strict["max_q_eff_at_old_gap_percent"], ONE_COMPETITOR_Q_PERCENT),
        str(strict["max_q_eff_at_old_gap_percent"]))

    two_sided = math_summary["two_sided_exclusion_gate_at_historical_gap"]
    add("two_sided_endpoint_distance",
        two_sided.get("endpoint_competitors") == 2
        and near(two_sided["required_distance_each_endpoint"], TWO_SIDED_DISTANCE),
        f"K={two_sided.get('endpoint_competitors')}; D={two_sided['required_distance_each_endpoint']}")
    add("two_sided_historical_gap_width",
        near(two_sided["max_q_eff_at_old_gap_percent"], TWO_SIDED_Q_PERCENT),
        str(two_sided["max_q_eff_at_old_gap_percent"]))

    add("raw_grid_shape", raw["grid"]["shape"] == [85, 40], str(raw["grid"]["shape"]))
    released = raw["maxima"]["released_logL_plus_logprior"]["network"]
    cached = raw["maxima"]["released_cached_network"]
    add("raw_and_cache_same_maximum",
        released["frequency_hz"] == cached["frequency_hz"] == 200.0
        and released["damping_rate_s_inv"] == cached["damping_rate_s_inv"] == 450.0,
        f"raw=({released['frequency_hz']},{released['damping_rate_s_inv']}), "
        f"cache=({cached['frequency_hz']},{cached['damping_rate_s_inv']})")

    max_add = max(v["max_abs_error"] for v in raw["detector_additivity"].values())
    add("detector_additivity", max_add < 1e-10, f"max_abs={max_add:.3e}")
    residual = raw["released_cache_comparison_up_to_additive_constant"]["centered_max_abs"]
    add("cache_residual", residual < 1e-3, f"centered_max_abs={residual:.3e}")
    ml = raw["maxima"]["maximum_log_likelihood_released_row"]["network"]
    add("row_sensitivity_detected",
        ml["damping_rate_s_inv"] == 420.0 and released["damping_rate_s_inv"] == 450.0,
        f"released={released['damping_rate_s_inv']}, ML-row={ml['damping_rate_s_inv']}")

    add("summary_raw_residual_consistency",
        near(summary["raw_minus7M"]["cache_raw_centered_max_abs_log_likelihood"], residual),
        str(summary["raw_minus7M"]["cache_raw_centered_max_abs_log_likelihood"]))
    add("summary_distance_consistency",
        near(summary["least_favorable_gate"]["required_distance"], strict["required_distance"]),
        str(summary["least_favorable_gate"]["required_distance"]))
    add("summary_two_sided_consistency",
        near(summary["two_sided_exclusion_gate"]["required_distance_each_endpoint"],
             two_sided["required_distance_each_endpoint"])
        and near(summary["two_sided_exclusion_gate"]["max_q_eff_percent"],
                 two_sided["max_q_eff_at_old_gap_percent"]),
        f"D={summary['two_sided_exclusion_gate']['required_distance_each_endpoint']}; "
        f"q%={summary['two_sided_exclusion_gate']['max_q_eff_percent']}")

    raw_scope = str(summary["raw_minus7M"].get("scope", ""))
    full_nature_gate = str(summary.get("gates", {}).get("full_nature_inference", ""))
    add("fixed_conditioning_scope",
        "fixed-conditioning" in raw_scope.lower()
        and "85x40" in raw_scope.lower()
        and "not the full nature inference" in raw_scope.lower(),
        raw_scope)
    add("full_nature_inference_not_reproduced",
        full_nature_gate == "NOT_REPRODUCED",
        f"full_nature_inference={full_nature_gate or 'missing'}")

    report_text = (ROOT / "GW250114_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.md").read_text()
    raw_report_text = (ROOT / "GW250114_V72_RAW_MINUS7M_REPLAY_AUDIT.md").read_text()
    combined_report_text = (report_text + "\n" + raw_report_text).lower()
    replay_source = ROOT / "gw250114_v72_raw_minus7m_replay.py"
    has_polarization_call, polarization_call_detail = filter_calls_use_polarization(replay_source)
    add("no_polarization_filter_attribution",
        "polarization" in combined_report_text
        and "not passed" in combined_report_text
        and not has_polarization_call,
        f"explicit no-pass qualification={('polarization' in combined_report_text and 'not passed' in combined_report_text)}; "
        f"filter-call psi/polarization keywords={polarization_call_detail}")

    preflight_ok, preflight_detail = receipt_pass(ROOT / "GW250114_V72_RAW_PREFLIGHT.json")
    add("raw_preflight_receipt", preflight_ok, preflight_detail)
    compare_ok, compare_detail = receipt_pass(ROOT / "GW250114_V72_FRESH_REPLAY_COMPARISON.json")
    add("fresh_replay_comparison_receipt", compare_ok, compare_detail)
    expected_repro_scripts = (
        ROOT / "gw250114_v72_raw_preflight.py",
        ROOT / "gw250114_v72_raw_surface_compare.py",
    )
    missing_repro_scripts = [path.name for path in expected_repro_scripts if not path.is_file()]
    add("preflight_and_comparator_scripts_present", not missing_repro_scripts,
        "ok" if not missing_repro_scripts else "missing=" + ",".join(missing_repro_scripts))

    # Deliberately exclude this audit's JSON output.  Otherwise the first run
    # changes the reported JSON count, which changes its own bytes and makes a
    # top-level manifest impossible to reproduce idempotently.
    json_files = sorted(
        path for path in ROOT.rglob("*.json")
        if path.resolve() != AUDIT_JSON.resolve()
    )
    json_ok = True
    json_error = "ok"
    try:
        for path in json_files:
            json.loads(path.read_text())
    except Exception as exc:  # pragma: no cover - diagnostic path
        json_ok = False
        json_error = f"{path.name}: {exc}"
    add("all_json_parse", json_ok, f"{len(json_files)} files; {json_error}")

    csv_files = sorted(ROOT.rglob("*.csv"))
    csv_ok = True
    csv_rows = 0
    csv_error = "ok"
    try:
        for path in csv_files:
            with path.open(newline="") as stream:
                rows = list(csv.reader(stream))
            csv_ok &= len(rows) >= 2
            csv_rows += max(0, len(rows) - 1)
    except Exception as exc:  # pragma: no cover - diagnostic path
        csv_ok = False
        csv_error = f"{path.name}: {exc}"
    add("all_csv_parse_nonempty", csv_ok, f"{len(csv_files)} files, {csv_rows} data rows; {csv_error}")

    png_files = sorted(ROOT.rglob("*.png"))
    png_ok = True
    dims: list[str] = []
    try:
        for path in png_files:
            width, height = png_dimensions(path)
            png_ok &= width >= 600 and height >= 400
            dims.append(f"{path.name}:{width}x{height}")
    except Exception as exc:  # pragma: no cover - diagnostic path
        png_ok = False
        dims.append(str(exc))
    add("png_integrity_and_dimensions", png_ok, "; ".join(dims))

    gate_rows = list(csv.DictReader((ROOT / "GW250114_V72_gate_status.csv").open()))
    physical = next(row for row in gate_rows if row["gate"] == "physical_ln4_g4_area_quantization_interpretation")
    add("physical_gate_locked", physical["status"] == "LOCKED" and physical["admitted"] == "false",
        f"status={physical['status']}, admitted={physical['admitted']}")

    passed = sum(bool(item["passed"]) for item in tests)
    audit = {
        "version": "GW250114_HRF_v72_package_audit",
        "date": "2026-07-12",
        "status": "PASS" if passed == len(tests) else "FAIL",
        "passed": passed,
        "total": len(tests),
        "tests": tests,
        "claim_boundary": "Internal reproducibility only; no HRF detection or physical branch claim."
    }
    AUDIT_DIR.mkdir(exist_ok=True)
    AUDIT_JSON.write_text(json.dumps(audit, indent=2) + "\n")
    md_lines = [
        "# GW250114 HRF v72 — Reproducibility audit", "",
        f"**Status:** `{audit['status']}` — `{passed}/{len(tests)}` checks passed.", "",
        "| Check | Status | Detail |", "|---|---|---|",
    ]
    for item in tests:
        detail_text = str(item["detail"]).replace("|", "\\|")
        md_lines.append(f"| `{item['name']}` | {'PASS' if item['passed'] else 'FAIL'} | {detail_text} |")
    md_lines.extend(["", "This audit checks package consistency only. It does not validate an HRF signal or physical interpretation.", ""])
    AUDIT_MD.write_text("\n".join(md_lines))
    print(json.dumps(audit, indent=2))
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
