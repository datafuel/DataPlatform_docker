# Create tables and views
dbt run --project-dir ./demo_project

# Export metadata to Metabase
# dbt-metabase export \
#     --dbt_path ./demo_project \
#     --mb_host @metabase \
#     --mb_user $DWH_POSTGRES_ADMIN \
#     --mb_password $DWH_POSTGRES_PASSWORD \
#     --database $DWH_POSTGRES_DB \
#     --schema $DWH_POSTGRES_PRS_SCHEMA

python dbt_sync_metabase.py

