from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import HeaderCreator
from coin_sdk.number_portability.messages.enum.enum_profile_deactivation import EnumProfileDeactivation
from coin_sdk.number_portability.messages.message import Message
from .enum_profile_deactivation_body import EnumProfileDeactivationBody
from .enum_profile_deactivation_message import EnumProfileDeactivationMessage


class EnumProfileDeactivationBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._dossierid = None
        self._currentnetworkoperator = None
        self._typeofnumber = None
        self._profileid = None

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_currentnetworkoperator(self, currentnetworkoperator: str):
        self._currentnetworkoperator = currentnetworkoperator
        return self

    def set_typeofnumber(self, typeofnumber: str):
        self._typeofnumber = typeofnumber
        return self

    def set_profileid(self, profileid: str):
        self._profileid = profileid
        return self

    def build(self):
        enum_deactivation_number = EnumProfileDeactivation(
            self._dossierid,
            self._currentnetworkoperator,
            self._typeofnumber,
            self._profileid,
        )
        body = EnumProfileDeactivationBody(enum_deactivation_number)
        message = EnumProfileDeactivationMessage(self._header, body)
        return Message(message, MessageType.ENUM_PROFILE_DEACTIVATION_V3)
