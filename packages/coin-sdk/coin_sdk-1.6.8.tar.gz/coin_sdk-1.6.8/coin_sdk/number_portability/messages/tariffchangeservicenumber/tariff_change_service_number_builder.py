from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import HeaderCreator, NumberSeries
from coin_sdk.number_portability.messages.message import Message
from .tariff_change_service_number import TariffChangeServiceNumber
from .tariff_change_service_number_seq import TariffChangeServiceNumberSeq
from .tariff_change_service_number_repeats import  TariffChangeServiceNumberRepeats
from .tariff_change_service_number_body import TariffChangeServiceNumberBody
from .tariff_change_service_number_message import  TariffChangeServiceNumberMessage
from ..tariffchangeservicenumber.tariff_info import TariffInfo


class TariffChangeServiceNumberBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._platformprovider = None
        self._planneddatetime = None
        self._dossierid = None
        self._note = None
        self._tariffChangeServiceNumber_seqs = []

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

    def add_tariffChangeServiceNumber_seq(self):
        return TariffChangeServiceNumberRepeatsBuilder(self)

    def build(self):
        repeats = [TariffChangeServiceNumberRepeats(seq) for seq in self._tariffChangeServiceNumber_seqs]
        tariffChangeServiceNumber = TariffChangeServiceNumber(
            self._dossierid,
            self._platformprovider,
            self._planneddatetime,
            repeats
        )
        body = TariffChangeServiceNumberBody(tariffChangeServiceNumber)
        message = TariffChangeServiceNumberMessage(self._header, body)
        return Message(message, MessageType.TARIFF_CHANGE_SERVICE_NUMBER_V3)


class TariffChangeServiceNumberRepeatsBuilder():
    def __init__(self, tariffChangeServiceNumber_builder: TariffChangeServiceNumberBuilder):
        super().__init__()
        self._tariffChangeServiceNumber_builder = tariffChangeServiceNumber_builder
        self._pop = None
        self._number_series = None
        self._tariff_info = None

    def set_number_series(self, start: str, end: str):
        self._number_series = NumberSeries(start, end)
        return self

    def set_tariff_info(self, peak: str, offPeak: str, currency: str, type: str, vat: str):
        tariffInfo = TariffInfo(peak, offPeak, currency, type, vat)
        self._tariff_info = tariffInfo
        return self

    def finish(self):
        seq = TariffChangeServiceNumberSeq(self._number_series, self._tariff_info)
        self._tariffChangeServiceNumber_builder._tariffChangeServiceNumber_seqs.append(seq)
        return self._tariffChangeServiceNumber_builder
