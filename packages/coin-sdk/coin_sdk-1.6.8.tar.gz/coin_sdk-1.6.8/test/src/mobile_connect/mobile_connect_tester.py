import os
import unittest

from coin_sdk.mobile_connect.v3.mcconfig import MCConfig
from coin_sdk.mobile_connect.v3.domain.error_body import ErrorBody
from coin_sdk.mobile_connect.v3.sender import Sender

config = MCConfig(
    os.getenv('CRDB_REST_BACKEND', 'http://0.0.0.0:8000'),
    'loadtest-loada',
    private_key_file='./test/setup/private-key.pem',
    hmac_secret='./test/setup/sharedkey.encrypted'
)

sender = Sender(config)


class MobileConnectTest(unittest.TestCase):

    def test_discovery_request(self):
        response = sender.send_discovery_request(msisdn='123456789')
        self.assertIsNotNone(response)

    def test_discovery_request_not_found(self):
        response = sender.send_discovery_request(msisdn='123456789', correlation_id='404')
        self.assertIsNone(response)

    def test_discovery_request_other_error(self):
        with self.assertRaises(Exception) as context:
            sender.send_discovery_request(msisdn='123456789', correlation_id='403')
        self.assertIsInstance(context.exception.response, ErrorBody)

if __name__ == '__main__':
    unittest.main()
