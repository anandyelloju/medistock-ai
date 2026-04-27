#!/bin/bash

# Initialize the database
echo "Initializing database..."
python scripts/init_db.py

# Start the application
# Use the PORT environment variable if provided (default 8501)
PORT=${PORT:-8501}

echo "Starting MediStock AI on port $PORT..."
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
