
# Generate docs
dbt docs generate --project-dir ./demo_project

# Serve docs on http://localhost:4444
dbt docs serve --port 4444 --project-dir ./demo_project --no-browser

