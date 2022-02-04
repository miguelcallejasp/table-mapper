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
        self.dict_cache = None
        self.dict_schema = None
        self.columns_schema: list = []
        self.data_rows: list = []
        self.string_cache = "[CACHE]"

    def cache(self, json_input: dict) -> bool:
        logging.info("{} Updating Cache".format(self.string_cache))
        try:
            logging.info("{} Getting schema".format(self.string_cache))
            # Getting Schema from Json
            self.dict_schema = json_input.get('schema')
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
            for schema_data

        return True


mapper = Mapper()
