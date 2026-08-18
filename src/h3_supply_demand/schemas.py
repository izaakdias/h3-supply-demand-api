"""API contracts."""

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    resolution: int = Field(default=8, ge=0, le=15)


class SupplyDemandResponse(BaseModel):
    h3_index: str
    resolution: int
    demand_score: float
    demand_level: str
    open_requests: int
    active_drivers: int
    avg_pickup_eta_minutes: float
    recommendation: str
