"""
GOAL
----
collect all obvious variants of code base_types

USEFUL IDEAS
------------
- in tests
- could be clearly used in docstrings without needless defining
    assert get_bool(LAMBDA_EXX) is False
"""
# =====================================================================================================================
from typing import *


# =====================================================================================================================
RANGE0: Iterable[int] = range(0)
RANGE1: Iterable[int] = range(1)
RANGE2: Iterable[int] = range(2)
RANGE3: Iterable[int] = range(3)


# =====================================================================================================================
class VALUES_BLANK__ELEMENTARY_SINGLE:
    NONE: None = None
    BOOL: bool = False
    INT: int = 0
    FLOAT: float = 0.0
    STR: str = ""         # that is why i create all others BLANKS_*
    BYTES: bytes = b""


class VALUES_BLANK__ELEMENTARY_COLLECTION:
    LIST: list = []
    TUPLE: tuple = ()
    DICT: dict = {}
    SET: set = set()
    RANGE: Iterable = RANGE0


@final
class VALUES_BLANK(VALUES_BLANK__ELEMENTARY_SINGLE, VALUES_BLANK__ELEMENTARY_COLLECTION):
    """
    GOAL
    ----
    keep all variants in one object with ability to iterate in bunch checks!
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
class VALUES_NOT_BLANK__ELEMENTARY_SINGLE:
    # NONE: None = None
    BOOL: bool = True
    INT: int = 1
    FLOAT: float = 1.2
    STR: str = "str"         # that is why i create all others BLANKS_*
    BYTES: bytes = b"bytes"


class VALUES__ELEMENTARY_SINGLE(VALUES_NOT_BLANK__ELEMENTARY_SINGLE):
    NONE: None = None


class VALUES_NOT_BLANK__ELEMENTARY_COLLECTION:
    LIST: list = [1, 2, ]
    TUPLE: tuple = (1, 2, )
    DICT: dict = {1: 11}
    SET: set = (1, 2, )
    RANGE: Iterable = RANGE1


@final
class VALUES_NOT_BLANK(VALUES_NOT_BLANK__ELEMENTARY_SINGLE, VALUES_NOT_BLANK__ELEMENTARY_COLLECTION):
    pass


# =====================================================================================================================
GEN_COMPR: Iterable = (i for i in range(3))


# ---------------------------------------------------------------------------------------------------------------------
def FUNC(*args, **kwargs) -> None:
    pass


def FUNC_NONE(*args, **kwargs) -> None:
    return None


def FUNC_TRUE(*args, **kwargs) -> bool:
    return True


def FUNC_FALSE(*args, **kwargs) -> bool:
    return False


def FUNC_ALL(*args, **kwargs) -> bool:
    """
    return all(args) and all(kwargs.values())

    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.run as tests
    """
    return all(args) and all(kwargs.values())


def FUNC_ANY(*args, **kwargs) -> bool:
    """
    return any(args) or any(kwargs.values())

    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.run as tests
    """
    return any(args) or any(kwargs.values())


def FUNC_LIST_DIRECT(*args, **kwargs) -> list[Any]:
    """
    DIRECT LIST() for Args+Kwargs

    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.get_bool as test variant

    return list(args) + list(kwargs)
    """
    return list(args) + list(kwargs)


def FUNC_LIST_VALUES(*args, **kwargs) -> list[Any]:
    """
    LIST() values for Args+Kwargs.values()

    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.get_bool as test variant

    return list(args) + list(kwargs.values())
    """
    return list(args) + list(kwargs.values())


def FUNC_DICT(*args, **kwargs) -> dict[Any, Any | None]:
    """
    DIRECT DICT() for Args+Kwargs

    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.get_bool as test variant

    return like DICT(*args, **kwargs)
    """
    result = dict.fromkeys(args)
    result.update(kwargs)
    return result


def FUNC_EXX(*args, **kwargs) -> Exception:
    return Exception("FUNC_EXX")


def FUNC_RAISE(*args, **kwargs) -> NoReturn:
    raise Exception("CALLABLE_RAISE")


def FUNC_GEN(*args, **kwargs) -> Generator:
    yield from range(5)


def FUNC_ECHO(echo: Any = None, *args, **kwargs) -> Any | NoReturn:
    return echo


# =====================================================================================================================
LAMBDA_ARGS: Callable[..., tuple[Any, ...]] = lambda *args: args        # used as resolve ARGS
LAMBDA_KWARGS: Callable[..., dict[str, Any]] = lambda **kwargs: kwargs  # used as resolve KWARGS
"""
GOAL
----
smth like 
for ARGS - ensure tuple
for KWARGS - use strings without quotes in dicts - but ypu may use directly dict(key1=1, ...)

USAGE
-----
for i in LAMBDA_ARGS(1, 2, 3):
    print(i)
"""


# ---------------------------------------------------------------------------------------------------------------------
LAMBDA: Callable[..., Any] = lambda *args, **kwargs: None
LAMBDA_0: Callable[..., int] = lambda *args, **kwargs: 0
LAMBDA_1: Callable[..., int] = lambda *args, **kwargs: 1
LAMBDA_NONE: Callable[..., None] = lambda *args, **kwargs: None
LAMBDA_TRUE: Callable[..., bool] = lambda *args, **kwargs: True
LAMBDA_FALSE: Callable[..., bool] = lambda *args, **kwargs: False

LAMBDA_EXX: Callable[..., Exception] = lambda *args, **kwargs: Exception("LAMBDA_EXX")
# LAMBDA_RAISE = lambda *args, **kwargs: raise Exception("LAMBDA_EXX")      # raise=SyntaxError: invalid syntax
LAMBDA_RAISE: Callable[..., NoReturn] = lambda *args, **kwargs: FUNC_RAISE()
# LAMBDA_GEN = lambda *args, **kwargs: yield from range(5)      # yield=SyntaxError: invalid syntax
LAMBDA_GEN: Callable[..., Iterable[Any]] = lambda *args, **kwargs: FUNC_GEN()
LAMBDA_ECHO: Callable[..., Any] = lambda echo, *args, **kwargs: echo

LAMBDA_ALL: Callable[..., bool] = lambda *args, **kwargs: FUNC_ALL(*args, **kwargs)
LAMBDA_ANY: Callable[..., bool] = lambda *args, **kwargs: FUNC_ANY(*args, **kwargs)

LAMBDA_LIST_DIRECT = lambda *args, **kwargs: FUNC_LIST_DIRECT(*args, **kwargs)
LAMBDA_LIST_VALUES = lambda *args, **kwargs: FUNC_LIST_VALUES(*args, **kwargs)
LAMBDA_DICT = lambda *args, **kwargs: FUNC_DICT(*args, **kwargs)


# =====================================================================================================================
class ClsException(Exception):
    pass
INST_EXCEPTION = ClsException("Exception")

# ---------------------------------------------------------------------------------------------------------------------
# class ClsBool(bool):  # cant use it!
#     pass


class ClsInt(int):
    pass


class ClsFloat(float):
    pass


class ClsStr(str):
    pass


class ClsList(list):
    pass


class ClsTuple(tuple):
    pass


class ClsSet(set):
    pass


class ClsDict(dict):
    pass


CLASSES__AS_FUNC: tuple[type, ...] = (ClsInt, ClsFloat, ClsStr, ClsList, ClsTuple, ClsSet, ClsDict, )   # actually this is keep all buildIn


# =====================================================================================================================
class Cls:
    pass
INST = Cls()


class ClsEmpty:
    pass
INST_EMPTY = ClsEmpty()


# ---------------------------------------------------------------------------------------------------------------------
class ClsInitArgsKwargs:
    """
    GOAL
    ----
    just apply init with any args/kwargs
    so no Exception would raise in any case!
    in first idea it was not matter to keep them in instance but did it just in case

    CREATED SPECIALLY FOR
    ---------------------
    ClsBoolTrue/*False
    """
    ARGS: tuple
    KWARGS: dict

    def __init__(self, *args, **kwargs):
        self.ARGS = args
        self.KWARGS = kwargs


class ClsInitRaise:
    def __init__(self, *args, **kwargs) -> NoReturn:
        raise Exception("ClsInitRaise")


# ---------------------------------------------------------------------------------------------------------------------
class ClsCall:
    def __call__(self, *args, **kwargs) -> None:
        pass

    def meth(self, *args, **kwargs) -> None:
        """
        for other results like None/True/False/ClsException use direct LAMBDA/FUNC_*! or wait special necessity.
        """
        pass
INST_CALL = ClsCall()


class ClsCallNone(ClsCall):
    pass
INST_CALL_NONE = ClsCallNone()


class ClsCallTrue:
    def __call__(self, *args, **kwargs) -> bool:
        return True
INST_CALL_TRUE = ClsCallTrue()


class ClsCallFalse:
    def __call__(self, *args, **kwargs) -> bool:
        return False
INST_CALL_FALSE = ClsCallFalse()


class ClsCallRaise:
    def __call__(self, *args, **kwargs) -> NoReturn:
        raise Exception("ClsCallRaise")
INST_CALL_RAISE = ClsCallRaise()


class ClsCallExx:
    def __call__(self, *args, **kwargs) -> Exception:
        return Exception("ClsCallExx")
INST_CALL_EXX = ClsCallExx()


# ---------------------------------------------------------------------------------------------------------------------
class ClsBoolTrue(ClsInitArgsKwargs):
    """
    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.get_bool as test variant
    """
    def __bool__(self):
        return True
INST_BOOL_TRUE = ClsBoolTrue()


class ClsBoolFalse(ClsInitArgsKwargs):
    """
    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.get_bool as test variant
    """
    def __bool__(self):
        return False
INST_BOOL_FALSE = ClsBoolFalse()


class ClsBoolRaise(ClsInitArgsKwargs):
    """
    CREATED SPECIALLY FOR
    ---------------------
    funcs.Valid.get_bool as test variant
    """
    def __bool__(self):
        raise Exception()
INST_BOOL_RAISE = ClsBoolRaise()


# ---------------------------------------------------------------------------------------------------------------------
class ClsIterYield:
    """
    CONSTRAINTS
    -----------
    YIELD and RETURN all are acceptable!
    several iterations - work fine!

        class Cls:
        def __iter__(self):
            yield from range(3)
            # return iter(range(3))

        obj = Cls()
        for _ in range(2):
            print()
            for i in obj:
                print(i)
    """

    def __iter__(self):
        # RETURN VARIANTS ------------
        # return [1,2,3]  #TypeError: iter() returned non-iterator of type 'list'
        # return range(5)  #TypeError: iter() returned non-iterator of type 'range'
        # return iter([1,2,3])  #OK

        # YIELD VARIANTS ------------    - MOST PREFERRED!(seek would be reset all time to the beginning!!!)
        # yield from [1,2,3]  #OK
        yield from range(5)   #OK
INST_ITER_YIELD = ClsIterYield()


class ClsIterArgs:
    ARGS: tuple

    def __init__(self, *args):
        self.ARGS = args

    def __iter__(self):
        yield from self.ARGS
INST_ITER_ARGS = ClsIterArgs()


class ClsGen:
    """
    ClsIterNext!
    """
    def __init__(self, start=1, end=3):
        self.start = start
        self.end = end
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        else:
            result = self.current
            self.current += 1
            return result
INST_GEN = ClsGen()


# ---------------------------------------------------------------------------------------------------------------------
class ClsEq:
    def __init__(self, val: Any = None, *args, **kwargs):
        self.VAL = val

    def __eq__(self, other):
        return other == self.VAL
INST_EQ = ClsEq()


class ClsEqTrue(ClsInitArgsKwargs):
    def __eq__(self, other):
        return True
INST_EQ_TRUE = ClsEqTrue()


class ClsEqFalse(ClsInitArgsKwargs):
    def __eq__(self, other):
        return False
INST_EQ_FALSE = ClsEqFalse()


class ClsEqRaise(ClsInitArgsKwargs):
    def __eq__(self, other):
        raise Exception()
INST_EQ_RAISE = ClsEqRaise()


# ---------------------------------------------------------------------------------------------------------------------
class ClsFullTypes:
    attrZero = 0

    attrNone = None
    attrTrue = True
    attrFalse = False
    attrInt = 1
    attrFloat = 1.1
    attrStr = "str"
    attrBytes = b"bytes"

    attrFunc = FUNC
    attrFuncTrue = FUNC_TRUE
    attrFuncList = FUNC_LIST_DIRECT
    attrFuncDict = FUNC_DICT
    attrFuncExx = FUNC_EXX
    attrFuncRaise = FUNC_RAISE
    attrFuncGen = FUNC_GEN

    attrGenCompr = GEN_COMPR

    attrCls = ClsEmpty
    attrInst = ClsEmpty()
    attrInstMeth = ClsCall().meth

    attrClsCall = ClsCall
    attrInstCall = INST_CALL
    attrClsCallTrue = ClsCallTrue
    attrInstCallTrue = INST_CALL_TRUE
    attrClsCallRaise = ClsCallRaise
    attrInstCallRaise = INST_CALL_RAISE
    attrClsCallExx = ClsCallExx
    attrInstCallExx = INST_CALL_EXX

    attrClsIterYield = ClsIterYield
    attrInstIterYield = INST_ITER_YIELD
    attrClsGen = ClsGen
    attrInstGen = INST_GEN

    attrClsBoolTrue = ClsBoolTrue
    attrInstBoolTrue = INST_BOOL_TRUE
    attrClsBoolFalse = ClsBoolFalse
    attrInstBoolFalse = INST_BOOL_FALSE
    attrClsBoolRaise = ClsBoolRaise
    attrInstBooRaise = INST_BOOL_RAISE

    attrSet = {1,2,3}
    attrList = [1,2,3]
    attrTuple = (1,2,3)
    attrDict = {1:1}
    attrListInst = [*[Cls(), ] * 3, 1]

    @property
    def propertyNone(self) -> None:
        return
    @classmethod
    @property
    def propertyClassmethodNone(cls) -> None:
        return

    @property
    def propertyInt(self) -> int:
        return 1
    @property
    def propertyExx(self) -> Exception:
        return Exception("propertyExx")
    @property
    def propertyRaise(self) -> NoReturn:
        raise Exception("propertyRaise")
    @property
    def propertyFunc(self) -> Callable:
        return FUNC

    def methNone(self) -> None:
        return
    def methInt(self) -> int:
        return 1
    def methExx(self) -> Exception:
        return Exception("methExx")
    def methRaise(self) -> NoReturn:
        raise Exception("methRaise")
    def methFunc(self) -> Callable:
        return FUNC
    @classmethod
    def classmethodNone(cls) -> None:
        return
    @staticmethod
    def staticmethodNone() -> None:
        return
INST_FULL_TYPES = ClsFullTypes()


# ---------------------------------------------------------------------------------------------------------------------
@final
class VALUES_CALLABLE:
    """
    GOAL
    ----
    collect all callables in one place
    """
    LAMBDA: Callable = LAMBDA
    FUNC: Callable = FUNC

    CLS: Callable | type = ClsCall
    INST: Callable = INST_CALL

    METH_CLS: Callable | type = ClsFullTypes.methNone
    METH_CLS_CLASSMETHOD: Callable = ClsFullTypes.classmethodNone
    METH_CLS_STATICMETHOD: Callable = ClsFullTypes.staticmethodNone
    METH_CLS_PROPERTY: Any = ClsFullTypes.propertyNone                           # NOT VALUES_CALLABLE!!!
    METH_CLS_PROPERTY_CLASSMETHOD: Any = ClsFullTypes.propertyClassmethodNone    # NOT VALUES_CALLABLE!!!

    METH_INST: Callable = INST_FULL_TYPES.methNone
    METH_INST_CLASSMETHOD: Callable = INST_FULL_TYPES.classmethodNone
    METH_INST_STATICMETHOD: Callable = INST_FULL_TYPES.staticmethodNone
    METH_INST_PROPERTY: Any = INST_FULL_TYPES.propertyNone                           # NOT VALUES_CALLABLE!!!
    METH_INST_PROPERTY_CLASSMETHOD: Any = INST_FULL_TYPES.propertyClassmethodNone    # NOT VALUES_CALLABLE!!!

    # PROPERTIES is not callables cause of when we access the attribute, decorator will return really final value not callable


def _callable__show_who_really_are():
    # from base_aux.base_types import ObjectInfo
    # ObjectInfo(VALUES_CALLABLE).print()
    # exit()
    from base_aux.aux_attr.m1_annot_attr1_aux import AttrAux_Existed
    for name, item in AttrAux_Existed(VALUES_CALLABLE).dump_dict().items():
        print(f"{name}={callable(item)}")


# ---------------------------------------------------------------------------------------------------------------------
class VictimAttrs:
    # At0
    At1 = None

    An0: Any
    An1: Any = None

    Ct1 = lambda x=None: 1
    Cn1: Callable = lambda x=None: 1


# =====================================================================================================================
if __name__ == "__main__":
    _callable__show_who_really_are()
    VictimAttrs().Cn1()


# =====================================================================================================================
