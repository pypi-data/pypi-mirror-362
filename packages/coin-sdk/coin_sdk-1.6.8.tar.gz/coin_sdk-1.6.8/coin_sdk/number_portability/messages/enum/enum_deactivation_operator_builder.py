from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import CustomerInfo, EnumRepeatsBuilder, HeaderCreator
from coin_sdk.number_portability.messages.common.enum_repeats_builder import EnumOperatorBuilder
from coin_sdk.number_portability.messages.enum.enum_content import EnumContent
from coin_sdk.number_portability.messages.enum.enum_operator_seq import EnumOperatorSeq
from coin_sdk.number_portability.messages.message import Message
from .enum_deactivation_operator_body import EnumDeactivationOperatorBody
from .enum_deactivation_operator_message import EnumDeactivationOperatorMessage
from .enum_number_repeats import EnumNumberRepeats
from .enum_number_seq import EnumNumberSeq


class EnumDeactivationOperatorBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._dossierid = None
        self._currentnetworkoperator = None
        self._typeofnumber = None
        self._enum_deactivation_operator_seqs = []

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_currentnetworkoperator(self, currentnetworkoperator: str):
        self._currentnetworkoperator = currentnetworkoperator
        return self

    def set_typeofnumber(self, typeofnumber: str):
        self._typeofnumber = typeofnumber
        return self

    def add_enum_deactivation_operator_seq(self):
        return EnumDeactivationOperatorRepeatsBuilder(self)

    def build(self):
        repeats = [EnumNumberRepeats(seq) for seq in self._enum_deactivation_operator_seqs]
        enum_deactivation_operator = EnumContent(
            self._dossierid,
            self._currentnetworkoperator,
            self._typeofnumber,
            repeats
        )
        body = EnumDeactivationOperatorBody(enum_deactivation_operator)
        message = EnumDeactivationOperatorMessage(self._header, body)
        return Message(message, MessageType.ENUM_DEACTIVATION_OPERATOR_V3)


class EnumDeactivationOperatorRepeatsBuilder(EnumOperatorBuilder):
    def __init__(self, enum_deactivation_operator_builder: EnumDeactivationOperatorBuilder):
        super().__init__()
        self._enum_deactivation_operator_builder = enum_deactivation_operator_builder

    def set_profileid(self, profileid: str):
        self._set_profileid(profileid)
        return self

    def set_default_service(self, default_service: str):
        self._set_defaultservice(default_service)
        return self

    def finish(self):
        seq = EnumOperatorSeq(self._profileid, self._defaultservice)
        self._enum_deactivation_operator_builder._enum_deactivation_operator_seqs.append(seq)
        return self._enum_deactivation_operator_builder
