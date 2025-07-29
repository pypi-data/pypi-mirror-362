import pytest
from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_values.m4_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m7_cmp import *


# =====================================================================================================================
class Cls(NestCmp_LGET):
    def __init__(self, value):
        self.VALUE = value

    def __cmp__(self, other):
        other = Cls(other)
        if self.VALUE == other.VALUE:
            return 0
        if self.VALUE > other.VALUE:
            return 1
        if self.VALUE < other.VALUE:
            return -1


def test____LE__():
    func_link = lambda result: result == 1
    Lambda(func_link, Cls(1)).expect__check_assert(True)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="func_link, args, kwargs, _EXPECTED, _pytestExpected",
    argvalues=[
        # not callable ------------
        (True, (), {}, True, True),

        (True, (111, ), {"111": 222}, True, True),
        (True, (111, ), {"111": 222}, False, False),

        (False, (), {}, True, False),

        # callable ------------
        (LAMBDA_ECHO, (), {}, True, False),

        (LAMBDA_ECHO, (None, ), {}, True, False),
        (LAMBDA_ECHO, (None, ), {}, None, True),
        (LAMBDA_ECHO, (True, ), {}, True, True),
        (LAMBDA_ECHO, (True, ), {}, True, True),
        (lambda value: value, (), {"value": True}, True, True),
        (lambda value: value, (), {"value": None}, True, False),

        # TYPES -------
        (int, (), {}, int, True),
        (1, (), {}, int, True),
        (1, (), {}, float, False),
        (1, (), {}, Exception, False),
        (Exception, (), {}, Exception, True),
        (Exception(), (), {}, Exception, True),

    ]
)
def test__check_assert(func_link, args, kwargs, _EXPECTED, _pytestExpected):
    try:
        Lambda(func_link, *args, **kwargs).expect__check_assert(_EXPECTED)
    except:
        assert not _pytestExpected
    else:
        assert _pytestExpected


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, []),
        ((None, ), {}, [None, ]),
        ((1, ), {}, [1, ]),
        ((1, 1), {}, [1, 1]),

        ((1, 1), {}, [1, 1]),
        ((1, 1), {"2": 22}, [1, 1, "2"]),
        ((1, 1), {"2": 22, "3": 33}, [1, 1, "2", "3"]),
    ]
)
def test__func_list_direct(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_LIST_DIRECT, *args, **kwargs).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, []),
        ((None, ), {}, [None, ]),
        ((1, ), {}, [1, ]),
        ((1, 1), {}, [1, 1]),

        ((1, 1), {}, [1, 1]),
        ((1, 1), {"2": 22}, [1, 1, 22]),
        ((1, 1), {"2": 22, "3": 33}, [1, 1, 22, 33]),
    ]
)
def test__func_list_values(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_LIST_VALUES, *args, **kwargs).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, {}),
        ((None, ), {}, {None: None}),
        ((1, ), {}, {1: None}),
        ((1, 1), {}, {1: None}),

        ((1, 1), {}, {1: None}),
        ((1, 1), {"2": 22}, {1: None, "2": 22}),
        ((1, 1), {"2": 22, "3": 33}, {1: None, "2": 22, "3": 33}),
    ]
)
def test__func_dict(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_DICT, *args, **kwargs).expect__check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, True),
        ((None, ), {}, False),
        ((1, ), {}, True),
        ((1, 1), {}, True),

        ((1, 1), {}, True),
        ((1, 1), {"2": 22}, True),
        ((1, 1), {"2": 22, "3": 33}, True),

        ((1, 1), {"2": 22, "3": None}, False),
    ]
)
def test__func_all(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_ALL, *args, **kwargs).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, False),
        ((None, ), {}, False),
        ((1, ), {}, True),
        ((1, 1), {}, True),

        ((1, 1), {}, True),
        ((1, 1), {"2": 22}, True),
        ((1, 1), {"2": 22, "3": 33}, True),

        ((1, 1), {"2": 22, "3": None}, True),
        ((1, None), {"2": 22, "3": None}, True),
        ((None, None), {"2": True, "3": None}, True),
        ((None, None), {"2": False, "3": None}, False),

        (Args(None, None), {"2": False, "3": None}, False),
    ]
)
def test__func_any(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_ANY, *args, **kwargs).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        ("11.688889V", EqValid_Regexp(r"\d+[.,]?\d*V"), True),
        (INST_EQ_TRUE, INST_EQ_TRUE, True),
        (INST_EQ_TRUE, INST_EQ_FALSE, True),
        (INST_EQ_FALSE, INST_EQ_TRUE, True),
        (INST_EQ_FALSE, INST_EQ_FALSE, False),
    ]
)
def test__EQ(source, other, _EXPECTED):
    assert Lambda(source).expect__check_bool(other) == _EXPECTED


# =====================================================================================================================
