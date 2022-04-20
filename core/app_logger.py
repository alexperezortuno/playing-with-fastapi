import logging, sys
from fastapi import Request, Response
from http import HTTPStatus
status_reasons = {x.value:x.name for x in list(HTTPStatus)}


def get_file_handler(formatter, log_filename):
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    return file_handler


def get_stream_handler(formatter):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name, formatter, log_filename = "logfile.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(formatter, log_filename))
    logger.addHandler(get_stream_handler(formatter))
    return logger


def get_extra_info(request: Request, response: Response):
    return {'req': {
        'url': request.url.path,
        'headers': {'host': request.headers['host'],
                    'user-agent': request.headers['user-agent'],
                    'accept': request.headers['accept']},
        'method': request.method,
        'httpVersion': request.scope['http_version'],
        'originalUrl': request.url.path,
        'query': {}
        },
        'res': {'statusCode': response.status_code, 'body': {'statusCode': response.status_code,
                   'status': status_reasons.get(response.status_code)}}}
