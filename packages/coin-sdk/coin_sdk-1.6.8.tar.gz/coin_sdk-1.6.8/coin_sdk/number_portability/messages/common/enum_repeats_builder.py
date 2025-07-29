from . import EnumRepeats
from . import EnumProfileSeq
from . import NumberSeries


class EnumRepeatsBuilder:
    def __init__(self):
        self._enum_repeats = []
        self._number_series = None

    def _add_enum_prof_seq(self, *profileids):
        self._enum_repeats = [EnumRepeats(EnumProfileSeq(profileid)) for profileid in profileids]

    def _set_number_series(self, start: str, end: str):
        self._number_series = NumberSeries(start, end)

class EnumOperatorBuilder:
    def __init__(self):
        self._profileid = None
        self._defaultservice = None

    def _set_profileid(self, profileid: str):
        self._profileid = profileid

    def _set_defaultservice(self, defaultservice: str):
        self._defaultservice = defaultservice
