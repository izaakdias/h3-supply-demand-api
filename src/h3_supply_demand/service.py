"""Explainable synthetic supply-demand scoring."""

from __future__ import annotations

import hashlib

import h3

from .schemas import SupplyDemandResponse


def _stable_number(cell: str, low: int, high: int) -> int:
    digest = hashlib.sha256(cell.encode("utf-8")).digest()
    return low + int.from_bytes(digest[:4], "big") % (high - low + 1)


def classify(score: float) -> str:
    if score >= 0.85:
        return "critical"
    if score >= 0.65:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def build_snapshot(latitude: float, longitude: float, resolution: int) -> SupplyDemandResponse:
    cell = h3.latlng_to_cell(latitude, longitude, resolution)
    open_requests = _stable_number(cell + ":requests", 4, 42)
    active_drivers = _stable_number(cell + ":drivers", 6, 36)
    eta = round(3.0 + _stable_number(cell + ":eta", 0, 120) / 20, 1)
    request_pressure = min(open_requests / 35, 1.0)
    supply_pressure = 1 - min(active_drivers / 40, 1.0)
    eta_pressure = min(max(eta - 4, 0) / 10, 1.0)
    score = round(min(1.0, 0.5 * request_pressure + 0.3 * supply_pressure + 0.2 * eta_pressure), 3)
    level = classify(score)
    recommendation = {
        "critical": "Prioritize driver dispatch and consider surge protection.",
        "high": "Increase driver incentives and monitor pickup ETA.",
        "medium": "Maintain normal operations and observe demand trend.",
        "low": "Keep the zone available for standard dispatching.",
    }[level]
    return SupplyDemandResponse(
        h3_index=cell,
        resolution=resolution,
        demand_score=score,
        demand_level=level,
        open_requests=open_requests,
        active_drivers=active_drivers,
        avg_pickup_eta_minutes=eta,
        recommendation=recommendation,
    )
