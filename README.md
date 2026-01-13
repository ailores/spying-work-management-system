# Spy Cat Agency (SCA)

Management system for Spy Cat Agency. This application allows you to manage spy cats and their missions.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended for dependency management)

## Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:ailores/spying-work-management-system.git
   cd spy-cat-agency
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory (based on the example below):
   ```env
   PROJECT_NAME="SpyCatAgency API"
   CATS_BREEDS_API_URL=https://api.thecatapi.com/v1/breeds
   ```

## Installation

Using `uv` (recommended):
```bash
uv sync
```

Alternatively, using `pip`:
```bash
pip install -r requirements.txt
```
*(Note: If requirements.txt is not present, use `uv pip compile pyproject.toml -o requirements.txt` or install dependencies listed in `pyproject.toml`)*

## Running the Application

To start the FastAPI server:

Using `uv`:
```bash
uv run uvicorn app.main:app --reload
```

Or directly with `python` (if dependencies are installed in your environment):
```bash
python -m app.main
```

The server will start at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

- `app/api/`: API routes and dependencies.
- `app/core/`: Database configuration, models, and schemas
- `app/main.py`: Application entry point.
- `pyproject.toml`: Project metadata and dependencies.