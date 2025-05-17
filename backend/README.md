# FHIR Discharge Simplification API

A FastAPI-based service that receives FHIR Bundles, stores the raw data, simplifies discharge information using an AI model, and provides patient- and doctor-facing endpoints.

## 🔧 Features
- Accepts FHIR Bundles via `/fhir/bundle`
- Stores raw bundle to PostgreSQL
- Asynchronously simplifies discharge content
- Doctor view: shows raw + simplified (`/doctor/{raw_id}`)
- Patient view: simplified only (`/patient/{simplified_id}`)

## 📦 Setup (macOS/Linux)

The setup script will:
- Create a Python virtual environment
- Install Python dependencies
- Install PostgreSQL via Homebrew (if needed)
- Start the PostgreSQL service
- Create the `fhirdb` database if missing, in db.py update DB_DSN = "postgresql://your_username@localhost:5432/fhirdb" change your_username, run whoami to check username
- Create the required tables (`raw_bundles`, `simplified_bundles`)

1. Clone the repo
2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. Start the server:
   ```bash
   python run.py
   ```

## 🧪 Testing
Use `curl`, Postman, or `pytest` to test endpoints. Sample test case:
```bash
curl -X POST http://localhost:8000/fhir/bundle \
     -H "Content-Type: application/json" \
     -d @fhir_sample.json
```

## 🛠 Project Structure
```
.
├── app/
│   ├── main.py          # FastAPI app
│   ├── db.py            # Database connection pool
│   ├── models.py        # Pydantic data models
│   ├── services.py      # Simplification logic
│   └── routes/
│       └── fhir.py      # Route handlers
├── run.py               # Entrypoint
├── setup.sh             # Environment setup script
├── requirements.txt     # Python dependencies
├── .gitignore           # Files to exclude from Git
└── README.md            # Project info
```

## 🧩 Database Schema (PostgreSQL)
```sql
CREATE TABLE raw_bundles (
    id UUID PRIMARY KEY,
    bundle JSONB
);

CREATE TABLE simplified_bundles (
    id UUID PRIMARY KEY,
    raw_id UUID REFERENCES raw_bundles(id),
    simplified JSONB
);
```
Test the Connection
Run:
bash
psql fhirdb

Make sure you can see your tables:
sql 
\dt

---
