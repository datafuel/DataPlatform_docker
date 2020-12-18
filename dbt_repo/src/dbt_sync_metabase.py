import metabt
import os


DWH_POSTGRES_DB = os.environ['DWH_POSTGRES_DB']
DWH_POSTGRES_PRS_SCHEMA = os.environ['DWH_POSTGRES_PRS_SCHEMA']

MB_ADMIN_EMAIL = os.environ['MB_ADMIN_EMAIL']
MB_ADMIN_PASSWORD = os.environ['MB_ADMIN_PASSWORD']

if __name__ == "__main__":

    metabt.export(
        dbt_path='/src/demo_project', 
        mb_host='metabase:3000', 
        mb_user=MB_ADMIN_EMAIL, 
        mb_password=MB_ADMIN_PASSWORD, 
        database="DWH Postgres", 
        mb_https=False,
        sync=True
    )