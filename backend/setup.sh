# This script sets up a virtual environment, installs Python dependencies,
# installs PostgreSQL via Homebrew (if not present), and prepares the database.
#!/bin/bash

VENV_DIR=".venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate and install requirements
echo "Activating virtual environment and installing dependencies..."
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check for PostgreSQL installation
brew services start postgresql
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL not found. Installing via Homebrew..."
    brew install postgresql
else
    echo "PostgreSQL is already installed."
fi

# Create fhirdb database if it doesn't exist
DB_EXIST=$(psql -Atqc "SELECT 1 FROM pg_database WHERE datname = 'fhirdb'")
if [ "$DB_EXIST" != "1" ]; then
    echo "Creating 'fhirdb' database..."
    createdb fhirdb
else
    echo "Database 'fhirdb' already exists."
fi

# Create tables if not present
psql fhirdb <<EOF
CREATE TABLE IF NOT EXISTS raw_bundles (
    id UUID PRIMARY KEY,
    bundle JSONB
);

CREATE TABLE IF NOT EXISTS simplified_bundles (
    id UUID PRIMARY KEY,
    raw_id UUID REFERENCES raw_bundles(id),
    simplified JSONB
);
EOF

echo "✅ Setup complete. To activate the environment manually later:"
echo "source $VENV_DIR/bin/activate"