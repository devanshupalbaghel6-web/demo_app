# Simple E-commerce App

This is a simple e-commerce application built with FastAPI (Backend) and React (Frontend).

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (Async), Alembic, PostgreSQL (Neon), AsyncPG.
- **Frontend**: React (Vite), Axios, TanStack Query.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- A PostgreSQL database (e.g., from [Neon](https://neon.tech/))

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create a virtual environment (if not already created):
    ```bash
    python -m venv .venv
    ```

3.  Activate the virtual environment:
    - Windows: `.venv\Scripts\activate`
    - Mac/Linux: `source .venv/bin/activate`

4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5.  Configure the database:
    - Create a `.env` file in the `backend` directory.
    - Add your Neon PostgreSQL connection string:
      ```
      DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
      ```
    - **Note**: Make sure to use `postgresql+asyncpg` as the scheme.

6.  Run Database Migrations (Optional for first run as app creates tables, but good practice):
    ```bash
    alembic upgrade head
    ```

7.  Start the server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    Docs at `http://localhost:8000/docs`.

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the development server:
    ```bash
    npm run dev
    ```
    The app will be available at `http://localhost:5173`.

## Project Structure

- `backend/`: FastAPI application
    - `main.py`: Entry point and API routes
    - `database.py`: Database connection setup
    - `models.py`: SQLAlchemy database models
    - `schemas.py`: Pydantic schemas for data validation
    - `alembic/`: Database migration scripts
- `frontend/`: React application
    - `src/api.js`: Axios setup
    - `src/components/ProductList.jsx`: Component to display products
    - `src/App.jsx`: Main application component
