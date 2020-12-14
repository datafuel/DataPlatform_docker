# Create tables and views
dbt run

# # Export metadata to Metabase
# dbt-metabase export \
#     --dbt_path . \
#     --mb_host @metabase \
#     --mb_user $DWH_POSTGRES_ADMIN \
#     --mb_password $DWH_POSTGRES_PASSWORD \
#     --database $DWH_POSTGRES_DB \
#     --schema $DWH_POSTGRES_PRS_SCHEMA

# # Generate docs
# dbt docs generate

# # Serve docs on http://localhost:4444
# dbt docs serve --port 4444

