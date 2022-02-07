import sys
import logging
from src.main.utils import Response
from src.main.model import mapper
from src.main.model import looker
from flask import request
from flask import Blueprint
from flask import json

# Logging Configuration
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)-15s %(name)s - %(levelname)s - %(message)s")

# Controller Routes for API Endpoints
controller = Blueprint("Main Controller", __name__, url_prefix="/v1/mapper/")


@controller.route("/test", methods=['GET'])
def test():
    return Response.response("This is a test response", 200)


@controller.route("/update", methods=['POST'])
def update():
    logging.info("Updating Map")
    # print(type(request.json))
    success_update = mapper.cache(request.json)
    if success_update:
        return Response.response("This is a working progress", 200)
    else:
        return Response.response("Something went wrong", 500)
    # Mapper.update()


@controller.route("/search", methods=['GET'])
def search():
    logging.info("Getting Info")
    print(request.args.to_dict())
    search_fields = request.args.to_dict()

    success_update = True
    kind = list(search_fields.keys())[0]
    values = list(search_fields.values())[0]

    memory_ready = looker.check_memory(kind)
    if memory_ready:
        response = looker.look_in_memory(kind, values)
        print(response)
    else:
        looker.build_memory(kind)
        response = looker.look_in_memory(kind, values)
        print(response)

    if response:
        return Response.response(json.loads(response), 200)
    else:
        return Response.response("Something went wrong", 500)
    # Mapper.update()
