from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import CustomerInfo, EnumRepeatsBuilder, HeaderCreator
from coin_sdk.number_portability.messages.enum.enum_content import EnumContent
from coin_sdk.number_portability.messages.message import Message
from .enum_deactivation_number_body import EnumDeactivationNumberBody
from .enum_deactivation_number_message import EnumDeactivationNumberMessage
from .enum_number_repeats import EnumNumberRepeats
from .enum_number_seq import EnumNumberSeq


class EnumDeactivationNumberBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._dossierid = None
        self._currentnetworkoperator = None
        self._typeofnumber = None
        self._enum_deactivation_number_seqs = []

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_currentnetworkoperator(self, currentnetworkoperator: str):
        self._currentnetworkoperator = currentnetworkoperator
        return self

    def set_typeofnumber(self, typeofnumber: str):
        self._typeofnumber = typeofnumber
        return self

    def add_enum_deactivation_number_seq(self):
        return EnumDeactivationNumberRepeatsBuilder(self)

    def build(self):
        repeats = [EnumNumberRepeats(seq) for seq in self._enum_deactivation_number_seqs]
        enum_deactivation_number = EnumContent(
            self._dossierid,
            self._currentnetworkoperator,
            self._typeofnumber,
            repeats
        )
        body = EnumDeactivationNumberBody(enum_deactivation_number)
        message = EnumDeactivationNumberMessage(self._header, body)
        return Message(message, MessageType.ENUM_DEACTIVATION_NUMBER_V3)


class EnumDeactivationNumberRepeatsBuilder(EnumRepeatsBuilder):
    def __init__(self, enum_deactivation_number_builder: EnumDeactivationNumberBuilder):
        super().__init__()
        self._enum_deactivation_number_builder = enum_deactivation_number_builder

    def set_number_series(self, start: str, end: str):
        self._set_number_series(start, end)
        return self

    def add_enum_profiles(self, *profileids):
        self._add_enum_prof_seq(*profileids)
        return self

    def finish(self):
        seq = EnumNumberSeq(self._number_series, self._enum_repeats)
        self._enum_deactivation_number_builder._enum_deactivation_number_seqs.append(seq)
        return self._enum_deactivation_number_builder
