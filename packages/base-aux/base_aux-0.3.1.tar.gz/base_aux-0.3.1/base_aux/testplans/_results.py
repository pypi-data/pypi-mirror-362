# FIXME: THIS is an attempt to separate results!


from typing import *


# =====================================================================================================================
class TpResults:
    """
    Results for whole testplan at one dut!!!
    """
    TCS_CLS: dict[type['TC'], list['TC']]

    def __init__(self, tc: 'TC'):
        pass
        self.TC = tc
        # index will get from TC!!!

    @classmethod
    def set__tcs(cls, tcs):
        pass

    def clear(self, cls=None):
        pass

    def add_result(self, cls, result):
        pass

    def get_result(self, cls):
        pass


# =====================================================================================================================
