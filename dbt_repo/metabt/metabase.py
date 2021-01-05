import logging
import yaml
import requests as rq
import json
import time
from typing import Any

from .configurator_settings import (
    DWH_POSTGRES_ADMIN, DWH_POSTGRES_PASSWORD, DWH_POSTGRES_DB, 
    DWH_POSTGRES_HOST, MB_ADMIN_FIRST_NAME, MB_ADMIN_LAST_NAME, 
    MB_ADMIN_EMAIL, MB_ADMIN_PASSWORD, SETUP_TOKEN_URL, 
    SETUP_ADMIN_URL, SETUP_DATABASE_URL, NEW_USER_URL
)

class MetabaseClient:
    """Metabase API client.
    """

    _SYNC_PERIOD_SECS = 5

    def __init__(self, host: str, user: str, password: str, https = False):
        """Constructor.
        
        Arguments:
            host {str} -- Metabase hostname.
            user {str} -- Metabase username.
            password {str} -- Metabase password.
        
        Keyword Arguments:
            https {bool} -- Use HTTPS instead of HTTP. (default: {True})
        """

        self.host = host
        self.protocol = "https" if https else "http"
        self.session_id = self.get_session_id(user, password)
        logging.info("Session established successfully")
    
    def get_session_id(self, user: str, password: str) -> str:
        """Obtains new session ID from API.
        
        Arguments:
            user {str} -- Metabase username.
            password {str} -- Metabase password.
        
        Returns:
            str -- Session ID.
        """

        return self.api('post', '/api/session', authenticated=False, json={
            'username': user,
            'password': password
        })['id']
    
    def sync_and_wait(self, database: str, models: list, timeout = 30) -> bool:
        """Synchronize with the database and wait for schema compatibility.
        
        Arguments:
            database {str} -- Metabase database name.
            models {list} -- List of dbt models read from project.
        
        Keyword Arguments:
            timeout {int} -- Timeout before giving up in seconds. (default: {30})
        
        Returns:
            bool -- True if schema compatible with models, false if still incompatible.
        """

        if timeout < self._SYNC_PERIOD_SECS:
            logging.critical("Timeout provided %d secs, must be at least %d", timeout, self._SYNC_PERIOD_SECS)
            return
        database_id = self.find_database_id(database)
        print(f'{database}/{database_id} Sync in progress..')

        if not database_id:
            logging.critical("Cannot find database by name %s", database)
            return
        
        response_sync = self.api('post', f'/api/database/{database_id}/sync')

        deadline = int(time.time()) + timeout
        sync_successful = False
        while True:
            sync_successful = self.models_compatible(database_id, models)
            time_after_wait = int(time.time()) + self._SYNC_PERIOD_SECS
            if not sync_successful and time_after_wait <= deadline:
                time.sleep(self._SYNC_PERIOD_SECS)
            else:
                break
        print('Sync successful')
        return sync_successful

    def models_compatible(self, database_id: str, models: list) -> bool:
        """Checks if models compatible with the Metabase database schema.
        
        Arguments:
            database_id {str} -- Metabase database ID.
            models {list} -- List of dbt models read from project.
        
        Returns:
            bool -- True if schema compatible with models, false otherwise.
        """

        _, field_lookup = self.build_metadata_lookups(database_id)

        for model in models:
            model_name = model['name'].upper()
            if model_name not in field_lookup:
                logging.warn("Model %s not found", model_name)
                return False

            table_lookup = field_lookup[model_name]
            for column in model.get('columns', []):
                column_name = column['name'].upper()
                if column_name not in table_lookup:
                    logging.warn("Column %s not found in model %s", column_name, model_name)
                    return False
        
        return True

    def export_models(self, database: str, models: list):
        """Exports dbt models to Metabase database schema.
        
        Arguments:
            database {str} -- Metabase database name.
            models {list} -- List of dbt models read from project.
        """


        database_id = self.find_database_id(database)
        if not database_id:
            logging.critical("Cannot find database by name %s", database)
            return
        
        table_lookup, field_lookup = self.build_metadata_lookups(database_id)

        for model in models:
            
            self.export_model(model, table_lookup, field_lookup)
    
    def export_model(self, model: dict, table_lookup: dict, field_lookup: dict):
        """Exports one dbt model to Metabase database schema.
        
        Arguments:
            model {dict} -- One dbt model read from project.
            table_lookup {dict} -- Dictionary of Metabase tables indexed by name.
            field_lookup {dict} -- Dictionary of Metabase fields indexed by name, indexed by table name.
        """

        model_name = model['name'].upper()

        api_table = table_lookup.get(model_name)
        if not api_table:
            print('table does not exist')
            logging.error('Table %s does not exist in Metabase', model_name)
            return

        table_id = api_table['id']
        if api_table['description'] != model['description']:
            print('updating description')
            # Update with new values
            self.api('put', f'/api/table/{table_id}', json={
                'description': model['description']
            })
            logging.info("Updated table %s successfully", model_name)
        else:
            print(f"Table {model_name} is up-to-date")
            logging.info("Table %s is up-to-date", model_name)

        for column in model.get('columns', []):
            self.export_column(model_name, column, field_lookup)
    
    def export_column(self, model_name: str, column: dict, field_lookup: dict):
        """Exports one dbt column to Metabase database schema.
        
        Arguments:
            model_name {str} -- One dbt model name read from project.
            column {dict} -- One dbt column read from project.
            field_lookup {dict} -- Dictionary of Metabase fields indexed by name, indexed by table name.
        """

        column_name = column['name'].upper()

        field = field_lookup.get(model_name, {}).get(column_name)
        if not field:
            print('field does not exist in Metabase')
            logging.error('Field %s.%s does not exist in Metabase', model_name, column_name)
            return
        
        field_id = field['id']
        fk_target_field_id = None
        if column.get('special_type') == 'type/FK':
            target_table = column['fk_target_table']
            target_field = column['fk_target_field']
            fk_target_field_id = field_lookup.get(target_table, {}) \
                .get(target_field, {}) \
                .get('id')
            
            if fk_target_field_id:
                self.api('put', f'/api/field/{fk_target_field_id}', json={
                    'special_type': 'type/PK'
                })
            else:
                logging.error("Unable to find foreign key target %s.%s", target_table, target_field)
        
        # Nones are not accepted, default to normal
        if not column.get('visibility_type'):
            column['visibility_type'] = 'normal'

        api_field = self.api('get', f'/api/field/{field_id}')
        if api_field['description'] != column.get('description') or \
                api_field['special_type'] != column.get('special_type') or \
                api_field['visibility_type'] != column.get('visibility_type') or \
                api_field['fk_target_field_id'] != fk_target_field_id:
            # Update with new values
            print(f'Updating {column_name}')
            self.api('put', f'/api/field/{field_id}', json={
                'description': column.get('description'),
                'special_type': column.get('special_type'),
                'visibility_type': column.get('visibility_type'),
                'fk_target_field_id': fk_target_field_id
            })
            logging.info("Updated field %s.%s successfully", model_name, column_name)
        else:
            logging.info("Field %s.%s is up-to-date", model_name, column_name)
    
    def find_database_id(self, name: str) -> str:
        """Finds Metabase database ID by name.
        
        Arguments:
            name {str} -- Metabase database name.
        
        Returns:
            str -- Metabase database ID.
        """

        for database in self.api('get', '/api/database'):
            if database['name'].upper() == name.upper():
                return database['id']
        return None


    def list_databases(self, ) -> list:
        """List All databases added to Metabase .
        
        Arguments:
            name {str} -- Metabase database name.
        
        Returns:
            list -- List of database dictionaries returned by Metabase.
        """

        return self.api('get', '/api/database')
    
    def get_database_metadata(self, database_id: str) -> (dict):
        """Get database etadata from Metabase
        
        Arguments:
            database_id {str} -- Metabase database ID.        
        Returns:
            dict -- Whatever returns the metadata API
        """
        metadata = self.api('get', f'/api/database/{database_id}/metadata')
        return metadata
        


    def build_metadata_lookups(self, database_id: str) -> (dict, dict):
        """Builds table and field lookups.
        
        Arguments:
            database_id {str} -- Metabase database ID.        
        Returns:
            dict -- Dictionary of tables indexed by name.
            dict -- Dictionary of fields indexed by name, indexed by table name.
        """

        table_lookup = {}
        field_lookup = {}

        metadata = self.api('get', f'/api/database/{database_id}/metadata')
        for table in metadata.get('tables', []):
            table_schema = 'public' if table['schema'] is None else table['schema']
            # if table_schema.upper() != schema.upper():
            #     continue

            table_name = table['name'].upper()
            table_lookup[table_name] = table

            table_field_lookup = {}

            for field in table.get('fields', []):
                field_name = field['name'].upper()
                table_field_lookup[field_name] = field

            field_lookup[table_name] = table_field_lookup
        return table_lookup, field_lookup

    def api(self, method: str, path: str, authenticated = True, critical = True, **kwargs) -> Any:
        """Unified way of calling Metabase API.
        
        Arguments:
            method {str} -- HTTP verb, e.g. get, post, put.
            path {str} -- Relative path of endpoint, e.g. /api/database.
        
        Keyword Arguments:
            authenticated {bool} -- Includes session ID when true. (default: {True})
            critical {bool} -- Raise on any HTTP errors. (default: {True})
        
        Returns:
            Any -- JSON payload of the endpoint.
        """

        headers = {}
        if 'headers' not in kwargs:
            kwargs['headers'] = headers
        else:
            headers = kwargs['headers'].copy()
        
        if authenticated:
            headers['X-Metabase-Session'] = self.session_id

        # response = rq.request(method, f"{self.protocol}://{self.host}{path}", **kwargs)
        response = rq.request(method, f"http://{self.host}{path}", **kwargs)
        if critical:
            response.raise_for_status()
        elif not response.ok:
            return False
        
        return json.loads(response.text)

class AdminClient:

    def __init__(self):

        # Get temporary token
        temp_token = self.return_token_if_connection_open()
        
        # Create Admin user and get admin sesssion token
        auth_token = self.create_admin_user( 
            temp_token, 
            MB_ADMIN_FIRST_NAME, 
            MB_ADMIN_LAST_NAME, 
            MB_ADMIN_EMAIL, 
            MB_ADMIN_PASSWORD
        )

        # Set Admin session headers for future requests
        self.headers = {'X-Metabase-Session':auth_token}

        # Add Postgres Database (part of the onboarding process)
        self.add_postgres_database(
            DWH_POSTGRES_HOST,
            DWH_POSTGRES_DB,
            DWH_POSTGRES_ADMIN,
            DWH_POSTGRES_PASSWORD
        )


    def return_token_if_connection_open(self):
        connection_is_not_open = True
        while connection_is_not_open:
            try:
                res_token = rq.get(SETUP_TOKEN_URL)
                if res_token.ok:
                    connection_is_not_open = False
                    temp_token = res_token.json()['setup-token']
            except rq.exceptions.ConnectionError:
                print(f'Database is still not available.. waiting {WAITING_TIME}s')
                time.sleep(WAITING_TIME)
        print(f'Temporary token generated by Metabase : {temp_token}')
        return temp_token

    def create_admin_user(self, temp_token, first_name, last_name, email, password):
        """
        Create Admin User and return Authentication Token

        Parameters:
        - setup_admin_url (str): Metabase endpoint to setup Admin
        - temp_token (str): Temporary token generated by Metabase API
            (endpoint api/session/properties)
        - first_name (str): First Name of the Admin
        - last_name (str): Last Name of the Admin
        - email (str): Email of the Admin
        - password (str): Password of the Admin

        Returns:
        - auth_token (str): Admin Authentication Token generated by Metabase
        """

        data_admin = {
            "token": temp_token,
            "prefs":{"site_name":"Metabase","allow_tracking":"true", "site_locale":"fr"},
            "user": {
                "email": email, 
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "site_name":"Metabase"
            },
            "database": None
        }

        res_admin = rq.post(SETUP_ADMIN_URL, json=data_admin)
        if res_admin.ok:
            auth_token = res_admin.json()['id']
            
            print('Admin created')
        
            return auth_token

        else:
            raise Exception(f'Cannot connect to Metabase. Status Code : {res_admin.status_code}')


    def add_postgres_database(
        self, 
        database_host, 
        database_name, 
        admin, 
        password
    ):
        """
        Create Admin User and return Authentication Token

        Parameters:
        - setup_database_url (str): Metabase endpoint to add database
        - headers (dict): Headers in the format:
            {'X-Metabase-Session':'your-token'}
        - database_host (str): Host of the database
        - database_name (str): Name of the database
        - admin (str): Username of the Admin
        - password (str): Password of the Admin

        Returns:
        - auth_token (str): Admin Authentication Token generated by Metabase
        """

        dc_db = {
            "engine": "postgres",
            "name": "DWH Postgres",
            "details": {
                "host": database_host,
                "port": "5432",
                "db": database_name,
                "user": admin,
                "password": password
            },
            "is_full_sync": True
        }

        res_db = rq.post(SETUP_DATABASE_URL, json=dc_db, headers=self.headers)

        if res_db.ok:
            print('Database succesfully created')