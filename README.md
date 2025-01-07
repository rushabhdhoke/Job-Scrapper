# Job Scraping and Visualization Setup

This project enables automated job scraping and visualization using Python scripts and Streamlit. Below are step-by-step instructions to set up the environment, test the scripts, schedule scraping jobs using cron, and launch the Streamlit application for data visualization.

---

## Prerequisites
1. Python 3.7 or above installed on your system.
2. Basic knowledge of terminal/command line usage.
3. Access to the project folder containing the following files:
    - `script.py`: The job scraping script.
    - `dashboard.py`: The Streamlit application.
    - `config.ini`: Configuration file for paths and parameters.
    - `requirements.txt`: Python dependencies.

---

## 1. Setting Up the Environment

### Step 1.1: Create a Virtual Environment
1. Open a terminal and navigate to the project folder:
   ```bash
   cd /path/to/project-folder
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```

### Step 1.2: Install Requirements
1. Install the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Testing the Job Scraping Script

### Step 2.1: Configure `config.ini`
1. Open `config.ini` and ensure the paths and parameters are correctly set, for example:
   ```ini
   [scraping]
   search_term = data analyst
   location = Canada
   results_wanted = 10
   hours_old = 24
   country_indeed = Canada

   [paths]
   csv_dir = /path/to/csv_folder
   log_file = /path/to/logs/job_scraping_log.txt
   ```

### Step 2.2: Run the Script
1. Run the job scraping script to populate the master file:
   ```bash
   python script.py
   ```
2. Verify that:
   - The `master_jobs.csv` file is created in the specified `csv_dir`.
   - Logs are written to the `log_file`.

### Step 2.3: Customize the Scraper
If you want to customize the scraping logic or parameters, explore the [JobSpy GitHub Repository](https://github.com/Bunsly/JobSpy) for more information on how to modify and extend its functionality.


---

## 3. Scheduling with Cron

### Step 3.1: Edit the Crontab
1. Open the crontab editor:
   ```bash
   crontab -e
   ```

### Step 3.2: Understand Cron Syntax
A cron job schedule has five fields that represent the timing:
   ```
   *  *  *  *  *  command_to_run
   -  -  -  -  -
   |  |  |  |  |
   |  |  |  |  +----- Day of the week (0 - 7, where 0 and 7 are Sunday)
   |  |  |  +-------- Month (1 - 12)
   |  |  +----------- Day of the month (1 - 31)
   |  +-------------- Hour (0 - 23)
   +----------------- Minute (0 - 59)
   ```

### Step 3.3: Add a Cron Job
1. Add the following line to schedule the script to run every 30 minutes:
   ```bash
   */30 * * * * /path/to/project-folder/venv/bin/python /path/to/project-folder/script.py
   ```
   Explanation:
   - `*/30`: Every 30 minutes.
   - `*`: Every hour.
   - `*`: Every day of the month.
   - `*`: Every month.
   - `*`: Every day of the week.

### Step 3.4: Verify Cron Job
1. Check the cron logs to ensure the job runs successfully:
   ```bash
   grep CRON /var/log/syslog
   ```

---

## 4. Setting Up the Streamlit App

### Step 4.1: Run the App
1. Launch the Streamlit application:
   ```bash
   streamlit run dashboard.py
   ```
2. Open the provided URL in a web browser (e.g., `http://localhost:8501`).

### Step 4.2: Interact with the Dashboard
1. Use the sidebar filters to search for jobs by title, company, or location.
2. View key performance indicators (KPIs) and filtered job listings.

---

## Troubleshooting

- **Master File Not Found**:
  Ensure the `script.py` script has run successfully and the `master_jobs.csv` file is located in the specified directory.

- **Streamlit App Not Loading**:
  Verify that you are in the correct environment and all dependencies are installed.

- **Cron Job Not Working**:
  Check the paths in the crontab entry and ensure the Python virtual environment is activated.

---

## Next Steps
- Deploy the Streamlit app to a cloud platform for remote access.
- Automate monitoring and logging for better reliability.


