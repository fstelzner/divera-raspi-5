#!/bin/bash

# Define variables
WATCHED_DIR="/home/pi/depechen"  # Change this to your directory
ARCHIVE_DIR="$WATCHED_DIR/archive"
LOG_FILE="$ARCHIVE_DIR/depeche.log"

# Create archive directory if it does not exist
mkdir -p "$ARCHIVE_DIR"

# Check for .pdf files in the watched directory
for FILE in "$WATCHED_DIR"/*.pdf; do
    # Check if the file exists and is not an empty list (in case no files are found)
    if [ -e "$FILE" ]; then
        FILENAME=$(basename "$FILE")
        
        # Check if the filename is already logged
        if ! grep -q "$FILENAME" "$LOG_FILE"; then
            # Print the file
            lp "$FILE"
            
            # Move the file to the archive directory
            mv "$FILE" "$ARCHIVE_DIR"
            
            # Log the filename
            echo "$FILENAME" >> "$LOG_FILE"
        fi
    fi
done
