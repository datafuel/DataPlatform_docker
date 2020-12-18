import requests as rq
from metabt import DbtReader, MetabaseClient

DBT_PATH = '/src/demo_project'

from metabt import (
    DWH_POSTGRES_ADMIN, DWH_POSTGRES_PASSWORD, DWH_POSTGRES_DB, 
    DWH_POSTGRES_HOST, MB_ADMIN_FIRST_NAME, MB_ADMIN_LAST_NAME, 
    MB_ADMIN_EMAIL, MB_ADMIN_PASSWORD, SETUP_TOKEN_URL, 
    SETUP_ADMIN_URL, SETUP_DATABASE_URL, NEW_USER_URL
)

# inlcudes = []
# excludes = []
models = DbtReader(DBT_PATH).read_models()
        # includes=includes, 
        # excludes=excludes
# )

print(models)

# client = MetabaseClient('metabase:3000', MB_ADMIN_EMAIL, MB_ADMIN_PASSWORD, True)
# database_id = client.find_database_id('DWH Postgres')
# meta = client.get_database_metadata(database_id)


# print(meta)
