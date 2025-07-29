import logging
import sys

from coin_sdk.common.config import Config


class MCConfig(Config):
    def __init__(self, base_uri, consumer_name, private_key_file, hmac_secret):
        super().__init__(base_uri, consumer_name, private_key_file, hmac_secret)
        self._base_uri = base_uri
        self._consumer_name = consumer_name
        self._private_key_file = private_key_file
        self._hmac_secret = hmac_secret

    @property
    def base_uri(self):
        return self._base_uri

    @property
    def api_url(self):
        return self._base_uri + '/mobile-connect/v3/discovery'

    @property
    def consumer_name(self):
        return self._consumer_name

    @property
    def private_key_file(self):
        return self._private_key_file

    @property
    def hmac_secret(self):
        return self._hmac_secret


_format = '%(asctime)s - %(name)-8s - %(levelname)s - %(message)s'


def set_logging(format=_format, level=logging.ERROR, stream=sys.stdout):
    logging.basicConfig(format=format, level=level, stream=stream)
