# ReleaseEZ.AI 

This project provides a full-stack setup with React (frontend), FastAPI (backend), PostgreSQL (database), and simplify locally using transformers.

## Backend Setup

1. Create a Python environment and install dependencies using pyenv:

```bash
cd backend
./setup_env.sh   # (first time)
pyenv activate releasez-env
```

2. Ensure PostgreSQL is running. Update the `DATABASE_URL` environment variable if it differs from the default `postgresql://postgres:postgres@localhost/postgres`.
```bash
brew install postgresql
brew services start postgresql
psql -U $(whoami) -d postgres   # (if above doesn't work)
psql -U postgres                # (connect to PostgreSQL)
  # SQL commands:
  \list                         # List all databases
  CREATE DATABASE releasezdb;   # create db name releasezdb
  \c releasezdb                 # connect to releasezdb
  \q                            # quit out of psql shell
psql -U hongear -d releasezdb   # get into sql shell
-- If you've previously created the database, add the latest columns:
ALTER TABLE patient ADD COLUMN IF NOT EXISTS has_generated_summary BOOLEAN DEFAULT FALSE;
ALTER TABLE patient ADD COLUMN IF NOT EXISTS has_printed_slip BOOLEAN DEFAULT FALSE;

clear database:
TRUNCATE TABLE doctor, patient, condition, procedure, medication_request, appointment, careplan, patient_pin RESTART IDENTITY CASCADE;
```
in backend/app/database.py  
update  
`DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/postgres")`  
to  
`DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hongear@localhost/releasezdb")`



3. Start the FastAPI server (run in backend directory):

```bash
uvicorn app.main:app --reload
```
http://127.0.0.1:8000/docs

### API Overview

Key endpoints served by FastAPI:

* `POST /auth/register` – create a user
* `POST /auth/login` – obtain a token (dummy implementation)
* `GET /patients` – list all patients
* `GET /patients/{id}` – patient detail
* `POST /bundles` – upload a discharge bundle
* `POST /fhir` – store a FHIR bundle (optionally associated with a patient) and
  automatically generate simplified text for Condition, Procedure and
  MedicationRequest resources. Include a `patient_id` query parameter if you wish
  to link the bundle to an existing patient.
* `GET /fhir` – list all stored bundles
* `GET /fhir/bundle/{id}` – retrieve a single bundle
* `GET /fhir/patient/{id}` – list bundles for a patient
* `POST /patients/import/{bundle_id}` – create a patient from a stored bundle
* `POST /summaries/generate` – simplify a patient's FHIR bundle using an LLM and
  return the patient details along with the simplified text

## Frontend Setup

Install dependencies and run the Vite development server:

```bash
cd frontend/frontend-doctor
npm install   # (first time)
npm run dev
```

### Seeding FHIR Data

An example bundle is included at `backend/sample_fhir_bundle.json`. You can store
it with:

```bash
curl -X POST "http://localhost:8000/fhir" \
  -H "Content-Type: application/json" \
  -d @backend/sample_fhir_bundle.json
```
This command uploads the bundle without linking it to a patient. Include a
`patient_id` query parameter if you want to associate it with one.
The backend will automatically simplify the included Condition, Procedure and
MedicationRequest resources and store those summaries next to the original
bundle.

After storing, create a patient from that bundle:

```bash
curl -X POST http://localhost:8000/patients/import/1
```

### Web Interface for Bundle Upload

The doctor-facing frontend provides a simple page for storing bundles. After running the frontend, navigate to `http://localhost:5173/fhir-upload` (default Vite port) and paste your bundle JSON. Clicking **Upload** will send
