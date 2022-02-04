import json
import logging
import pandas as pd
import os
import sys
from src.main.utils import utilities

# Logging Methods
log_level = os.getenv('LOG_LEVEL') if 'LOG_LEVEL' in os.environ else 'DEBUG'
level_attribute = utilities.guess_log(log_level)
logging.basicConfig(stream=sys.stdout, level=level_attribute,
                    format="%(asctime)-15s %(name)s [%(levelname)s] %(message)s")


class Mapper(object):
    logging.debug("Mapper is being initialized")

    def __init__(self):
        mapper = pd.DataFrame()
        self.dict_schema = None
        self.dict_data = None
        # Internal built data
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
            self.dict_data = json_input.get('data')

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
                print(schema_data)
                tuple_rowed = self.rowing_processing(schema_data)

        except Exception as error:
            logging.error(error)
        return True

    def rowing_processing(self, schema_data_row) -> tuple:
        # Columns for Schema found: ['index', 'collectionCode', 'hash', 'tenant', 'thingType']
        organized_list: list = []
        for keys in self.columns_schema:
            key_matcher = schema_data_row.get(keys)
            organized_list.append(key_matcher)
        sorted_tuple = tuple(organized_list)
        return sorted_tuple


mapper = Mapper()
