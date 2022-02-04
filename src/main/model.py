import json
import logging
import pandas as pd

class Mapper(object):
    logging.debug("Mapper is being initialized")
    def __init__(self):
        mapper = pd.DataFrame()
        self.dict_cache = None
        self.string_cache = "[CACHE]"

    def cache(self, json_dict: dict):
        logging.info("{} Updating Cache".format(self.string_cache))
        try:
            logging.info("{} Getting schema".format(self.string_cache))
