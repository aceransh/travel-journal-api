# Travel Journal API (FastAPI + SQLite)

A simple REST API for recording and querying travel records with filtering, pagination, and basic aggregation. Built with FastAPI, Pydantic, SQLAlchemy, and SQLite.

Repo is ready to run locally and includes a seed script for demo data.

## Quickstart

Prereqs: Python 3.11+ recommended

- Create and activate a virtual environment
  - macOS/Linux:
    - python -m venv .venv
    - source .venv/bin/activate
  - Windows (PowerShell):
    - python -m venv .venv
    - .\.venv\Scripts\Activate.ps1

- Install dependencies
  - pip install -r requirements.txt

- Run the API
  - uvicorn main:app --reload
  - API runs at http://127.0.0.1:8000

- Seed 20 example trips (optional; macOS/Linux)
  - chmod +x ./seed.sh
  - ./seed.sh

- Interactive Docs
  - Swagger UI: http://127.0.0.1:8000/docs
  - ReDoc: http://127.0.0.1:8000/redoc

## Health

- GET /health → {"Status":"Ok"}

## Data Model

Trip
- id: integer
- locationName: string
- city: string
- country: string
- visitDate: date (YYYY-MM-DD)
- rating: integer (1–5 expected)
- notes: string | null

Example
```
{
  "id": 1,
  "locationName": "Eiffel Tower",
  "city": "Paris",
  "country": "France",
  "visitDate": "2024-06-01",
  "rating": 5,
  "notes": "Iconic landmark"
}
```

## Endpoints

Base: http://127.0.0.1:8000

- GET / → "Hello World"
- GET /health → health check
- POST /trips → create
- GET /trips → list with rich filtering + pagination
- GET /trips/{trip_id} → read one
- PUT /trips/{trip_id} → full update
- DELETE /trips/{trip_id} → delete
- GET /trips/stats/avg-rating-by-country → aggregation

### Create a trip
POST /trips
- Body:
```
{
  "locationName": "Louvre Museum",
  "city": "Paris",
  "country": "France",
  "visitDate": "2024-06-02",
  "rating": 4,
  "notes": "Mona Lisa"
}
```
- cURL:
```
curl -X POST http://127.0.0.1:8000/trips \
  -H "Content-Type: application/json" \
  -d '{"locationName":"Louvre Museum","city":"Paris","country":"France","visitDate":"2024-06-02","rating":4,"notes":"Mona Lisa"}'
```

### List trips (filtering + pagination)
GET /trips
- Query params (all optional):
  - locationName (substring, case-insensitive)
  - city (substring, case-insensitive)
  - country (substring, case-insensitive)
  - visitDate (exact date)
  - visitDateFrom (inclusive)
  - visitDateTo (inclusive)
  - rating (exact)
  - minRating, maxRating
  - limit (default 20, 1–100)
  - offset (default 0)
- Headers:
  - X-Total-Count: total records matching filters
- cURL examples:
  - All trips (first page):
    - curl "http://127.0.0.1:8000/trips"
  - Paris trips rated >=4 in June 2024:
    - curl "http://127.0.0.1:8000/trips?city=paris&minRating=4&visitDateFrom=2024-06-01&visitDateTo=2024-06-30"
  - USA trips, paginated:
    - curl -i "http://127.0.0.1:8000/trips?country=usa&limit=5&offset=0"

### Get a trip
GET /trips/{trip_id}
- cURL:
  - curl "http://127.0.0.1:8000/trips/1"

### Update a trip (full replace)
PUT /trips/{trip_id}
- Body: same shape as create
- cURL:
```
curl -X PUT http://127.0.0.1:8000/trips/1 \
  -H "Content-Type: application/json" \
  -d '{"locationName":"Eiffel Tower","city":"Paris","country":"France","visitDate":"2024-06-01","rating":5,"notes":"Sunset view"}'
```

### Delete a trip
DELETE /trips/{trip_id}
- Returns 204 No Content on success
- cURL:
  - curl -X DELETE "http://127.0.0.1:8000/trips/1" -i

### Aggregation: average rating by country
GET /trips/stats/avg-rating-by-country
- Response:
```
[
  { "country": "Japan", "count": 4, "avgRating": 4.5 },
  { "country": "USA", "count": 7, "avgRating": 4.29 },
  ...
]
```
- cURL:
  - curl "http://127.0.0.1:8000/trips/stats/avg-rating-by-country"

## Error Handling

- 404 Not Found when a trip ID does not exist
  - { "detail": "Trip 999 not found" }
- 422 Unprocessable Entity for invalid payloads (FastAPI/Pydantic validation)

Notes
- Rating is expected to be 1–5. Query validators enforce ranges for filters; request model currently relies on caller discipline.

## Design Decisions

- Framework: FastAPI for speed, typing, auto-docs, and Pydantic validation.
- Data: SQLite via SQLAlchemy ORM for local, file-backed persistence (app.db).
- Models: Clear separation of Pydantic models (request/response) and SQLAlchemy models (DB).
- Filtering: Case-insensitive substring search using SQL LOWER + LIKE; exact/ range filters for date and rating.
- Pagination: limit/offset plus X-Total-Count header for client-side paging.
- Consistency: Conventional RESTful routes and JSON payloads.

Project Structure
- main.py: FastAPI app and routes
- models.py: Pydantic schemas and SQLAlchemy Trip table
- database.py: engine/session setup (SQLite)
- requirements.txt: pinned deps
- seed.sh: 20 sample trips via POST requests

## Demo Flow (15–20 min)

- Health check and docs (/docs)
- Create a trip (POST /trips)
- List with filters + pagination (GET /trips?city=...&minRating=...&visitDateFrom=...&limit=...&offset=...)
- Get one, update, delete (GET/PUT/DELETE /trips/{id})
- Aggregation (GET /trips/stats/avg-rating-by-country)
- Brief code walk-through: models.py → database.py → main.py query building

## Future Improvements

- Validation: enforce rating 1–5 at model level; stricter field constraints.
- Migrations: Alembic for schema evolution.
- Images: UploadFile support; store in S3/local with signed URLs.
- Auth: user accounts, per-user journals, rate limiting.
- More analytics: top destinations per month, streaks, most-visited cities.
- Performance: indexes on city/country/date; caching for aggregations.
- Config: environment variables for DB URL, ports, CORS.

## Notes

- DB path: SQLite file at ./app.db next to the codebase.
- Resetting data: stop server, delete app.db, restart, re-run seed.sh.

Happy traveling!
