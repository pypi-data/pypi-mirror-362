import pytest

from base_aux.base_lambdas.m1_lambda import *


# =====================================================================================================================
class Test__New:
    # Victim: type[NEW_CLASS____]
    # victim: NEW_CLASS____

    @classmethod
    def setup_class(cls):
        pass
        # cls.Victim = type("VICTIM", (NEW_CLASS____,), {})

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1_direct(self):
        assert True

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("1",), 1),
            (("hello",), Exception),
        ]
    )
    def test__2_parametrized_by_one_func(self, args, _EXPECTED):
        Lambda(int, args).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(argnames="func_link", argvalues=[int, float, ])
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("1",), 1),
            (("hello",), Exception),
        ]
    )
    def test__3_parametrized_by_several_funcs(self, func_link, args, _EXPECTED):
        Lambda(func_link, args).expect__check_assert(_EXPECTED)


# =====================================================================================================================
