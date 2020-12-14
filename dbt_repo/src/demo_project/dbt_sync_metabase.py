import metabt
import os


DWH_POSTGRES_DB = os.environ['DWH_POSTGRES_DB']
DWH_POSTGRES_PRS_SCHEMA = os.environ['DWH_POSTGRES_PRS_SCHEMA']

MB_ADMIN_EMAIL = os.environ['MB_ADMIN_EMAIL']
MB_ADMIN_PASSWORD = os.environ['MB_ADMIN_PASSWORD']

if __name__ == "__main__":

    metabt.export(
        dbt_path='.', 
        mb_host='metabase:3000', 
        mb_user=MB_ADMIN_EMAIL, 
        mb_password=MB_ADMIN_PASSWORD, 
        database="DWH Postgres", 
        schema=DWH_POSTGRES_PRS_SCHEMA,
        mb_https=False,
        sync=True,
        includes=["covid-france"]
        # excludes=["covid-france_ods"]
    )

# HOST = "metabase:3000"

# from metabt import MetabaseClient

# client = MetabaseClient(HOST, MB_ADMIN_EMAIL, MB_ADMIN_PASSWORD)

# ls_db_raw = client.list_databases()

# for db in ls_db_raw:
#     db_name = db['name']
#     db_id = db['id']
#     db_id_fetched = client.find_database_id(db_name)
#     print(db_name, db_id, db_id_fetched)

# client.find_database_id('DWH Postgres')

    



# print(dir(client))