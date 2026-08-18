# H3 Supply & Demand API

A production-shaped geospatial API that turns a latitude/longitude into an H3 service cell and returns an explainable supply-demand snapshot.

This is an independent portfolio project using deterministic synthetic signals. It contains no Leaf.app source code, internal logic, or customer data.

## What it demonstrates

- Geospatial feature bucketing with H3
- Typed request and response contracts with Pydantic
- FastAPI service design with OpenAPI documentation
- Explainable demand and supply scoring
- Health checks, Docker packaging, tests, and CI

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
uvicorn h3_supply_demand.api:app --reload
```

Open the interactive API docs at `http://127.0.0.1:8000/docs`.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/v1/supply-demand/predict \
  -H 'content-type: application/json' \
  -d '{"latitude": -22.9068, "longitude": -43.1729, "resolution": 8}'
```

## Design

The service converts coordinates into an H3 cell, derives a deterministic synthetic operational snapshot, and computes:

- open request pressure;
- driver supply ratio;
- pickup ETA pressure;
- an explainable demand score and demand level;
- a recommended operational action.

The synthetic generator makes the API reproducible while keeping the repository safe to publish. A production integration would replace the generator with an approved feature store or read model.

## Testing

```bash
pytest
```

## Next iterations

1. Add Redis-backed snapshots with TTLs.
2. Add neighborhood queries using H3 grid disks.
3. Add authentication, rate limiting, and request tracing.
4. Connect the endpoint to a versioned forecasting model.
