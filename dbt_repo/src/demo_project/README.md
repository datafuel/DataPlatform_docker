# Covid France dbt

# About
A dbt project allowing the processing of data related to COVID-19 in France.

# Prerequisites
- A Python environment with dbt (`pip install dbt`)

# Quickstart
1. Clone repo `git clone https://github.com/datafuel/Covid_France_dbt.git`
2. Run `cd Covid_France_dbt`
4. Move the `profiles/profiles.yml` to your `/.dbt` directory
5. Run `dbt run --project-dir ./covid_france`
6. Serve docs on http://localhost:4444 with `dbt docs serve --port 4444 --project-dir ./covid_france`   

# Use this project as a package
1. Create a file next to your `dbt_project.yml` called `packages.yml` with the following content : 
```
packages:
  - git: "https://github.com/datafuel/Covid_France_dbt.git"
    revision: 0.0.1
```
## Data Sources used in the project

- https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7
- https://www.data.gouv.fr/fr/datasets/r/70cef74f-70b1-495a-8500-c089229c0254
  
