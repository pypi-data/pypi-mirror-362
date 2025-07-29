"""
GOAL
----
try keep all patterns for life!
"""
from base_aux.base_enums.m2_enum1_adj import *
from base_aux.base_values.m2_value_special import *


# =====================================================================================================================
class Patterns:
    """
    STYLE
    -----
    PNAME: str = r""
    """


# =====================================================================================================================
class Pat_VersionBlock(Patterns):
    # CLEAR: list[str] = [r"[\"' -]*", ]
    VALID_REVERSE: list[str] = [r".*\d[^0-9a-zA-Z]+\d.*", r".*[a-zA-Z][^0-9a-zA-Z]+[a-zA-Z].*", r".*[:].*"]
    # VALID: list[str] = [r"[0-9a-z]+", ]
    ITERATE: str = r"\d+|[a-z]+"


class Pat_Version(Patterns):
    # VERSION_TUPLE = r"\((\d+\.+(\w+\.?)+)\)"
    # VERSION_LIST = r"\[(\d+\.+(\w+\.?)+)\]"
    VERSION_IN_BRACKETS: list = [r"\((.*)\)", r"\[(.*)\]"]  # get first bracket!!!
    VALID_BRACKETS: list = [r"[^\[].*\]", r"\[.*[^\]]", r"[^\(].*\)", r"\(.*[^\)]"]


# =====================================================================================================================
class Pat_Cmts(Patterns):
    """
    GOAL
    ----
    patterns for parse comments
    """
    SHARP_LINE: str = r"^\#.*$"
    SHARP_INLINE: str = r"\s+\#.*$"

    DSLASH_LINE: str = r"^\/\/.*$"
    DSLASH_INLINE: str = r"\s+\/\/.*$"

    REM_LINE: str = r"^REM +.*$"
    REM_INLINE: str = r"\s+REM +.*$"

    C_MLINE: str = r"\s*/\*(.|\n)*?\*/ *"


# =====================================================================================================================
class Pat_NumberSingle(Patterns):
    """
    NOTE
    ----
    All patts ready to get result value by first group!

    *Exact - for exact/only number without any cover (suffix-prefix)!
    *COVERED - for any trash cover! used in re.fullmatch
    """
    # aux ---------
    _fpoint: EnumAdj_NumFPoint = EnumAdj_NumFPoint.AUTO
    _cover: tuple[str, str] = (r"\D*?", r"\D*")

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, fpoint: TYPING__FPOINT_DRAFT = NoValue) -> None | NoReturn:
        if fpoint is NoValue:
            pass
        elif fpoint in EnumAdj_NumFPoint:
            self._fpoint = EnumAdj_NumFPoint(fpoint)
        else:
            raise TypeError(f"{fpoint=}")

    # -----------------------------------------------------------------------------------------------------------------
    INT_EXACT: str = r"(-?\d+)"

    @classmethod
    @property
    def INT_COVERED(cls) -> str:
        return cls._cover[0] + cls.INT_EXACT + cls._cover[1]

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def FLOAT_EXACT(self) -> str:
        if self._fpoint == EnumAdj_NumFPoint.DOT:
            return r"(-?\d+\.\d+)"
        if self._fpoint == EnumAdj_NumFPoint.COMMA:
            return r"(-?\d+\,\d+)"
        if self._fpoint == EnumAdj_NumFPoint.AUTO:
            return r"(-?\d+[,.]\d+)"

    @property
    def FLOAT_COVERED(self) -> str:
        return self._cover[0] + self.FLOAT_EXACT + self._cover[1]

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def BOTH_EXACT(self) -> str:
        return r"(" + self.FLOAT_EXACT + r"|" + self.INT_EXACT + r")"   # float at FIRST PLACE only!

    @property
    def BOTH_COVERED(self) -> str:
        return self._cover[0] + self.BOTH_EXACT + self._cover[1]


# =====================================================================================================================
