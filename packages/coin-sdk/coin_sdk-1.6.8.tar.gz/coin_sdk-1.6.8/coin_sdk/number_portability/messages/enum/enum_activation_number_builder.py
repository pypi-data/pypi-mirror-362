from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import CustomerInfo, EnumRepeatsBuilder, HeaderCreator
from coin_sdk.number_portability.messages.enum.enum_content import EnumContent
from coin_sdk.number_portability.messages.message import Message
from .enum_activation_number_body import EnumActivationNumberBody
from .enum_activation_number_message import EnumActivationNumberMessage
from .enum_number_repeats import EnumNumberRepeats
from .enum_number_seq import EnumNumberSeq


class EnumActivationNumberBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._dossierid = None
        self._currentnetworkoperator = None
        self._typeofnumber = None
        self._enum_activation_number_seqs = []

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_currentnetworkoperator(self, currentnetworkoperator: str):
        self._currentnetworkoperator = currentnetworkoperator
        return self

    def set_typeofnumber(self, typeofnumber: str):
        self._typeofnumber = typeofnumber
        return self

    def add_enum_activation_number_seq(self):
        return EnumActivationNumberRepeatsBuilder(self)

    def build(self):
        repeats = [EnumNumberRepeats(seq) for seq in self._enum_activation_number_seqs]
        enum_activation_number = EnumContent(
            self._dossierid,
            self._currentnetworkoperator,
            self._typeofnumber,
            repeats
        )
        body = EnumActivationNumberBody(enum_activation_number)
        message = EnumActivationNumberMessage(self._header, body)
        return Message(message, MessageType.ENUM_ACTIVATION_NUMBER_V3)


class EnumActivationNumberRepeatsBuilder(EnumRepeatsBuilder):
    def __init__(self, enum_activation_number_builder: EnumActivationNumberBuilder):
        super().__init__()
        self._enum_activation_number_builder = enum_activation_number_builder

    def set_number_series(self, start: str, end: str):
        self._set_number_series(start, end)
        return self

    def add_enum_profiles(self, *profileids):
        self._add_enum_prof_seq(*profileids)
        return self

    def finish(self):
        seq = EnumNumberSeq(self._number_series, self._enum_repeats)
        self._enum_activation_number_builder._enum_activation_number_seqs.append(seq)
        return self._enum_activation_number_builder
