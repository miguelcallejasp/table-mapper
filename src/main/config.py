import logging
import os
import sys
from src.main.utils import utilities

# Logging Methods
log_level = os.getenv('LOG_LEVEL') if 'LOG_LEVEL' in os.environ else 'INFO'
level_attribute = utilities.guess_log(log_level)
logging.basicConfig(stream=sys.stdout, level=level_attribute,
                    format="%(asctime)-15s %(name)s [%(levelname)s] %(message)s")


flask_app_host = "0.0.0.0"
flask_app_port = "8080"