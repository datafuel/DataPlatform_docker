# Create tables and views
dbt run

# Generate docs
dbt docs generate

# Serve docs on http://localhost:4444
dbt docs serve --port 4444