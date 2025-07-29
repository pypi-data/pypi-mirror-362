import json
import logging
from http import HTTPStatus

import requests
from requests import Response, RequestException

from coin_sdk.common.securityservice import SecurityService
from coin_sdk.common.sendrequest import json2obj, RequestSender, ErrorHandler
from coin_sdk.mobile_connect.v3.mcconfig import MCConfig
from coin_sdk.mobile_connect.v3.domain.discovery_request import DiscoveryRequestV3
from coin_sdk.mobile_connect.v3.domain.discovery_response import DiscoveryResponseV3
from coin_sdk.mobile_connect.v3.domain.error_body import ErrorBody
from coin_sdk.mobile_connect.v3.domain.link import LinkDto
from coin_sdk.mobile_connect.v3.domain.supported_services import SupportedServicesDto

logger = logging.getLogger(__name__)


class DiscoveryRequestNoResultException(RequestException):
    """Discovery request did not yield any results"""

class DiscoveryRequestErrorHandler(ErrorHandler):

    def error_message_to_object(self, error_message):
        return ErrorBody(error_message.error, error_message.description, error_message.correlation_id)

    def on_connection_error(self, status: int, description: str, response: Response):
        raise requests.ConnectionError(f'HTTP Status: {status}, {description}', response=response)

    def on_not_found(self, error_object, response: Response):
        raise DiscoveryRequestNoResultException(f'HTTP Status: {HTTPStatus.NOT_FOUND}, {HTTPStatus.NOT_FOUND.description}', response=error_object)

    def on_other_error(self, status: int, description: str, response: Response):
        raise requests.HTTPError(f'HTTP Status: {status}, {description}', response=response)


def json_to_discovery_response_v3(json: dict[str, ...]):
    try:
        return DiscoveryResponseV3(**json) if 'supportedServices' in json else \
            SupportedServicesDto(**json) if 'accountTakeoverProtection' in json else LinkDto(**json)
    except AttributeError:
        return json2obj(json)


def discovery_response_parser(response: str) -> DiscoveryResponseV3:
    return json.loads(response, object_hook=json_to_discovery_response_v3)


class Sender:
    def __init__(self, config: MCConfig, error_handler=DiscoveryRequestErrorHandler()):
        self._config = config
        self._request_sender = RequestSender(
            security_service=SecurityService(config),
            error_handler=error_handler,
            object_parser=discovery_response_parser
        )

    def send_discovery_request(self, msisdn: str, correlation_id: str=None) -> DiscoveryResponseV3 | None:
        discovery_request = DiscoveryRequestV3(msisdn=msisdn, correlation_id=correlation_id)
        logger.info(f'Sending discovery request: {discovery_request}')
        message_dict = discovery_request.to_dict()
        try:
            return self._request_sender.send_request(requests.post, self._config.api_url, message_dict)
        except DiscoveryRequestNoResultException:
            return None
