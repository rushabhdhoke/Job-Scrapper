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

## Troubleshooting

- **Master File Not Found**:
  Ensure the `script.py` script has run successfully and the `master_jobs.csv` file is located in the specified directory.

---

## Next Steps
- Visualize the obtained CSV in Tableau for better understanding

