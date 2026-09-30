#!/usr/bin/env python3
"""Deterministic v72 theorem/numerics generator.

Scope
-----
This is a methods-only calculation.  It does not analyze strain and it does not
claim an HRF detection, ln(4) identification, area quantization, or quantum
horizon physics.

The generator implements:

* the zero-uniform-separation obstruction for an unrestricted continuous-tau
  alternative that accumulates at the target point;
* least-favourable Gaussian separation and exact affine nuisance quotients;
* exclusion-radius and finite-composite precision budgets;
* a deterministic bias/precision frontier;
* exact two-observable resource allocation examples; and
* shared- versus detector-specific nuisance alias examples.

Only NumPy, Matplotlib, and the Python standard library are required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


VERSION = "GW250114_HRF_v72_math"
DATE = "2026-07-12"
TAU_TARGET = math.log(4.0)
TAU_OLD_COMPETITOR = 1.3802695723157803
DELTA_LOG = math.log(TAU_TARGET / TAU_OLD_COMPETITOR)
LOG_MARGIN = math.log(10.0)
TARGET_PROBABILITY = 0.90
Z_TARGET = NormalDist().inv_cdf(TARGET_PROBABILITY)
D_STRICT = Z_TARGET + math.sqrt(Z_TARGET**2 + 2.0 * LOG_MARGIN)
Q_STRICT = DELTA_LOG / D_STRICT
TWO_SIDED_ENDPOINTS = 2
TWO_SIDED_MISS_PER_ENDPOINT = (1.0 - TARGET_PROBABILITY) / TWO_SIDED_ENDPOINTS
Z_TWO_SIDED = NormalDist().inv_cdf(1.0 - TWO_SIDED_MISS_PER_ENDPOINT)
D_TWO_SIDED = Z_TWO_SIDED + math.sqrt(Z_TWO_SIDED**2 + 2.0 * LOG_MARGIN)


def normal_cdf(x: float) -> float:
    return NormalDist().cdf(float(x))


def normal_log_survival(x: float) -> float:
    """Stable log P[Z>x] for a standard normal variate."""
    x = float(x)
    if x < 8.0:
        return math.log(0.5 * math.erfc(x / math.sqrt(2.0)))
    inv2 = 1.0 / (x * x)
    series = 1.0 - inv2 + 3.0 * inv2**2 - 15.0 * inv2**3 + 105.0 * inv2**4
    return -0.5 * x * x - math.log(x) - 0.5 * math.log(2.0 * math.pi) + math.log(series)


def normal_survival(x: float) -> float:
    log_value = normal_log_survival(x)
    return math.exp(log_value) if log_value > math.log(np.finfo(float).tiny) else 0.0


def fmt_float(x: Any) -> Any:
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


def write_csv(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: fmt_float(row.get(k, "")) for k in fields})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def least_favourable_metrics(delta: float, q: float, margin: float = LOG_MARGIN) -> dict[str, float]:
    d = abs(delta) / q if q > 0 else math.inf
    minimax_error = normal_cdf(-0.5 * d) if math.isfinite(d) else 0.0
    if d == 0.0:
        p_margin = 0.0
    elif math.isinf(d):
        p_margin = 1.0
        log10_p_margin = 0.0
    else:
        standardized_threshold = margin / d - 0.5 * d
        log_p_margin = normal_log_survival(standardized_threshold)
        p_margin = normal_survival(standardized_threshold)
        log10_p_margin = log_p_margin / math.log(10.0)
    if d == 0.0:
        log10_p_margin = -math.inf
    return {
        "mahalanobis_distance": d,
        "minimax_midpoint_error": minimax_error,
        "probability_score_exceeds_ln10_under_target": p_margin,
        "log10_probability_score_exceeds_ln10_under_target": log10_p_margin,
    }


def affine_distance_squared(delta: np.ndarray, covariance: np.ndarray, nuisance: np.ndarray) -> float:
    """Mahalanobis distance to an affine nuisance column space."""
    delta = np.asarray(delta, dtype=float).reshape(-1)
    covariance = np.asarray(covariance, dtype=float)
    nuisance = np.asarray(nuisance, dtype=float)
    if nuisance.ndim == 1:
        nuisance = nuisance.reshape(delta.size, -1)
    if nuisance.size == 0:
        nuisance = np.zeros((delta.size, 0), dtype=float)
    ki = np.linalg.inv(covariance)
    if nuisance.shape[1] == 0:
        projection = ki
    else:
        gram = nuisance.T @ ki @ nuisance
        projection = ki - ki @ nuisance @ np.linalg.pinv(gram) @ nuisance.T @ ki
    value = float(delta @ projection @ delta)
    return max(0.0, value)


def affine_direct_distance_squared(delta: np.ndarray, covariance: np.ndarray, nuisance: np.ndarray) -> float:
    delta = np.asarray(delta, dtype=float).reshape(-1)
    nuisance = np.asarray(nuisance, dtype=float)
    if nuisance.ndim == 1:
        nuisance = nuisance.reshape(delta.size, -1)
    if nuisance.size == 0:
        nuisance = np.zeros((delta.size, 0), dtype=float)
    ki = np.linalg.inv(np.asarray(covariance, dtype=float))
    if nuisance.shape[1] == 0:
        residual = delta
    else:
        gamma = -np.linalg.pinv(nuisance.T @ ki @ nuisance) @ nuisance.T @ ki @ delta
        residual = delta + nuisance @ gamma
    return max(0.0, float(residual @ ki @ residual))


def two_channel_information(
    p_first: np.ndarray | float,
    q: tuple[float, float],
    b: tuple[float, float],
    sigma: tuple[float, float],
    resource: float,
) -> np.ndarray:
    p = np.asarray(p_first, dtype=float)
    a1 = resource * p / sigma[0] ** 2
    a2 = resource * (1.0 - p) / sigma[1] ** 2
    determinant = q[0] * b[1] - q[1] * b[0]
    denominator = a1 * b[0] ** 2 + a2 * b[1] ** 2
    numerator = a1 * a2 * determinant**2
    return np.divide(numerator, denominator, out=np.zeros_like(p), where=denominator > 0)


def optimal_two_channel_design(
    q: tuple[float, float],
    b: tuple[float, float],
    sigma: tuple[float, float],
    resource: float,
) -> tuple[float, float]:
    determinant = q[0] * b[1] - q[1] * b[0]
    denominator = abs(b[0]) / sigma[0] + abs(b[1]) / sigma[1]
    if denominator == 0.0:
        scores = (abs(q[0]) / sigma[0], abs(q[1]) / sigma[1])
        p = 1.0 if scores[0] >= scores[1] else 0.0
        imax = resource * max(scores) ** 2
        return p, imax
    p = (abs(b[1]) / sigma[1]) / denominator
    imax = resource * determinant**2 / (abs(b[0]) * sigma[1] + abs(b[1]) * sigma[0]) ** 2
    return p, imax


def common_nuisance_information(q: np.ndarray, b: np.ndarray, variance: np.ndarray) -> tuple[float, float, float]:
    """Return common-nuisance information, detector-specific information, and best common coefficient."""
    q = np.asarray(q, dtype=float)
    b = np.asarray(b, dtype=float)
    w = 1.0 / np.asarray(variance, dtype=float)
    denom = float(np.sum(w * b * b))
    a_hat = float(np.sum(w * b * q) / denom) if denom > 0 else 0.0
    common = float(np.sum(w * (q - b * a_hat) ** 2))
    individual = np.divide(q, b, out=np.zeros_like(q), where=b != 0)
    specific_residual = np.where(b != 0, q - b * individual, q)
    specific = float(np.sum(w * specific_residual**2))
    return common, specific, a_hat


def make_tables(outdir: Path) -> dict[str, list[dict[str, Any]]]:
    tables: dict[str, list[dict[str, Any]]] = {}

    closure_rows: list[dict[str, Any]] = []
    for exponent in range(0, 10):
        radius = DELTA_LOG * 10.0 ** (-exponent)
        metrics = least_favourable_metrics(radius, Q_STRICT)
        closure_rows.append(
            {
                "sequence_index": exponent,
                "alternative_log_radius": radius,
                "radius_over_old_gap": radius / DELTA_LOG,
                "lower_tau": TAU_TARGET * math.exp(-radius),
                "q_eff_reference": Q_STRICT,
                **metrics,
                "uniform_infimum_distance": 0.0,
                "uniform_minimax_max_error": 0.5,
                "interpretation": "pointwise alternatives approach target; unrestricted continuous family has zero uniform distance",
            }
        )
    tables["continuous_closure"] = closure_rows

    exclusion_specs = [
        ("quarter_old_gap", DELTA_LOG / 4.0),
        ("half_old_gap", DELTA_LOG / 2.0),
        ("full_old_gap", DELTA_LOG),
        ("one_percent_log_radius", 0.01),
    ]
    exclusion_rows: list[dict[str, Any]] = []
    for label, radius in exclusion_specs:
        exclusion_rows.append(
            {
                "exclusion_definition": label,
                "log_exclusion_radius": radius,
                "log_exclusion_radius_percent": 100.0 * radius,
                "lower_tau_boundary": TAU_TARGET * math.exp(-radius),
                "upper_tau_boundary": TAU_TARGET * math.exp(radius),
                "endpoint_competitors": TWO_SIDED_ENDPOINTS,
                "miss_probability_per_endpoint": TWO_SIDED_MISS_PER_ENDPOINT,
                "strict_distance_required_each_endpoint": D_TWO_SIDED,
                "max_q_eff": radius / D_TWO_SIDED,
                "max_q_eff_percent": 100.0 * radius / D_TWO_SIDED,
                "criterion": "both lower and upper endpoint scores exceed ln(10) with joint probability at least 0.90 by Bonferroni control",
            }
        )
    tables["exclusion_precision"] = exclusion_rows

    multiplicity_rows: list[dict[str, Any]] = []
    for competitors in [1, 2, 3, 5, 10, 20]:
        miss_allocation = (1.0 - TARGET_PROBABILITY) / competitors
        z = NormalDist().inv_cdf(1.0 - miss_allocation)
        distance = z + math.sqrt(z * z + 2.0 * LOG_MARGIN)
        multiplicity_rows.append(
            {
                "n_competitors": competitors,
                "bonferroni_miss_probability_per_competitor": miss_allocation,
                "normal_quantile": z,
                "required_pairwise_distance": distance,
                "max_q_eff_at_old_gap": DELTA_LOG / distance,
                "max_q_eff_at_old_gap_percent": 100.0 * DELTA_LOG / distance,
                "qualification": "conservative intersection rule; endpoint score is not a composite Bayes factor",
            }
        )
    tables["multiplicity"] = multiplicity_rows

    lane_specs = [
        ("v71_synthetic_carrier_at_optimistic_directwave_snr", 0.1046289428600577),
        ("NRSur7dq4_exact_product_anchor_only_optimistic", 0.011925803223219933),
        ("v71_expected_logLR_ln10_width", 0.0020295930013866014),
        ("v71_correct_sign_90pct_width", 0.0016992830196104567),
        ("v71_strict_ln10_90pct_width", Q_STRICT),
    ]
    lane_rows: list[dict[str, Any]] = []
    for label, q in lane_specs:
        metrics = least_favourable_metrics(DELTA_LOG, q)
        lane_rows.append(
            {
                "lane": label,
                "q_eff": q,
                "q_eff_percent": 100.0 * q,
                **metrics,
                "strict_gate_pass": metrics["mahalanobis_distance"] >= D_STRICT - 1e-12,
                "qualification": "Gaussian geometry benchmark only; not an event likelihood or evidence result",
            }
        )
    tables["least_favourable_lanes"] = lane_rows

    bias_rows: list[dict[str, Any]] = []
    for fraction in [0.0, 0.1, 0.25, 0.4, 0.49, 0.5, 0.6]:
        half_width = fraction * DELTA_LOG
        remaining = max(0.0, DELTA_LOG - 2.0 * half_width)
        bias_rows.append(
            {
                "symmetric_bias_halfwidth_over_gap": fraction,
                "symmetric_bias_halfwidth": half_width,
                "symmetric_bias_halfwidth_percent": 100.0 * half_width,
                "remaining_log_separation": remaining,
                "max_q_eff_for_strict_gate": remaining / D_STRICT,
                "max_q_eff_for_strict_gate_percent": 100.0 * remaining / D_STRICT,
                "nuisance_images_overlap_or_touch": remaining == 0.0,
                "formula": "d_U=(abs(Delta)-2U)_+/q_eff",
            }
        )
    tables["bias_frontier"] = bias_rows

    affine_cases = [
        (
            "scalar_old_branch_at_strict_width",
            np.array([DELTA_LOG]),
            np.array([[Q_STRICT**2]]),
            np.zeros((1, 0)),
            "point-versus-point recovery",
        ),
        (
            "exact_shared_nuisance_alias",
            np.array([1.0, 1.0]),
            np.eye(2),
            np.array([[1.0], [1.0]]),
            "branch displacement lies in nuisance column space",
        ),
        (
            "orthogonal_completion_residual",
            np.array([1.0, 1.0]),
            np.eye(2),
            np.array([[1.0], [0.0]]),
            "one component survives nuisance quotient",
        ),
        (
            "branch_specific_combined_alias",
            np.array([1.0, -1.0]),
            np.eye(2),
            np.eye(2),
            "combined branch-specific nuisance columns span displacement",
        ),
        (
            "correlated_covariance_partial_completion",
            np.array([1.0, 0.5]),
            np.array([[1.0, 0.2], [0.2, 2.0]]),
            np.array([[1.0], [0.0]]),
            "correlated fixed covariance example",
        ),
    ]
    affine_rows: list[dict[str, Any]] = []
    for label, delta, cov, nuisance, note in affine_cases:
        d2 = affine_distance_squared(delta, cov, nuisance)
        direct = affine_direct_distance_squared(delta, cov, nuisance)
        affine_rows.append(
            {
                "case": label,
                "dimension": delta.size,
                "nuisance_rank": int(np.linalg.matrix_rank(nuisance)) if nuisance.size else 0,
                "distance_squared_projection_formula": d2,
                "distance_squared_direct_gls": direct,
                "absolute_difference": abs(d2 - direct),
                "distance": math.sqrt(d2),
                "exact_alias_numerically": d2 < 1e-12,
                "qualification": note,
            }
        )
    tables["affine_examples"] = affine_rows

    resource = 100.0
    design_specs = [
        (
            "same_tau_response_common_free_timescale",
            (1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
            "rank fail: common free log-timescale is identical to the tau tangent",
        ),
        (
            "nonproportional_tau_responses_q1_1_q2_0p5",
            (1.0, 0.5),
            (1.0, 1.0),
            (1.0, 1.0),
            "illustrative g_i=t*F_i(tau) lane; no physical F_i supplied",
        ),
        (
            "nonproportional_tau_responses_q1_1_q2_2",
            (1.0, 2.0),
            (1.0, 1.0),
            (1.0, 1.0),
            "illustrative g_i=t*F_i(tau) lane; no physical F_i supplied",
        ),
        (
            "nonproportional_tau_responses_unequal_noise",
            (1.0, 0.5),
            (1.0, 1.0),
            (1.0, 2.0),
            "illustrates noise-weighted resource allocation",
        ),
        (
            "nuisance_free_second_anchor",
            (1.0, 1.0),
            (0.5, 0.0),
            (1.0, 1.0),
            "open-allocation supremum as channel-1 resource tends to zero from above; the n_i>0 theorem has no attained boundary maximum",
        ),
    ]
    design_rows: list[dict[str, Any]] = []
    for label, q, b, sigma, note in design_specs:
        determinant = q[0] * b[1] - q[1] * b[0]
        p, imax = optimal_two_channel_design(q, b, sigma, resource)
        design_rows.append(
            {
                "design": label,
                "q1": q[0],
                "q2": q[1],
                "b1": b[0],
                "b2": b[1],
                "sigma1": sigma[0],
                "sigma2": sigma[1],
                "resource": resource,
                "completion_determinant": determinant,
                "rank_complete": abs(determinant) > 1e-14,
                "optimal_fraction_channel1": p,
                "optimal_fraction_channel2": 1.0 - p,
                "allocation_status": (
                    "NONUNIQUE_RANK_FAIL"
                    if abs(determinant) <= 1e-14
                    else "OPEN_DOMAIN_SUPREMUM_NOT_ATTAINED"
                    if p in (0.0, 1.0)
                    else "INTERIOR_MAXIMUM"
                ),
                "maximum_efficient_information": imax,
                "minimum_q_eff_if_information_positive": 1.0 / math.sqrt(imax) if imax > 0 else math.inf,
                "qualification": note,
            }
        )
    tables["two_observable_design"] = design_rows

    detector_specs = [
        (
            "same_alias_coefficient_replication",
            np.array([2.0, 4.0]),
            np.array([1.0, 2.0]),
            np.array([1.0, 1.0]),
            "same coefficient a=2 works in both detectors; replication cannot complete",
        ),
        (
            "conflicting_alias_coefficients_shared_nuisance",
            np.array([1.0, 2.0]),
            np.array([1.0, 1.0]),
            np.array([1.0, 1.0]),
            "each detector aliases alone, but no common coefficient fits both",
        ),
        (
            "conflicting_aliases_unequal_variance",
            np.array([1.0, 2.0]),
            np.array([1.0, 1.0]),
            np.array([1.0, 4.0]),
            "same conflict with weaker second detector",
        ),
        (
            "single_delay_common_scale_alias",
            np.array([1.0, 3.0, 0.5]),
            np.array([1.0, 3.0, 0.5]),
            np.array([1.0, 1.0, 1.0]),
            "abstracted v69 tangent geometry: common coefficient preserves the local linear alias; the separate v69 finite gauge supplies exact global nonidentifiability",
        ),
    ]
    detector_rows: list[dict[str, Any]] = []
    for label, q, b, variance, note in detector_specs:
        common, specific, a_hat = common_nuisance_information(q, b, variance)
        coefficients = np.divide(q, b, out=np.full_like(q, np.nan), where=b != 0)
        detector_rows.append(
            {
                "case": label,
                "n_detectors": q.size,
                "individual_alias_coefficients": ";".join(f"{x:.12g}" for x in coefficients),
                "best_common_alias_coefficient": a_hat,
                "common_nuisance_efficient_information": common,
                "detector_specific_nuisance_information": specific,
                "common_information_ge_specific": common + 1e-14 >= specific,
                "common_alias_survives": common < 1e-12,
                "qualification": note,
            }
        )
    tables["detector_alias"] = detector_rows

    filenames = {
        "continuous_closure": "GW250114_V72_continuous_alternative_closure_sequence.csv",
        "exclusion_precision": "GW250114_V72_exclusion_radius_precision_budget.csv",
        "multiplicity": "GW250114_V72_finite_composite_multiplicity_budget.csv",
        "least_favourable_lanes": "GW250114_V72_least_favourable_lane_power.csv",
        "bias_frontier": "GW250114_V72_bias_precision_frontier.csv",
        "affine_examples": "GW250114_V72_affine_nuisance_distance_examples.csv",
        "two_observable_design": "GW250114_V72_two_observable_optimal_design.csv",
        "detector_alias": "GW250114_V72_detector_alias_consistency.csv",
    }
    for key, filename in filenames.items():
        write_csv(outdir / filename, tables[key])
    return tables


def make_figures(outdir: Path, tables: dict[str, list[dict[str, Any]]]) -> None:
    metadata = {"Software": "GW250114 HRF v72 deterministic theorem generator"}

    closure = tables["continuous_closure"]
    x = np.array([r["radius_over_old_gap"] for r in closure])
    error = np.array([r["minimax_midpoint_error"] for r in closure])
    p10 = np.array([r["probability_score_exceeds_ln10_under_target"] for r in closure])
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.semilogx(x, error, "o-", label="minimax midpoint error")
    ax.semilogx(x, p10, "s-", label=r"$P(L>\ln 10)$")
    ax.axhline(0.5, color="black", linewidth=1.0, linestyle="--", label="uniform closure limit 1/2")
    ax.set_xlabel(r"alternative log-radius / historical branch gap")
    ax.set_ylabel("probability")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title("Continuous alternatives approach the target")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(outdir / "GW250114_V72_continuous_closure.png", dpi=180, metadata=metadata)
    plt.close(fig)

    exclusion = tables["exclusion_precision"]
    labels = [r["exclusion_definition"].replace("_", "\n") for r in exclusion]
    qmax = [r["max_q_eff_percent"] for r in exclusion]
    fig, ax = plt.subplots(figsize=(7.4, 4.7))
    bars = ax.bar(labels, qmax, color=["#4C78A8", "#72B7B2", "#F58518", "#E45756"])
    for bar, value in zip(bars, qmax):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.4f}%", ha="center", va="bottom", fontsize=8)
    ax.set_ylabel(r"maximum $q_{\rm eff}$ (%)")
    ax.set_title(r"Precision required by the preregistered exclusion radius")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(outdir / "GW250114_V72_exclusion_precision_budget.png", dpi=180, metadata=metadata)
    plt.close(fig)

    multiplicity = tables["multiplicity"]
    k = np.array([r["n_competitors"] for r in multiplicity])
    q = np.array([r["max_q_eff_at_old_gap_percent"] for r in multiplicity])
    distance = np.array([r["required_pairwise_distance"] for r in multiplicity])
    fig, ax1 = plt.subplots(figsize=(7.2, 4.7))
    ax1.plot(k, q, "o-", color="#4C78A8")
    ax1.set_xlabel("number of preregistered competitors")
    ax1.set_ylabel(r"maximum $q_{\rm eff}$ at old gap (%)", color="#4C78A8")
    ax1.tick_params(axis="y", labelcolor="#4C78A8")
    ax1.grid(True, alpha=0.25)
    ax2 = ax1.twinx()
    ax2.plot(k, distance, "s--", color="#E45756")
    ax2.set_ylabel("required pairwise distance", color="#E45756")
    ax2.tick_params(axis="y", labelcolor="#E45756")
    ax1.set_title("Conservative finite-composite precision budget")
    fig.tight_layout()
    fig.savefig(outdir / "GW250114_V72_multiplicity_precision_budget.png", dpi=180, metadata=metadata)
    plt.close(fig)

    p = np.linspace(0.0, 1.0, 1001)
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    curves = [
        ("same tau response (rank fail)", (1.0, 1.0), (1.0, 1.0), (1.0, 1.0)),
        (r"different tau response, $q_2=0.5$", (1.0, 0.5), (1.0, 1.0), (1.0, 1.0)),
        (r"different tau response, $q_2=2$", (1.0, 2.0), (1.0, 1.0), (1.0, 1.0)),
        ("different tau response, unequal noise", (1.0, 0.5), (1.0, 1.0), (1.0, 2.0)),
    ]
    for label, qv, bv, sv in curves:
        info = two_channel_information(p, qv, bv, sv, 1.0)
        ax.plot(p, info, label=label)
        pstar, imax = optimal_two_channel_design(qv, bv, sv, 1.0)
        ax.scatter([pstar], [imax], s=26)
    ax.set_xlabel("resource fraction assigned to channel 1")
    ax.set_ylabel(r"efficient information per resource unit")
    ax.set_title("Different tau response under one free timescale completes the rank")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "GW250114_V72_two_observable_design.png", dpi=180, metadata=metadata)
    plt.close(fig)


def run_self_tests(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    tests: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        tests.append({"name": name, "passed": bool(passed), "detail": detail})

    strict_metrics = least_favourable_metrics(DELTA_LOG, Q_STRICT)
    check("strict_distance_recovery", abs(strict_metrics["mahalanobis_distance"] - D_STRICT) < 1e-12, f"D={strict_metrics['mahalanobis_distance']:.16g}")
    check("strict_probability_recovery", abs(strict_metrics["probability_score_exceeds_ln10_under_target"] - 0.9) < 1e-12, f"p={strict_metrics['probability_score_exceeds_ln10_under_target']:.16g}")
    check("unrestricted_continuum_infimum_zero", all(r["uniform_infimum_distance"] == 0.0 for r in tables["continuous_closure"]), "analytic closure theorem encoded")
    check("closure_error_approaches_half", abs(tables["continuous_closure"][-1]["minimax_midpoint_error"] - 0.5) < 1e-8, f"last_error={tables['continuous_closure'][-1]['minimax_midpoint_error']:.16g}")
    expected_two_sided_q = DELTA_LOG / D_TWO_SIDED
    check("two_sided_full_gap_q_recovery", abs(tables["exclusion_precision"][2]["max_q_eff"] - expected_two_sided_q) < 1e-15, "two endpoint lanes reproduce the K=2 multiplicity width")
    check("two_sided_joint_success_recovery", abs(1.0 - 2.0 * TWO_SIDED_MISS_PER_ENDPOINT - TARGET_PROBABILITY) < 1e-15, "Bonferroni lower bound equals 0.90")
    check("stable_extreme_tail_log_probability", tables["least_favourable_lanes"][0]["log10_probability_score_exceeds_ln10_under_target"] < -600.0, "extreme carrier-lane tail retained in log10 form")
    check("bias_half_gap_closes_images", any(abs(r["symmetric_bias_halfwidth_over_gap"] - 0.5) < 1e-15 and r["nuisance_images_overlap_or_touch"] for r in tables["bias_frontier"]), "U=Delta/2")

    rng = np.random.default_rng(720071)
    maximum_projection_error = 0.0
    maximum_reparameterization_error = 0.0
    for _ in range(64):
        m, rank = 7, 3
        a = rng.normal(size=(m, m))
        covariance = a @ a.T + 0.5 * np.eye(m)
        nuisance = rng.normal(size=(m, rank))
        delta = rng.normal(size=m)
        projected = affine_distance_squared(delta, covariance, nuisance)
        direct = affine_direct_distance_squared(delta, covariance, nuisance)
        maximum_projection_error = max(maximum_projection_error, abs(projected - direct))
        transform = rng.normal(size=(rank, rank))
        while abs(np.linalg.det(transform)) < 0.05:
            transform = rng.normal(size=(rank, rank))
        transformed = affine_distance_squared(delta, covariance, nuisance @ transform)
        maximum_reparameterization_error = max(maximum_reparameterization_error, abs(projected - transformed))
    check("affine_projection_matches_direct_gls", maximum_projection_error < 1e-10, f"max_abs={maximum_projection_error:.3e}")
    check("nuisance_reparameterization_invariance", maximum_reparameterization_error < 1e-10, f"max_abs={maximum_reparameterization_error:.3e}")
    check("affine_exact_alias_zero", tables["affine_examples"][1]["distance_squared_projection_formula"] < 1e-12, f"d2={tables['affine_examples'][1]['distance_squared_projection_formula']:.3e}")

    maximum_design_grid_error = 0.0
    for _ in range(32):
        q = tuple(rng.normal(size=2))
        b = tuple(rng.normal(size=2))
        sigma = tuple(np.exp(rng.normal(size=2)))
        pstar, imax = optimal_two_channel_design(q, b, sigma, 100.0)
        igrid = float(np.max(two_channel_information(np.linspace(0.0, 1.0, 20001), q, b, sigma, 100.0)))
        maximum_design_grid_error = max(maximum_design_grid_error, abs(imax - igrid) / max(1.0, abs(imax)))
        if not 0.0 <= pstar <= 1.0:
            maximum_design_grid_error = math.inf
    check("two_channel_optimum_matches_dense_grid", maximum_design_grid_error < 1e-7, f"max_relative={maximum_design_grid_error:.3e}")
    check("identical_slopes_rank_fail", not tables["two_observable_design"][0]["rank_complete"] and tables["two_observable_design"][0]["maximum_efficient_information"] == 0.0, "determinant=0")
    check("distinct_slopes_rank_complete", tables["two_observable_design"][1]["rank_complete"] and tables["two_observable_design"][1]["maximum_efficient_information"] > 0.0, "determinant nonzero")
    check("detector_common_information_ge_specific", all(r["common_information_ge_specific"] for r in tables["detector_alias"]), "least squares with one common coefficient is no less restrictive")
    check("same_detector_alias_survives", tables["detector_alias"][0]["common_alias_survives"], "same coefficient fits both")
    check("conflicting_detector_alias_breaks_common_nuisance", not tables["detector_alias"][1]["common_alias_survives"] and tables["detector_alias"][1]["detector_specific_nuisance_information"] < 1e-12, "individual aliases conflict only under shared nuisance")

    passed = sum(int(t["passed"]) for t in tests)
    return {
        "version": VERSION,
        "date": DATE,
        "status": "PASS" if passed == len(tests) else "FAIL",
        "n_passed": passed,
        "n_tests": len(tests),
        "tests": tests,
    }


def make_summary(tables: dict[str, list[dict[str, Any]]], self_test: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": VERSION,
        "date": DATE,
        "scope": "methods-only deterministic theorem and numerical feasibility package; no strain analysis",
        "claim_boundary": "No HRF detection, no ln(4)/g=4 identification, no area quantization, and no quantum-horizon claim.",
        "historical_branch_geometry": {
            "tau_target_ln4": TAU_TARGET,
            "tau_old_competitor": TAU_OLD_COMPETITOR,
            "delta_log_tau": DELTA_LOG,
        },
        "strict_least_favourable_gate": {
            "scope": "one preregistered named competitor",
            "score_margin": LOG_MARGIN,
            "target_probability": TARGET_PROBABILITY,
            "required_distance": D_STRICT,
            "max_q_eff_at_old_gap": Q_STRICT,
            "max_q_eff_at_old_gap_percent": 100.0 * Q_STRICT,
        },
        "continuous_alternative": {
            "unrestricted_punctured_continuum_uniform_distance": 0.0,
            "uniform_minimax_max_error": 0.5,
            "status": "EXACT_FAIL_BY_CLOSURE_WITHOUT_EXCLUSION_RADIUS",
            "required_repair": "preregistered exclusion radius with an indifference gap, an interval/equivalence procedure with its own coverage or type-I semantics, or a normalized-prior Bayes model with sensitivity analysis",
        },
        "two_sided_exclusion_gate_at_historical_gap": {
            "endpoint_competitors": TWO_SIDED_ENDPOINTS,
            "joint_target_probability_lower_bound": TARGET_PROBABILITY,
            "required_distance_each_endpoint": D_TWO_SIDED,
            "max_q_eff_at_old_gap": DELTA_LOG / D_TWO_SIDED,
            "max_q_eff_at_old_gap_percent": 100.0 * DELTA_LOG / D_TWO_SIDED,
        },
        "affine_nuisance_formula": "d^2=delta^T[K^-1-K^-1C(C^TK^-1C)^+C^TK^-1]delta",
        "two_observable_completion_rule": "q1*b2-q2*b1 != 0 for one shared local nuisance",
        "detector_rule": "individually locally aliased detectors have positive shared-nuisance tangent information only if no common linear nuisance coefficient fits every detector; global identification requires a separate nuisance-image check",
        "generated_table_counts": {key: len(rows) for key, rows in tables.items()},
        "self_test": {"status": self_test["status"], "n_passed": self_test["n_passed"], "n_tests": self_test["n_tests"]},
        "gate_status": {
            "unrestricted_continuous_tau_uniform_separation": "EXACT_FAIL_BY_CLOSURE",
            "finite_composite_least_favourable_framework": "PASS_METHOD_ONLY",
            "global_nuisance_distances_from_real_joint_likelihood": "NOT_MEASURED",
            "two_observable_experimental_design": "THEOREM_ONLY_NO_SECOND_PHYSICAL_OBSERVABLE",
            "raw_detector_factorization": "NOT_EXECUTED",
            "physical_interpretation": "LOCKED",
        },
        "verdict": "COMPOSITE_GATE_REQUIRES_RESOLUTION_AND_REAL_JOINT_NUISANCE_IMAGES",
    }


MATH_OUTPUT_FILES = (
    "GW250114_V72_affine_nuisance_distance_examples.csv",
    "GW250114_V72_bias_precision_frontier.csv",
    "GW250114_V72_continuous_alternative_closure_sequence.csv",
    "GW250114_V72_continuous_closure.png",
    "GW250114_V72_detector_alias_consistency.csv",
    "GW250114_V72_exclusion_precision_budget.png",
    "GW250114_V72_exclusion_radius_precision_budget.csv",
    "GW250114_V72_finite_composite_multiplicity_budget.csv",
    "GW250114_V72_least_favourable_lane_power.csv",
    "GW250114_V72_math_self_test.json",
    "GW250114_V72_math_summary.json",
    "GW250114_V72_multiplicity_precision_budget.png",
    "GW250114_V72_two_observable_design.png",
    "GW250114_V72_two_observable_optimal_design.csv",
)


def make_manifest(outdir: Path, generator: Path) -> None:
    files = [outdir / name for name in MATH_OUTPUT_FILES]
    missing = [p.name for p in files if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"missing generated math outputs: {missing}")
    payload = {
        "version": VERSION,
        "date": DATE,
        "generator": {"name": generator.name, "sha256": sha256(generator)},
        "files": [{"name": p.name, "bytes": p.stat().st_size, "sha256": sha256(p)} for p in files],
    }
    write_json(outdir / "GW250114_V72_math_manifest.json", payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--strict", action="store_true", help="exit nonzero if a numerical self-test fails")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    outdir = args.outdir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    tables = make_tables(outdir)
    make_figures(outdir, tables)
    self_test = run_self_tests(tables)
    write_json(outdir / "GW250114_V72_math_self_test.json", self_test)
    summary = make_summary(tables, self_test)
    write_json(outdir / "GW250114_V72_math_summary.json", summary)
    make_manifest(outdir, Path(__file__).resolve())
    print(json.dumps({"version": VERSION, "outdir": str(outdir), "self_test": self_test["status"], "tests": f"{self_test['n_passed']}/{self_test['n_tests']}", "verdict": summary["verdict"]}, sort_keys=True))
    return 0 if (not args.strict or self_test["status"] == "PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
