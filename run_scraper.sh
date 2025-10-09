#!/bin/bash
# run_scraper.sh — runs the AI scraper automatically

# Go to your project directory
cd ~/Projects/ai_automation || exit

# Activate virtual environment
source venv/bin/activate

# Run the scraper
python fetch_google.py >> logs/cron_run.log 2>&1
