from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import HeaderCreator, NumberSeries
from coin_sdk.number_portability.messages.message import Message
from .activation_service_number import ActivationServiceNumber
from .activation_service_number_seq import ActivationServiceNumberSeq
from .activation_service_number_repeats import  ActivationServiceNumberRepeats
from .activation_service_number_body import ActivationServiceNumberBody
from .activation_service_number_message import  ActivationServiceNumberMessage
from ..tariffchangeservicenumber.tariff_info import TariffInfo


class ActivationServiceNumberBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._platformprovider = None
        self._planneddatetime = None
        self._dossierid = None
        self._note = None
        self._activationServiceNumber_seqs = []

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_platformprovider(self, platformprovider: str):
        self._platformprovider = platformprovider
        return self

    def set_planneddatetime(self, planneddatetime: str):
        self._planneddatetime = planneddatetime
        return self

    def set_note(self, note: str):
        self._note = note
        return self

    def add_activationServiceNumber_seq(self):
        return ActivationServiceNumberRepeatsBuilder(self)

    def build(self):
        repeats = [ActivationServiceNumberRepeats(seq) for seq in self._activationServiceNumber_seqs]
        activationServiceNumber = ActivationServiceNumber(
            self._dossierid,
            self._platformprovider,
            self._planneddatetime,
            self._note,
            repeats
        )
        body = ActivationServiceNumberBody(activationServiceNumber)
        message = ActivationServiceNumberMessage(self._header, body)
        return Message(message, MessageType.ACTIVATION_SERVICE_NUMBER_V3)


class ActivationServiceNumberRepeatsBuilder():
    def __init__(self, activationServiceNumber_builder: ActivationServiceNumberBuilder):
        super().__init__()
        self._activationServiceNumber_builder = activationServiceNumber_builder
        self._pop = None
        self._number_series = None
        self._tariff_info = None

    def set_number_series(self, start: str, end: str):
        self._number_series = NumberSeries(start, end)
        return self

    def set_pop(self, pop: str):
        self._pop = pop
        return self

    def set_tariff_info(self, peak: str, offPeak: str, currency: str, type: str, vat: str):
        tariffInfo = TariffInfo(peak, offPeak, currency, type, vat)
        self._tariff_info = tariffInfo
        return self

    def finish(self):
        seq = ActivationServiceNumberSeq(self._number_series, self._tariff_info, self._pop)
        self._activationServiceNumber_builder._activationServiceNumber_seqs.append(seq)
        return self._activationServiceNumber_builder
