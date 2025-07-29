import json
import logging
from abc import ABC, abstractmethod
from collections import namedtuple
from http import HTTPStatus
from json import JSONDecodeError
from typing import Callable

import requests
from requests import Response

from coin_sdk.common.securityservice import SecurityService

logger = logging.getLogger(__name__)


def _json_object_hook(d):
    return namedtuple('obj', d.keys())(*d.values())


def json2obj(data: str):
    try:
        return json.loads(data, object_hook=_json_object_hook)
    except JSONDecodeError:
        return data


class ErrorHandler(ABC):
    def handle_http_error(self, response: Response):
        logger.debug('Checking for errors')
        status = response.status_code
        logger.debug(f'Http Status: {status}')
        if status == HTTPStatus.OK:
            return
        description = HTTPStatus(status).description
        if status == HTTPStatus.BAD_GATEWAY or status == HTTPStatus.SERVICE_UNAVAILABLE or status == HTTPStatus.GATEWAY_TIMEOUT:
            self.on_connection_error(status, description, response)

        logger.error(f'Error: {response.text}')
        try:
            error_message = json2obj(response.text)
            error_object = self.error_message_to_object(error_message)
            if status == HTTPStatus.NOT_FOUND:
                self.on_not_found(error_object, response)
            raise requests.HTTPError(f'HTTP Status: {status}, {description}\n{str(error_object)}',
                                     response=error_object)
        except AttributeError:
            logger.error(response)
            self.on_other_error(status, description, response)

    @abstractmethod
    def error_message_to_object(self, error_message):
        pass

    @abstractmethod
    def on_connection_error(self, status: int, description: str, response: Response):
        pass

    @abstractmethod
    def on_not_found(self, error_object, response: Response):
        pass

    @abstractmethod
    def on_other_error(self, status: int, description: str, response: Response):
        pass


class RequestSender:
    def __init__(
            self,
            security_service: SecurityService,
            error_handler: ErrorHandler,
            object_parser=json2obj
    ):
        self._security_service = security_service
        self._error_handler = error_handler
        self._object_parser = object_parser

    def send_request(
            self,
            request: Callable[..., Response],
            url: str,
            json: dict[str, str]
    ):
        method = request.__name__
        headers = self._security_service.generate_headers(url, method, json)
        cookie = self._security_service.generate_jwt()
        logger.debug(f'Making request: {method}')
        response = request(url, json=json, headers=headers, cookies=cookie)
        logger.debug(f'Header: {response.request.headers}')
        logger.debug(f'Body: {response.request.body}')
        self._error_handler.handle_http_error(response)
        logger.debug('Converting JSON response to Python')
        response_json = self._object_parser(response.text)
        logger.debug(f'Response: {response_json}')
        return response_json