from coin_sdk.number_portability.domain import MessageType
from coin_sdk.number_portability.messages.common import HeaderCreator
from coin_sdk.number_portability.messages.enum.enum_profile_activation import EnumProfileActivation
from coin_sdk.number_portability.messages.message import Message
from .enum_profile_activation_body import EnumProfileActivationBody
from .enum_profile_activation_message import EnumProfileActivationMessage


class EnumProfileActivationBuilder(HeaderCreator):
    def __init__(self):
        super().__init__()
        self._dossierid = None
        self._currentnetworkoperator = None
        self._typeofnumber = None

        self._scope = None
        self._profileid = None
        self._ttl = None
        self._dnsclass = None
        self._rectype = None
        self._order = None
        self._preference = None
        self._flags = None
        self._enumservice = None
        self._regexp = None
        self._usertag = None
        self._domain = None
        self._spcode = None
        self._processtype = None
        self._gateway = None
        self._service = None
        self._domaintag = None
        self._replacement = None

    def set_dossierid(self, dossierid: str):
        self._dossierid = dossierid
        return self

    def set_currentnetworkoperator(self, currentnetworkoperator: str):
        self._currentnetworkoperator = currentnetworkoperator
        return self

    def set_typeofnumber(self, typeofnumber: str):
        self._typeofnumber = typeofnumber
        return self

    def set_scope(self, scope: str):
        self._scope = scope
        return self

    def set_profileid(self, profileid: str):
        self._profileid = profileid
        return self

    def set_ttl(self, ttl: str):
        self._ttl = ttl
        return self

    def set_dnsclass(self, dnsclass: str):
        self._dnsclass = dnsclass
        return self

    def set_rectype(self, rectype: str):
        self._rectype = rectype
        return self

    def set_order(self, order: str):
        self._order = order
        return self

    def set_preference(self, preference: str):
        self._preference = preference
        return self

    def set_flags(self, flags: str):
        self._flags = flags
        return self

    def set_enumservice(self, enumservice: str):
        self._enumservice = enumservice
        return self

    def set_regexp(self, regexp: str):
        self._regexp = regexp
        return self

    def set_usertag(self, usertag: str):
        self._usertag = usertag
        return self

    def set_domain(self, domain: str):
        self._domain = domain
        return self

    def set_spcode(self, spcode: str):
        self._spcode = spcode
        return self

    def set_processtype(self, processtype: str):
        self._processtype = processtype
        return self

    def set_gateway(self, gateway: str):
        self._gateway = gateway
        return self

    def set_service(self, service: str):
        self._service = service
        return self

    def set_domaintag(self, domaintag: str):
        self._domaintag = domaintag
        return self

    def set_replacement(self, replacement: str):
        self._replacement = replacement
        return self

    def build(self):
        enum_activation_number = EnumProfileActivation(
            self._dossierid,
            self._currentnetworkoperator,
            self._typeofnumber,
            self._scope,
            self._profileid,
            self._ttl,
            self._dnsclass,
            self._rectype,
            self._order,
            self._preference,
            self._flags,
            self._enumservice,
            self._regexp,
            self._usertag,
            self._domain,
            self._spcode,
            self._processtype,
            self._gateway,
            self._service,
            self._domaintag,
            self._replacement,
        )
        body = EnumProfileActivationBody(enum_activation_number)
        message = EnumProfileActivationMessage(self._header, body)
        return Message(message, MessageType.ENUM_PROFILE_ACTIVATION_V3)
