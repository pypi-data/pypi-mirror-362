import logging
import sys


class Config:
    def __init__(self, base_uri, consumer_name, private_key_file=None, hmac_secret=None, private_key_mem=None,
                 shared_key=None):
        assert private_key_file or private_key_mem, "either private_key_file or private_key_mem should be present"
        assert hmac_secret or shared_key, "either hmac_secret or shared_key should be present"
        self._base_uri = base_uri
        self._consumer_name = consumer_name
        self._private_key_file = private_key_file
        self._hmac_secret = hmac_secret
        self._private_key_mem = private_key_mem
        self._shared_key = shared_key

    @property
    def base_uri(self):
        return self._base_uri

    @property
    def consumer_name(self):
        return self._consumer_name

    @property
    def private_key_file(self):
        return self._private_key_file

    @property
    def hmac_secret(self):
        return self._hmac_secret

    @property
    def shared_key(self):
        return self._shared_key

    @property
    def private_key_mem(self):
        return self._private_key_mem


_format = '%(asctime)s - %(name)-8s - %(levelname)s - %(message)s'


def set_logging(format=_format, level=logging.ERROR, stream=sys.stdout):
    logging.basicConfig(format=format, level=level, stream=stream)
