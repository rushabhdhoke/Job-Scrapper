import os
import pandas as pd
from datetime import datetime
from jobspy import scrape_jobs
import logging
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Configuration parameters
CSV_DIR = config['paths']['csv_dir']
MASTER_FILE = os.path.join(CSV_DIR, 'master_jobs.csv')
LOG_FILE = config['paths']['log_file']

# Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def write_to_log(message, level=logging.INFO):
    """Write a message to the log file with a specific level."""
    logging.log(level, message)

def scrape_and_upsert(search_term: str, location: str, results_wanted: int, hours_old: int, country_indeed: str):
    """Scrape job listings and upsert data into the master file."""
    try:
        # Debugging: Print the master file path
        print(f"Using master file: {MASTER_FILE}")

        # Scrape jobs
        jobs = scrape_jobs(
            site_name=["glassdoor", "indeed", "linkedin"],
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

        if os.path.exists(MASTER_FILE):
            # Load existing data
            master_df = pd.read_csv(MASTER_FILE)

            # Combine and deduplicate
            columns_to_check = ['title', 'company', 'location']
            combined_df = pd.concat([master_df, jobs]).drop_duplicates(subset=columns_to_check, keep='first')

            # Save updated master file
            combined_df.to_csv(MASTER_FILE, index=False)

            # Log new jobs
            new_jobs = jobs[~jobs[columns_to_check].apply(tuple, axis=1).isin(master_df[columns_to_check].apply(tuple, axis=1))]
            if not new_jobs.empty:
                for _, row in new_jobs.iterrows():
                    write_to_log(f"New job added: {row['title']} at {row['company']}. Location: {row['location']}. Link: {row['job_url']}")
                print(f"{len(new_jobs)} new jobs added to the master file.")
        else:
            # Create master file if it doesn't exist
            jobs.to_csv(MASTER_FILE, index=False)
            write_to_log(f"Master file created and saved {len(jobs)} jobs.")
            print(f"Master file created and saved {len(jobs)} jobs.")

    except Exception as e:
        write_to_log(f"Error occurred: {str(e)}", level=logging.ERROR)
        print(f"An error occurred: {str(e)}")

def main():
    # Parameters
    search_term = config['scraping']['search_term']
    location = config['scraping']['location']
    results_wanted = int(config['scraping']['results_wanted'])
    hours_old = int(config['scraping']['hours_old'])
    country_indeed = config['scraping']['country_indeed']

    # Ensure CSV_DIR exists
    os.makedirs(CSV_DIR, exist_ok=True)

    # Scrape and upsert jobs
    scrape_and_upsert(search_term, location, results_wanted, hours_old, country_indeed)

if __name__ == "__main__":
    main()
