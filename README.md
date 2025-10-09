# AI Automation Scraper

A daily web scraper that collects the latest articles about **AI in Automation** and sends a curated email digest.  
Built with Python, BeautifulSoup, and SQLite, this project is designed for personal use and automation.

---

## Features

- Scrapes AI Automation news from multiple sources.
- Stores articles in a local SQLite database (`scraper.db`).
- Sends daily email notifications with new articles.
- Logs all activity for easy debugging.
- Works on Linux and Windows with a virtual environment.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Angelique867/AI-Automation-Scraper.git
cd AI-Automation-Scraper
```
### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux
# OR
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your environment variables

Create a file called .env or email_password.env in the project root with your email credentials:

```bash
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECEIVER_EMAIL=recipient_email@gmail.com
```
⚠️ Never commit this file to GitHub.
It is included in .gitignore to prevent accidental exposure.

### 5. Run the scraper manually

```bash
python fetch_google.py
```

Check the logs:
```bash
cat logs/cron_run.log
```

### 6. Automate daily runs (Linux)
#### 1. Create a shell script run_scraper.sh: (Be sure to update the path for your computer)
```bash
#!/bin/bash
cd ~/Documents/ai_scraper || exit
source venv/bin/activate
python fetch_google.py >> logs/cron_run.log 2>&1
```
#### 2. Make it executable:
```bash
chmod +x run_scraper.sh
```
#### 3. Schedule with cron:
```bash
crontab -e
```
Add: (Be sure to update the path for your computer)
```bash
0 9 * * * /home/YourUsername/Documents/ai_scraper/run_scraper.sh
```

### 7. Logs
All scraper activity is logged to:
```bash
logs/cron_run.log
```
You can check it anytime with:
```bash
tail -f logs/cron_run.log
```

### 8. Notes
* Virtual environment (venv/) and .env files are ignored by Git.
* Use app passwords for Gmail instead of your main password.
* Emails are only sent if new articles are found (configurable in the script).

Dependencies
* Python 3.x
* requests
* beautifulsoup4
* python-dotenv
* sqlite3 (built-in)
* smtplib (built-in)

License
This project is for personal use. Do not use credentials or scrape sites without permission.
