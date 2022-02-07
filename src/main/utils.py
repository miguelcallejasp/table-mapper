import logging
import requests
from urllib.parse import urlsplit
from flask import jsonify


class Response(object):
    def __init__(self, message, status_code):
        self.status_code = status_code
        self.message = message

    @staticmethod
    def response(message, status_code):
        return jsonify(message=message,
                       status=status_code), status_code


class Utils(object):
    def method_to_request(self, method):
        """Dispatch method"""
        method_function = method.lower() + "_method"
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_function, lambda: "Invalid Method")
        # Call the method as we return it
        return method()

    @staticmethod
    def batch(iterable, n=1):
        total_length = len(iterable)
        for ndx in range(0, total_length, n):
            yield iterable[ndx:min(ndx + n, total_length)]

    @staticmethod
    def get_method():
        return requests.get

    @staticmethod
    def post_method():
        return requests.post

    @staticmethod
    def put_method():
        return requests.put

    @staticmethod
    def url_handler(uri):
        return urlsplit(uri)

    @staticmethod
    def guess_log(log):

        if log == 'CRITICAL':
            level_attribute = logging.CRITICAL
        else:
            pass
        if log == 'WARNING':
            level_attribute = logging.WARNING
        else:
            pass
        if log == 'ERROR':
            level_attribute = logging.ERROR
        else:
            pass
        if log == 'INFO':
            level_attribute = logging.INFO
        else:
            pass
        if log == 'DEBUG':
            level_attribute = logging.DEBUG
        else:
            pass

        return level_attribute


utilities = Utils()
