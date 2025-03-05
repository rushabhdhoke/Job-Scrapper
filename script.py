import os
import duckdb
import pandas as pd
import requests
import logging
from datetime import datetime
from jobspy import scrape_jobs
from configparser import ConfigParser

# Load configuration from config.ini
config = ConfigParser()
config.read('config.ini')

# Configuration parameters
DB_FILE = config['paths']['db_file']
LOG_FILE = config['paths']['log_file']
DISCORD_WEBHOOK_URL = config['discord']['webhook_url']

# Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def write_to_log(message, level=logging.INFO):
    """Write a message to the log file with a specific level."""
    logging.log(level, message)

def send_to_discord(message):
    """Send a job update message to Discord via Webhook."""
    if not DISCORD_WEBHOOK_URL:
        write_to_log("Discord Webhook URL not set. Skipping notification.", level=logging.WARNING)
        return

    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            write_to_log("✅ Successfully sent message to Discord.")
        else:
            write_to_log(f"⚠️ Failed to send message to Discord: {response.status_code}, {response.text}", level=logging.WARNING)
    except Exception as e:
        write_to_log(f"❌ Error sending message to Discord: {str(e)}", level=logging.ERROR)

# Get DuckDB connection
def get_db_connection():
    return duckdb.connect(DB_FILE)

# Create jobs table if it doesn't exist
def create_jobs_table():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                site TEXT,
                job_url TEXT,
                date_added TIMESTAMP
            )
        """)

def scrape_and_upsert():
    """Scrape job listings and upsert data into DuckDB."""
    try:
        search_term = config['scraping']['search_term']
        location = config['scraping']['location']
        results_wanted = int(config['scraping']['results_wanted'])
        hours_old = int(config['scraping']['hours_old'])
        country_indeed = config['scraping']['country_indeed']

        write_to_log(f"Scraping jobs for '{search_term}' in '{location}'...")

        # Scrape jobs
        jobs = scrape_jobs(
            site_name=["glassdoor", "linkedin"],
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed
        )

        if jobs.empty:
            write_to_log("No jobs found. Script stopped.", level=logging.WARNING)
            print("No jobs found. Exiting script.")
            return

        # Add timestamp
        jobs['date_added'] = datetime.now()

        # Select required columns
        expected_columns = ['id', 'title', 'company', 'location', 'site', 'job_url', 'date_added']
        jobs = jobs[expected_columns]

        # Connect to DuckDB
        with get_db_connection() as conn:
            # Ensure the table exists
            create_jobs_table()

            # Retrieve existing job IDs
            existing_jobs = conn.execute("SELECT id FROM jobs").fetchdf()

            # Identify new jobs
            new_jobs = jobs[~jobs['id'].isin(existing_jobs['id'])]

            if not new_jobs.empty:
                # Convert DataFrame to list of tuples for batch insertion
                job_records = list(new_jobs.itertuples(index=False, name=None))

                # Insert new jobs
                conn.executemany(
                    "INSERT INTO jobs (id, title, company, location, site, job_url, date_added) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    job_records
                )

                # Log and send new jobs to Discord
                for _, row in new_jobs.iterrows():
                    message = f"**New Job Added!**\n**Title:** {row['title']}\n**Company:** {row['company']}\n**Location:** {row['location']}\n🔗 [Apply Here]({row['job_url']})"
                    write_to_log(message)
                    send_to_discord(message)

                print(f"✅ {len(new_jobs)} new jobs added to the database.")
            else:
                print("No new jobs to add.")

    except Exception as e:
        write_to_log(f"Error occurred: {str(e)}", level=logging.ERROR)
        print(f"An error occurred: {str(e)}")

def main():
    scrape_and_upsert()

if __name__ == "__main__":
    main()
