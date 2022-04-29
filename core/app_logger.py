import logging, sys, os
from fastapi import Request, Response
from http import HTTPStatus

status_reasons = {x.value: x.name for x in list(HTTPStatus)}
log = os.getenv('LOG_LEVEL', 'info').lower()
log_level = logging.INFO

if log == 'debug':
    log_level = logging.DEBUG
elif log == 'info':
    log_level = logging.INFO
elif log == 'warning':
    log_level = logging.WARNING
elif log == 'error':
    log_level = logging.ERROR
elif log == 'critical':
    log_level = logging.CRITICAL


def get_file_handler(formatter, log_filename):
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    return file_handler


def get_stream_handler(formatter):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name, formatter, log_filename="logfile.log"):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
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
