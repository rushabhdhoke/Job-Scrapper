import pandas as pd
import streamlit as st
import os
from configparser import ConfigParser

st.set_page_config(layout='wide', page_title="Job Listings Dashboard")

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Paths
CSV_DIR = config['paths']['csv_dir']
MASTER_FILE = os.path.join(CSV_DIR, 'master_jobs.csv')

# Load data
def load_data():
    if not os.path.exists(MASTER_FILE):
        st.error("Master file not found. Please run the scraper first.")
        return pd.DataFrame()
    df = pd.read_csv(MASTER_FILE)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df = df.dropna(subset=['date_added'])
    return df.sort_values(by='date_added', ascending=False)

# Load and display data
df = load_data()

if df.empty:
    st.warning("No job data available. Run the scraper to fetch jobs.")
else:
    # Sidebar filters
    st.sidebar.header("Filter Options")
    search_title = st.sidebar.text_input("Search Title")
    search_company = st.sidebar.text_input("Search Company")
    location_options = df['location'].unique()
    filter_location = st.sidebar.multiselect("Filter by Location", location_options)

    # Apply filters
    filtered_df = df.copy()
    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]
    if search_company:
        filtered_df = filtered_df[filtered_df['company'].str.contains(search_company, case=False, na=False)]
    if filter_location:
        filtered_df = filtered_df[filtered_df['location'].isin(filter_location)]

    # Display KPIs
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric(label="Total Jobs", value=len(df))
    with kpi_col2:
        jobs_today = df[df['date_added'].dt.date == pd.Timestamp.now().date()].shape[0]
        st.metric(label="Today's Jobs", value=jobs_today)
    with kpi_col3:
        if not df['company'].empty:
            top_company = df['company'].value_counts().idxmax()
            top_company_jobs = df['company'].value_counts().max()
            st.metric(label="Top Hiring Company", value=top_company, delta=f"{top_company_jobs} Jobs")
    with kpi_col4:
        if not df['location'].empty:
            top_location = df['location'].value_counts().idxmax()
            top_location_count = df['location'].value_counts().max()
            st.metric(label="Top Job Location", value=top_location, delta=f"{top_location_count} Jobs")

    # Display filtered data
    st.markdown("#### Job Listings")
    st.dataframe(
        filtered_df[['title', 'company', 'location', 'date_added', 'job_url']],
        use_container_width=True,
        column_config={
            'title': st.column_config.Column('Title', width='large'),
            'company': st.column_config.Column('Company', width='small'),
            'location': st.column_config.Column('Location', width='small'),
            'date_added': st.column_config.Column('Date', width='small'),
            'job_url': st.column_config.LinkColumn('Job URL', display_text="Link", width='small')
        }
    )
