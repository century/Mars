#!/bin/zsh

# Add all changes
git add .

# Get the current date and time in the required format
DATE=$(date +"%Y-%m-%dT%H:%M:%S")

# Commit with the date in the message
git commit -m "Commit $DATE"

# Push to the main branch
git push -u origin main
