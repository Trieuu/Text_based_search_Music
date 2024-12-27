#!/bin/bash

# Default wait time (in seconds)
WAIT_TIME=${WAIT_TIME:-0}

echo "Waiting for $WAIT_TIME seconds before starting the Flask app..."
sleep $WAIT_TIME

# Execute multiple Python files in sequence
echo "Running script1.py..."
python indexing.py

echo "Running script2.py..."
python load_index_to_elastic.py

# Start the Flask application
echo "Starting Flask app..."
exec python main.py
