# DataPlatform on Docker Compose
A complete Open Source Data Platform with ETL, DataWarehouse and DataViz

# Prerequisites

- Docker (started) and docker-compose (just install Docker for Desktop if you are on laptop) 

# Quickstart

1. Clone repo `git clone https://github.com/datafuel/DataPlatform_docker.git`
2. Run `cd DataPlatform_docker`
3. Rename **.env.example** to **.env** and replace dummy values with yours
4. Run `docker-compose up` then access the services
Make sure to wait at least 30 seconds before launching MetaBase ! 


## Access services
  - Metabase : http://localhost:3000
  - Meltano : http://localhost:5000