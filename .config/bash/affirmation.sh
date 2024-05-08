#!/bin/bash

# File that stores the last time the affirmation was shown
HUSH_FILE="/c/Users/tahazzot/.config/.hush-affirmation"

# Current time in seconds since epoch
current_time=$(date +%s)

# Flag to indicate whether the affirmation should be shown
show_affirmation=false

# Check if the .hush-affirmation file exists
if [ -f "$HUSH_FILE" ]; then
    # Read the last recorded time from the file
    last_time=$(<"$HUSH_FILE")

    # Calculate the time difference in seconds
    time_difference=$((current_time - last_time))

    # Check if an hour (3600 seconds) has passed
    if [ $time_difference -ge 3600 ]; then
        # An hour or more has passed, allow showing the affirmation
        show_affirmation=true
        # Update the time in the file
        echo "$current_time" > "$HUSH_FILE"
    fi
else
    # The file does not exist, so create it and set the current time
    echo "$current_time" > "$HUSH_FILE"
    show_affirmation=true
fi

# If it's time to show the affirmation
if $show_affirmation; then
    # Fetch affirmation from the API
    affirmation=$(curl -s https://www.affirmations.dev/ | awk -F '"' '/affirmation/ {print $4}')

    # Use cowsay with the ghostbusters cow file and the fetched affirmation
    # Pipe the output to lolcatjs for colored output
    cowsay -f ghostbusters "$affirmation" | lolcatjs
fi