# Download covid-france dbt package
# dbt deps --project-dir ./demo_project

# Create tables and views
dbt run --project-dir ./demo_project

# Export metadata to Metabase
python dbt_sync_metabase.py

