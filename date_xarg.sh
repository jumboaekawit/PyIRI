#!/bin/bash

# Configuration
START_DATE="2026-07-01"
END_DATE=`date +%F`
MAX_PROCESSES=8  # Number of concurrent jobs

# Function to run for each date
process_date() {
    local current_date="$1"
    python Daily_parameters.py $current_date
    echo "Completed task for date: $current_date"
}

export -f process_date  # Export the function for xargs

# Generate dates, feed into xargs with parallel limit
current="$START_DATE"
while [ "$current" != "$(date -I -d "$END_DATE + 1 day")" ]; do
    echo "$current"
    current=$(date -I -d "$current + 1 day")
done | xargs -n 1 -P "$MAX_PROCESSES" bash -c 'process_date "$0"'

echo "All date processing complete!"