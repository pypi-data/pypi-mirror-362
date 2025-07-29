from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import HeaderCreator, NumberSeries
from coin_sdk.number_portability.messages.message import Message
from .deactivation_service_number import DeactivationServiceNumber
from .deactivation_service_number_seq import DeactivationServiceNumberSeq
from .deactivation_service_number_repeats import  DeactivationServiceNumberRepeats
from .deactivation_service_number_body import DeactivationServiceNumberBody
from .deactivation_service_number_message import  DeactivationServiceNumberMessage
from ..tariffchangeservicenumber.tariff_info import TariffInfo


class DeactivationServiceNumberBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._platformprovider = None
        self._planneddatetime = None
        self._dossierid = None
        self._note = None
        self._deactivationServiceNumber_seqs = []

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_platformprovider(self, platformprovider: str):
        self._platformprovider = platformprovider
        return self

    def set_planneddatetime(self, planneddatetime: str):
        self._planneddatetime = planneddatetime
        return self

    def add_deactivationServiceNumber_seq(self):
        return DeactivationServiceNumberRepeatsBuilder(self)

    def build(self):
        repeats = [DeactivationServiceNumberRepeats(seq) for seq in self._deactivationServiceNumber_seqs]
        deactivationServiceNumber = DeactivationServiceNumber(
            self._dossierid,
            self._platformprovider,
            self._planneddatetime,
            repeats
        )
        body = DeactivationServiceNumberBody(deactivationServiceNumber)
        message = DeactivationServiceNumberMessage(self._header, body)
        return Message(message, MessageType.DEACTIVATION_SERVICE_NUMBER_V3)


class DeactivationServiceNumberRepeatsBuilder():
    def __init__(self, deactivationServiceNumber_builder: DeactivationServiceNumberBuilder):
        super().__init__()
        self._deactivationServiceNumber_builder = deactivationServiceNumber_builder
        self._pop = None
        self._number_series = None
        self._tariff_info = None

    def set_number_series(self, start: str, end: str):
        self._number_series = NumberSeries(start, end)
        return self

    def set_pop(self, pop: str):
        self._pop = pop
        return self

    def finish(self):
        seq = DeactivationServiceNumberSeq(self._number_series, self._pop)
        self._deactivationServiceNumber_builder._deactivationServiceNumber_seqs.append(seq)
        return self._deactivationServiceNumber_builder
