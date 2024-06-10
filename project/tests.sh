.#!/bin/bash

# Directory containing the data
DATA_DIR="../data"
# SQLite database file
DB_FILE="${DATA_DIR}/data.sqlite"

# Function to clean up before running tests
cleanup() {
    echo "Cleaning up old data files..."
    rm -f ${DATA_DIR}/*.csv
    rm -f ${DB_FILE}
}

# Function to check if a file exists
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "Error: $1 not found! Exiting"
        sleep 3
        exit 1
    fi
}

# Clean up old files
cleanup

# Run the data pipeline
echo "Running the data pipeline..."
chmod +x pipeline.sh
./pipeline.sh
#python pipeline.py

# Check if the SQLite database file is created
check_file_exists ${DB_FILE}

# Additional validation can be added here
echo "Data pipeline executed successfully and ${DB_FILE} exists."

echo "Running additional validation..."

echo "Database file: ${DB_FILE}"

# Debugging: Print the tables in the database
#echo "Running sqlite3 command to list tables..."
#sqlite3 "${DB_FILE}" ".tables"
# Check for the presence of expected tables in the database

echo "Checking tables..."
TABLES=$(sqlite3 "${DB_FILE}" ".tables")


if [[ "$TABLES" != *"asylum_applications"* ]]; then
    echo "Error: asylum_applications table not found in the database! Exiting"
    sleep 3
    exit 1
else
    echo "asylum_applications table found in the database"
fi

if [[ "$TABLES" != *"global_temperature"* ]]; then
    echo "Error: global_temperature table not found in the database! Exiting"
    sleep 3
    exit 1
else
    echo "global_temperature table found in the database"
fi
python test.py
echo "All tests passed successfully."
sleep 3
