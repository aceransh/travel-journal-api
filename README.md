# Travel Journal REST API

A production-ready REST API for logging and querying travel experiences. It supports full CRUD for trips, robust filtering and pagination, and a bonus aggregation endpoint for insights. Built for the App Team Carolina take-home to showcase thoughtful API design, clean architecture, and developer ergonomics.

## 🚀 Tech Stack

| Component      | Technology | Rationale |
| --- | --- | --- |
| Language | Python | Versatile, readable, large ecosystem |
| API Framework | FastAPI | High performance, automatic validation with Pydantic, interactive docs |
| Database ORM | SQLAlchemy | Powerful query builder, safe by default (prevents SQL injection) |
| Database | SQLite | Simple, file-based, zero setup required |
| Web Server | Uvicorn | Lightning-fast ASGI server optimized for FastAPI |

## ✨ Core Features

- Full CRUD functionality (Create, Read, Update, Delete) for travel records.
- Persistent data storage using a SQLite database.
- Advanced, database-level filtering on the GET /trips endpoint.
- Efficient pagination using limit and offset.
- Bonus aggregation endpoint to calculate average ratings by country.
- Automatic, interactive API documentation via FastAPI.

## 📚 API Endpoint Documentation

Base URL: http://127.0.0.1:8000

1) POST /trips — Create a new travel record
- Request body:
```json
{
  "locationName": "Louvre Museum",
  "city": "Paris",
  "country": "France",
  "visitDate": "2024-06-02",
  "rating": 4,
  "notes": "Mona Lisa"
}
```
- Success response (201):
```json
{
  "id": 1,
  "locationName": "Louvre Museum",
  "city": "Paris",
  "country": "France",
  "visitDate": "2024-06-02",
  "rating": 4,
  "notes": "Mona Lisa"
}
```

2) GET /trips — List trips with filtering and pagination
- Key query params: country, minRating, limit, offset
  - Example: /trips?country=USA&minRating=4&limit=10&offset=0
- Success response (200):
```json
[
  {
    "id": 10,
    "locationName": "Statue of Liberty",
    "city": "New York",
    "country": "USA",
    "visitDate": "2024-09-01",
    "rating": 5,
    "notes": "Gift from France"
  }
]
```

3) GET /trips/{trip_id} — Retrieve a single trip
- Success response (200):
```json
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

4) PUT /trips/{trip_id} — Update a trip (full replacement)
- Request body:
```json
{
  "locationName": "Eiffel Tower",
  "city": "Paris",
  "country": "France",
  "visitDate": "2024-06-01",
  "rating": 5,
  "notes": "Sunset view"
}
```
- Success response (200): same shape as GET /trips/{trip_id} with updated fields.

5) DELETE /trips/{trip_id} — Delete a trip
- Success response: 204 No Content (empty body)

6) GET /trips/stats/avg-rating-by-country — Aggregated insights
- Success response (200):
```json
[
  { "country": "Japan", "count": 4, "avgRating": 4.5 },
  { "country": "USA", "count": 7, "avgRating": 4.29 }
]
```

Notes:
- Validation errors return 422 with details.
- Nonexistent resources return 404 with a clear message.

## 🧠 My Thought Process & Design Choices

- FastAPI was chosen for speed of development, strong typing, performance, and built-in Swagger/ReDoc. Pydantic models ensure request/response consistency and validation with minimal boilerplate.
- The API follows REST principles:
  - Plural, resource-oriented paths (/trips).
  - Standard HTTP methods (GET, POST, PUT, DELETE).
  - Appropriate status codes (201 on create, 204 on delete, 404 on not found, 422 on validation errors).
- Data is persisted via SQLAlchemy ORM into SQLite for a portable, zero-config setup suitable for interviews and demos.

Challenge: Efficient Filtering
- Rather than filtering in Python post-fetch (which doesn’t scale), filtering is pushed down to the database via SQLAlchemy’s query builder (LOWER + LIKE for case-insensitive substring matches, range filters for dates/ratings). This keeps queries efficient and leverages DB indexing if migrated to a production database later.

## 📈 Future Improvements

1. User Authentication (JWT) to secure endpoints and enable per-user journals.
2. Image Uploads for attaching a photo per trip (local or S3, signed URLs).
3. Automated Testing with pytest and testcontainers/SQLite-in-memory for reliability.
4. Validation: enforce rating 1–5 at the model level; add stricter field constraints.
5. Database Migrations with Alembic for schema evolution.
6. More analytics: top destinations per month, streaks, most-visited cities.
7. Performance: indexes on city/country/date; caching for aggregations.
8. Configuration: environment variables for DB URL, ports, and CORS.

## 🛠️ How to Set Up and Run This Project

1) Clone the repository
```
git clone <YOUR_PUBLIC_REPO_URL> travel-journal-api
cd travel-journal-api
```

2) Create and activate a virtual environment
- macOS/Linux:
```
python -m venv .venv
source .venv/bin/activate
```
- Windows (PowerShell):
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Install dependencies
```
pip install -r requirements.txt
```

4) Run the server
```
uvicorn main:app --reload
```
- App runs at: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

Optional: Seed demo data on macOS/Linux
```
chmod +x ./seed.sh
./seed.sh
```

## 🧪 How to Demo & Test

- Use the interactive Swagger UI at: http://127.0.0.1:8000/docs
- Steps:
  - Expand POST /trips, click Try it out, and create a record.
  - Open GET /trips to list and filter using country, minRating, limit, offset.
  - Retrieve a single record via GET /trips/{trip_id}.
  - Update with PUT /trips/{trip_id} and delete with DELETE /trips/{trip_id}.
  - Show insights via GET /trips/stats/avg-rating-by-country.
- Create a trip (POST /trips)
- List with filters + pagination (GET /trips?city=...&minRating=...&visitDateFrom=...&limit=...&offset=...)
- Get one, update, delete (GET/PUT/DELETE /trips/{id})
- Aggregation (GET /trips/stats/avg-rating-by-country)
- Brief code walk-through: models.py → database.py → main.py query building

## Notes

- DB path: SQLite file at ./app.db next to the codebase.
- Resetting data: stop server, delete app.db, restart, re-run seed.sh.

Happy traveling!
