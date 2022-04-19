import json
import logging
import pandas as pd
import os
import sys
import src.main.config as config
from src.main.utils import utilities
from google.cloud import datastore
from google.oauth2 import service_account

# Logging Methods
log_level = os.getenv('LOG_LEVEL') if 'LOG_LEVEL' in os.environ else 'DEBUG'
level_attribute = utilities.guess_log(log_level)
logging.basicConfig(stream=sys.stdout, level=level_attribute,
                    format="%(asctime)-15s %(name)s [%(levelname)s] %(message)s")


# TODO: Migrate to Firebase Datastore

class Datastore(object):
    # Global
    google_sa_file = config.google_sa_file
    google_project = config.google_project

    def __init__(self):
        logging.debug("Initializing Datastore")
        if not config.serverless:
            self.credentials = service_account.Credentials.from_service_account_file(self.google_sa_file)
            self.ds_client = datastore.Client(credentials=self.credentials, project=self.google_project)
        else:
            self.ds_client = datastore.Client()
        self.memory_cache = pd.DataFrame()
        self.string_datastore = "[DATASTORE]"

    def return_memory(self):
        return self.memory_cache

    def build_entity(self, kind, name, elements):

        # Map is a dictionary
        """
        :param kind:
        :param name:
        :param elements:
        :return:

        Database kind:name
        { 'column1': 'value1',
          'column2': 'value2 }
        """

        logging.debug("{} Building an entity from Dictionary".format(self.string_datastore))
        kind_name = self.ds_client.key(kind, name)
        logging.debug("{} Key Index for entity is: {} - {}".format(
            self.string_datastore,
            kind,
            name
        ))
        entity = datastore.Entity(kind_name)
        for k, v in elements.items():
            entity[k] = v
        return entity

    def put(self, entity):
        logging.debug("{} Adding to Datastore".format(self.string_datastore))
        try:
            self.ds_client.put(entity)
        except Exception as error:
            logging.error(error)

    def put_many(self, list_of_entities):
        logging.debug("{} Adding Multiple Entities to Datastore".format(self.string_datastore))
        try:
            if len(list_of_entities) > 499:
                logging.warning("{} List is too long, it will be batched.".format(
                    self.string_datastore
                ))
                for entity_batch in utilities.batch(list_of_entities, 300):
                    self.ds_client.put_multi(entity_batch)
            else:
                logging.warning("{} List of entities will be inserted: {} elements.".format(
                    self.string_datastore,
                    len(list_of_entities)
                ))
                self.ds_client.put_multi(list_of_entities)
        except Exception as error:
            logging.error(error)

    def fetch_all(self, kind):
        query = self.ds_client.query(kind=kind)
        try:
            results = query.fetch()
            entities = []
            logging.debug("{} Building Dataframe for lookup.".format(
                self.string_datastore
            ))
            for lines in results:
                entities.append(lines)
            # Adding the key entity in the table
            for e in entities:  # go through entities
                print(e)
                print(e.key.name)
                print(e.key.kind)
                e['entity_key_name'] = e.key.name
                e[e.key.kind] = e.key.kind
            self.memory_cache = pd.DataFrame(entities)
        except Exception as error:
            logging.error("{} Couldn't fetch results. {}".format(
                self.string_datastore,
                error
            ))


class Mapper(Datastore):
    logging.debug("Mapper is being initialized")

    def __init__(self):
        super().__init__()
        self.mapper = pd.DataFrame()
        self.dict_schema = None
        self.dict_data = None
        # Internal built data
        self.primary_keys: list = []  # This is a list for primary keys.
        self.dict_cache = None
        self.columns_schema: list = []
        self.data_rows: list = []
        self.string_cache = "[CACHE]"

    def clean_objects(self):
        self.columns_schema: list = []
        self.data_rows: list = []
        self.dict_schema = None
        self.dict_data = None

    def cache(self, json_input: dict) -> bool:
        logging.info("{} Updating Cache".format(self.string_cache))
        # Cleaning objects
        self.clean_objects()
        try:
            logging.info("{} Getting schema".format(self.string_cache))
            # Getting Schema from Json
            self.dict_schema = json_input.get('schema')
            self.primary_keys = self.dict_schema.get('primaryKey')
            self.dict_data = json_input.get('data')

            logging.debug("{} Primary Keys are: {}".format(
                self.string_cache,
                self.primary_keys
            ))
            # Reading Schema
            for schema_keys in self.dict_schema.get('fields'):
                self.columns_schema.append(schema_keys['name'])

            logging.debug("{} Columns for Schema found: {}".format(
                self.string_cache,
                str(self.columns_schema)
            ))
        except Exception as error:
            logging.error("{} Schema couldn't be determine".format(
                self.string_cache
            ))
            logging.error(error)

        try:
            logging.info("{} Loading Cache Information".format(
                self.string_cache
            ))
            for schema_data in self.dict_data:
                # This is a list of tuples
                self.data_rows.append(self.rowing_processing(schema_data))
        except Exception as error:
            logging.error(error)

        try:
            logging.info("{} Building a Dataframe Table".format(
                self.string_cache
            ))
            self.build_table()
        except Exception as error:
            logging.error(error)

        return True

    def build_table(self):
        self.mapper = pd.DataFrame(
            columns=self.columns_schema,
            data=self.data_rows
        )
        # Dropping the duplicates in the memory cache
        self.mapper.drop_duplicates(inplace=True, subset=self.primary_keys)
        # Saving to google store with a made up Kind
        self.update_datastore()

    def update_datastore(self):
        logging.debug("{} Loading Entities for Datastore".format(self.string_cache))
        entities = []
        for index, row in self.mapper.iterrows():
            unique_dictionary = {}
            for columns in row.items():
                unique_dictionary[columns[0]] = columns[1]

            # This part is so in Datastore there is a staging phase to make testing
            if config.staging:
                logging.info("Working with Staging data")
                kind = self.primary_keys[0] + str("-staging")
            else:
                logging.info("Working with Production data")
                kind = self.primary_keys[0]

            name = unique_dictionary.pop(self.primary_keys[0])
            entities.append(super().build_entity(kind, name, unique_dictionary))

        super().put_many(list_of_entities=entities)

    def rowing_processing(self, schema_data_row) -> tuple:
        # Columns for Schema found: ['index', 'collectionCode', 'hash', 'tenant', 'thingType']
        organized_list: list = []
        for keys in self.columns_schema:
            key_matcher = schema_data_row.get(keys)
            organized_list.append(key_matcher)
        sorted_tuple = tuple(organized_list)
        return sorted_tuple


mapper = Mapper()


class Looker(Datastore):
    def __init__(self):
        self.parameters = None
        self.string_looker = "[LOOKER]"
        super().__init__()

    def check_memory(self, kind) -> bool:
        logging.debug("{} Looking if memory is ready".format(self.string_looker))
        if len(super().return_memory()) != 0:
            logging.debug("{} Mem is present. See if the kind is correct.".format(self.string_looker))
            if kind in list(self.memory_cache.columns):
                logging.debug("{} Kind is present".format(self.string_looker))
                return True
        else:
            logging.warning("No memory is loaded. Loading...")
            self.build_memory(kind)
            return True

    def build_memory(self, kind):
        logging.debug("{} Building Memory from kind: {}".format(
            self.string_looker,
            kind
        ))
        super().fetch_all(kind)

    def look_in_memory(self, kind, name):
        logging.debug("{} Looking for {} - {}".format(
            self.string_looker,
            kind,
            name
        ))
        result = self.memory_cache.loc[self.memory_cache['entity_key_name'] == name]
        return result.reset_index(drop=True).to_json(orient='records')


looker = Looker()
