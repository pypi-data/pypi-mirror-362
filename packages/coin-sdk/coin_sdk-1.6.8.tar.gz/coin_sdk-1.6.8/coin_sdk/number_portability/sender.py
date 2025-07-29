import logging

import requests

from coin_sdk.common.securityservice import SecurityService
from coin_sdk.common.sendrequest import RequestSender
from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.message_response import MessageResponse
from coin_sdk.number_portability.npconfig import NpConfig
from coin_sdk.number_portability.utils import NumberPortabilityErrorHandler

logger = logging.getLogger(__name__)


class Sender:
    def __init__(self, config: NpConfig, error_handler=NumberPortabilityErrorHandler()):
        self._config = config
        self._request_sender = RequestSender(security_service=SecurityService(config), error_handler=error_handler)

    def _send_request(self, request, url, json):
        response_json = self._request_sender.send_request(request, url, json)
        try:
            return MessageResponse(response_json.transaction_id)
        except AttributeError:
            return response_json

    def send_message(self, message):
        logger.info(f'Sending message: {message}')
        message_type = message.get_message_type()
        message_dict = message.to_dict()
        url = f'{self._config.api_url}/{message_type.value}'
        logger.debug(f'url: {url}')
        return self._send_request(requests.post, url, message_dict)

    def confirm(self, transaction_id):
        logger.info(f'Sending confirmation for id: {transaction_id}')
        url = f'{self._config.api_url}/{MessageType.CONFIRMATION_V3.value}/{transaction_id}'
        logger.debug(f'url: {url}')
        json = {'transactionId': transaction_id}
        return self._send_request(requests.put, url, json)
