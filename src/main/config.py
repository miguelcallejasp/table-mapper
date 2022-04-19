import logging
import os
import sys
from src.main.utils import utilities

# Logging Methods
log_level = os.getenv('LOG_LEVEL') if 'LOG_LEVEL' in os.environ else 'DEBUG'
level_attribute = utilities.guess_log(log_level)
logging.basicConfig(stream=sys.stdout, level=level_attribute,
                    format="%(asctime)-15s %(name)s [%(levelname)s] %(message)s")


flask_app_host = "0.0.0.0"
flask_app_port = "8081"
google_sa_file = "/Users/miguelcallejas/Documents/Engineering/Personal/table-mapper/resources/db-mapper-sa.json"
google_project = "devops-db-resources"
serverless = True
staging = False
