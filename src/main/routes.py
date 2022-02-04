import sys
import logging
from src.main.utils import Response
from src.main.model import Mapper
from flask import request
from flask import Blueprint
from flask import json

# Logging Configuration
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)-15s %(name)s - %(levelname)s - %(message)s")

# Controller Routes for API Endpoints
controller = Blueprint("Main Controller", __name__, url_prefix="/v1/mapper/")


@controller.route("/test", methods=['GET'])
def test():
    return Response.response("This is a test response", 200)


@controller.route("/update", methods=['POST'])
def update():
    logging.info("Updating Map")
    success_update = Mapper.cache(request.json)
    if success_update:
        return Response.response("This is a working progress", 200)
    else:
        return Response.response("Something went wrong", 500)
    #Mapper.update()