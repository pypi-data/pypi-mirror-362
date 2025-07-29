import os
import random
import unittest

from requests import HTTPError

from coin_sdk.number_portability.domain import ConfirmationStatus
from coin_sdk.number_portability.messages.activationservicenumber import ActivationServiceNumberBuilder
from coin_sdk.number_portability.messages.cancel import CancelBuilder
from coin_sdk.number_portability.messages.deactivation import DeactivationBuilder
from coin_sdk.number_portability.messages.deactivationservicenumber.deactivation_service_number_builder import \
    DeactivationServiceNumberBuilder
from coin_sdk.number_portability.messages.enum import EnumActivationNumberBuilder, EnumDeactivationNumberBuilder, \
    EnumProfileActivationBuilder, EnumProfileDeactivationBuilder
from coin_sdk.number_portability.messages.enum.enum_activation_operator_builder import EnumActivationOperatorBuilder
from coin_sdk.number_portability.messages.enum.enum_deactivation_operator_builder import EnumDeactivationOperatorBuilder
from coin_sdk.number_portability.messages.portingperformed import PortingPerformedBuilder
from coin_sdk.number_portability.messages.portingrequest import PortingRequestBuilder
from coin_sdk.number_portability.messages.portingrequest.porting_request_builder import ContractType
from coin_sdk.number_portability.messages.portingrequestanswer import PortingRequestAnswerBuilder
from coin_sdk.number_portability.messages.portingrequestanswerdelayed import PortingRequestAnswerDelayedBuilder
from coin_sdk.number_portability.messages.tariffchangeservicenumber.tariff_change_service_number_builder import \
    TariffChangeServiceNumberBuilder
from coin_sdk.number_portability.npconfig import NpConfig
from coin_sdk.number_portability.receiver import Receiver, OffsetPersister
from coin_sdk.number_portability.sender import Sender

config = NpConfig(
    os.getenv('CRDB_REST_BACKEND', 'http://0.0.0.0:8000'),
    'loadtest-loada',
    private_key_file='./test/setup/private-key.pem',
    hmac_secret='./test/setup/sharedkey.encrypted'
)

sender = Sender(config)


class ExamplesTest(unittest.TestCase):

    def test_porting_request(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_request = (
            PortingRequestBuilder()
            .set_dossierid(dossier_id)
            .set_recipientnetworkoperator('LOADB')
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_contract(ContractType.CONTINUATION)
            .add_porting_request_seq()
                .set_number_series('0612345678', '0612345678')
                .finish()
            .add_porting_request_seq()
                .set_number_series('0612345678', '0612345678')
                .add_enum_profiles('PROF1', 'PROF2')
                .finish()
            .set_customerinfo("test", "test bv", "1", "a", "1234AB", "1")
            .build()
        )
        result = sender.send_message(porting_request)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_cancel(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        cancel = CancelBuilder() \
            .set_dossierid(dossier_id) \
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB') \
            .build()
        result = sender.send_message(cancel)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_deactivation(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        deactivation = (
            DeactivationBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_originalnetworkoperator('LOADA')
            .add_deactivation_seq()
                .set_number_series('0612345678', '0612345678')
                .finish()
            .build()
        )
        result = sender.send_message(deactivation)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_porting_performed(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_performed = (
            PortingPerformedBuilder()
            .set_header('LOADA', 'LOADB')
            .set_dossierid(dossier_id)
            .set_donornetworkoperator('LOADB')
            .set_recipientnetworkoperator('LOADA')
            .add_porting_performed_seq()
                .set_number_series('0612345678', '0612345678')
                .finish()
            .add_porting_performed_seq()
                .set_number_series('0612345678', '0612345678')
                .add_enum_profiles('PROF1', 'PROF2')
                .finish()
            .build()
        )
        result = sender.send_message(porting_performed)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_porting_request_answer(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_performed_answer = (
            PortingRequestAnswerBuilder()
            .set_header('LOADA', 'LOADB')
            .set_dossierid(dossier_id)
            .set_blocking('N')
            .add_porting_request_answer_seq()
                .set_donornetworkoperator('LOADA')
                .set_donorserviceprovider('LOADA')
                .set_firstpossibledate('20190101120000')
                .set_number_series('0612345678', '0612345678')
                .set_note('This is a note')
                .set_blockingcode('99')
                .finish()
            .add_porting_request_answer_seq()
                .set_donornetworkoperator('LOADA')
                .set_donorserviceprovider('LOADA')
                .set_firstpossibledate('20190101120000')
                .set_number_series('0612345678', '0612345678')
                .set_note('This is a note')
                .set_blockingcode('99')
                .finish()
            .build()
        )
        result = sender.send_message(porting_performed_answer)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_porting_request_answer_delayed(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_request_answer_delayed = (
            PortingRequestAnswerDelayedBuilder()
            .set_header('LOADA', 'LOADB')
            .set_dossierid(dossier_id)
            .set_donornetworkoperator('LOADB')
            .build()
        )
        result = sender.send_message(porting_request_answer_delayed)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_send_error(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_request_answer_delayed = (
            PortingRequestAnswerDelayedBuilder()
                .set_header('LOADA', 'LOADA')
                .set_dossierid(dossier_id)
                .set_donornetworkoperator('LOADB')
                .build()
        )
        try:
            sender.send_message(porting_request_answer_delayed)
        except HTTPError as e:
            print(e)

    def test_activationsn(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        activationsn = (
            ActivationServiceNumberBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_platformprovider('LOADB')
            .set_planneddatetime("20190101121212")
            .set_note("A Note")
            .add_activationServiceNumber_seq()
                .set_number_series('0612345678', '0612345678')
                .set_tariff_info("1023,00", "1023,00", "1", "2", "3")
                .set_pop("Test")
                .finish()
            .build()
        )
        result = sender.send_message(activationsn)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_deactivationsn(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        deactivationsn = (
            DeactivationServiceNumberBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_platformprovider('LOADB')
            .set_planneddatetime("20190101121212")
            .add_deactivationServiceNumber_seq()
                .set_number_series('0612345678', '0612345678')
                .set_pop("Test")
                .finish()
            .build()
        )
        result = sender.send_message(deactivationsn)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_tariffchangesn(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        tariffchangesn = (
            TariffChangeServiceNumberBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_platformprovider('LOADB')
            .set_planneddatetime("20190101121212")
            .add_tariffChangeServiceNumber_seq()
                .set_number_series('0612345678', '0612345678')
                .set_tariff_info("1023,00", "1023,00", "1", "2", "3")
                .finish()
            .build()
        )
        result = sender.send_message(tariffchangesn)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_enumactivationnumber(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        enumactivationnumber = (
            EnumActivationNumberBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_typeofnumber("1")
            .add_enum_activation_number_seq()
                .set_number_series('0612345678', '0612345678')
                .add_enum_profiles("PROF1", "PROF2")
                .finish()
            .build()
        )
        result = sender.send_message(enumactivationnumber)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_enumdeactivationnumber(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        enumdeactivationnumber = (
            EnumDeactivationNumberBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_typeofnumber("1")
            .add_enum_deactivation_number_seq()
                .set_number_series('0612345678', '0612345678')
                .add_enum_profiles("PROF1", "PROF2")
                .finish()
            .build()
        )
        result = sender.send_message(enumdeactivationnumber)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_enumactivationoperator(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        enumactivationoperator = (
            EnumActivationOperatorBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_typeofnumber("1")
            .add_enum_activation_operator_seq()
                .set_profileid("PROF-12")
                .set_default_service("Y")
                .finish()
            .build()
        )
        result = sender.send_message(enumactivationoperator)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_enumdeactivationoperator(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        enumdeactivationoperator = (
            EnumDeactivationOperatorBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_typeofnumber("1")
            .add_enum_deactivation_operator_seq()
                .set_profileid("PROF-12")
                .set_default_service("Y")
                .finish()
            .build()
        )
        result = sender.send_message(enumdeactivationoperator)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_enumprofileactivation(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        enumprofileactivation = (
            EnumProfileActivationBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_typeofnumber("3")
            .set_scope("SCOPE-123")
            .set_profileid("5879AF-GNU9480N")
            .set_ttl("7")
            .set_dnsclass("abc def")
            .set_rectype("uvw xyz")
            .set_order("13")
            .set_preference("13")
            .set_flags("abc, def")
            .set_enumservice("Enum Service 123")
            .set_regexp("[A-Z][a-z]+\\\\d")
            .set_usertag("tag123123kjkjk")
            .set_domain("domain123")
            .set_spcode("23kjkj324")
            .set_processtype("processTypeX")
            .set_gateway("6i3k")
            .set_service("sdf sdfdsf")
            .set_domaintag("fdksalfds2132")
            .set_replacement("sdf dsjhsfd sdfsfd")
            .build()
        )
        result = sender.send_message(enumprofileactivation)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId");

    def test_enumprofiledeactivation(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        enumprofiledeactivation = (
            EnumProfileDeactivationBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_typeofnumber("1")
            .set_profileid("PROF-12")
            .build()
        )
        result = sender.send_message(enumprofiledeactivation)
        self.assertRegex(result[0], "[0-9a-z]{30,40}", "Should match the transactionId")

    def test_receive_message(self):
        TestReceiver(config).start_stream(confirmation_status=ConfirmationStatus.ALL, offset_persister=TestOffsetPersister)

    @staticmethod
    def _generate_random_dossier_id(operator: str):
        random_int = random.randint(10000, 99999)
        return f'{operator}-{random_int}'


class TestReceiver(Receiver):
    def on_keep_alive(self):
        pass

    def on_porting_request(self, message_id, message):
        print('porting request')
        self.handle_message(message_id, message)

    def on_porting_request_answer(self, message_id, message):
        print('porting request answer')
        self.handle_message(message_id, message)

    def on_porting_request_answer_delayed(self, message_id, message):
        print('porting request answer delayed')
        self.handle_message(message_id, message)

    def on_porting_performed(self, message_id, message):
        print('porting performed')
        self.handle_message(message_id, message)

    def on_deactivation(self, message_id, message):
        print('deactivation')
        self.handle_message(message_id, message)

    def on_cancel(self, message_id, message):
        print('cancel')
        self.handle_message(message_id, message)

    def on_activation_service_number(self, message_id, message):
        print('activation service number')
        self.handle_message(message_id, message)

    def on_deactivation_service_number(self, message_id, message):
        print('deactivation service number')
        self.handle_message(message_id, message)

    def on_tariff_change_service_number(self, message_id, message):
        print('tariff change service number')
        self.handle_message(message_id, message)

    def on_range_activation(self, message_id, message):
        print('range activation')
        self.handle_message(message_id, message)

    def on_range_deactivation(self, message_id, message):
        print('range deactivation')
        self.handle_message(message_id, message)

    def on_enum_activation_number(self, message_id, message):
        print('enum activation number')
        self.handle_message(message_id, message)

    def on_enum_activation_range(self, message_id, message):
        print('enum activation number')
        self.handle_message(message_id, message)

    def on_enum_activation_operator(self, message_id, message):
        print('enum activation number')
        self.handle_message(message_id, message)

    def on_enum_deactivation_number(self, message_id, message):
        print('enum deactivation number')
        self.handle_message(message_id, message)

    def on_enum_deactivation_range(self, message_id, message):
        print('enum deactivation number')
        self.handle_message(message_id, message)

    def on_enum_deactivation_operator(self, message_id, message):
        print('enum deactivation number')
        self.handle_message(message_id, message)

    def on_enum_profile_activation(self, message_id, message):
        print('enum activation profile')
        self.handle_message(message_id, message)

    def on_enum_profile_deactivation(self, message_id, message):
        print('enum deactivation profile')
        self.handle_message(message_id, message)

    def on_error_found(self, message_id, message):
        print('error!')
        self.handle_message(message_id, message)
        self.stop()

    def handle_message(self, message_id, message):
        print(message)
        sender.confirm(message_id)


class TestOffsetPersister(OffsetPersister):
    def __init__(self):
        self._offset = -1

    def get_persisted_offset(self):
        return self._offset

    def persist_offset(self, offset):
        self._offset = offset


if __name__ == '__main__':
    unittest.main()
