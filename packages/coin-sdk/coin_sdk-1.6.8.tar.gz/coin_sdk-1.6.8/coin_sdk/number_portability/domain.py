from enum import Enum


class ConfirmationStatus(Enum):
    UNCONFIRMED = "Unconfirmed"
    ALL = "All"


class MessageType(Enum):
    ACTIVATION_SERVICE_NUMBER_V3 = "activationsn"
    CANCEL_V3 = "cancel"
    CONFIRMATION_V3 = "confirmations"
    DEACTIVATION_V3 = "deactivation"
    DEACTIVATION_SERVICE_NUMBER_V3 = "deactivationsn"
    ERROR_FOUND_V3 = "errorfound"
    ENUM_ACTIVATION_NUMBER_V3 = "enumactivationnumber"
    ENUM_ACTIVATION_OPERATOR_V3 = "enumactivationoperator"
    ENUM_ACTIVATION_RANGE_V3 = "enumactivationrange"
    ENUM_DEACTIVATION_NUMBER_V3 = "enumdeactivationnumber"
    ENUM_DEACTIVATION_OPERATOR_V3 = "enumdeactivationoperator"
    ENUM_DEACTIVATION_RANGE_V3 = "enumdeactivationrange"
    ENUM_PROFILE_ACTIVATION_V3 = "enumprofileactivation"
    ENUM_PROFILE_DEACTIVATION_V3 = "enumprofiledeactivation"
    PORTING_REQUEST_V3 = "portingrequest"
    PORTING_REQUEST_ANSWER_V3 = "portingrequestanswer"
    PORTING_PERFORMED_V3 = "portingperformed"
    PORTING_REQUEST_ANSWER_DELAYED_V3 = "pradelayed"
    RANGE_ACTIVATION_V3 = "rangeactivation"
    RANGE_DEACTIVATION_V3 = "rangedeactivation"
    TARIFF_CHANGE_SERVICE_NUMBER_V3 = "tariffchangesn"
    _VERSION_SUFFIX_V3 = "-v3"

    def get_event_type(self):
        return f'{self.value}{self._VERSION_SUFFIX_V3.value}'
