# 🚁 Mission Planner API

A robust FastAPI-based REST API for authoring, validating, and storing UAV missions. This project demonstrates high-level software engineering discipline with from-scratch implementations of graph and interval-based algorithms.

## 🚀 Features

- **Mission Management**: Create, store, and manage UAV missions and flight logs.
- **Topological Validation**: Uses a custom **Topological Sort** algorithm ($O(V+E)$) to validate mission step dependencies and detect circular loops.
- **Airspace Conflict Detection**: Uses a custom **Interval Tree** to check for mission schedule conflicts against restricted airspace windows in $O(\log N)$ time.
- **MAVLink Export**: Export missions as QGroundControl compatible `.waypoints` files.
- **Fully Tested**: Includes unit tests for DSA components and integration tests for all API endpoints.
- **Docker Ready**: Fully containerized for easy deployment.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy (SQLite)
- **Testing**: Pytest
- **DSA**: Custom Topological Sort & Interval Tree implementations

## 📦 Installation & Setup

### Using Docker (Recommended)
```bash
docker build -t mission-planner .
docker run -p 8000:8000 mission-planner
```

### Local Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn app.main:app --reload`

## 🧪 Testing
Run the test suite to verify the algorithms and API:
```bash
pytest
```

## 📖 API Documentation
Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
