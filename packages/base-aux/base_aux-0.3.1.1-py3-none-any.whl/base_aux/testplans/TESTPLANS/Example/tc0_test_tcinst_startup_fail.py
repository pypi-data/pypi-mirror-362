from base_aux.testplans.tc import *
from base_aux.valid.m2_valid_derivatives import *
from base_aux.valid.m3_valid_chains import *
from .tc0_groups import *


# =====================================================================================================================
class TestCase(Base_TestCase):
    ASYNC = True
    DESCRIPTION = "test TC_inst startup fail"

    # RUN -------------------------------------------------------------------------------------------------------------
    def startup__wrapped(self) -> TYPING__RESULT_W_EXX:
        return False


# =====================================================================================================================
