metabt export \
    --dbt_path . \
    --mb_host "metabase:3000" \
    --mb_user MB_ADMIN_EMAIL \
    --mb_password MB_ADMIN_PASSWORD \
    --database "DWH Postgres" \
    --schema DWH_POSTGRES_PRS_SCHEMA \
    # --mb_https HTTPS \
    --sync ENABLE \
    --includes ["covid-france"] 