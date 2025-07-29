from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.base_enums.m2_enum1_adj import *
from base_aux.aux_text.m0_text_examples import *


# =====================================================================================================================
class Test__sub:
    @pytest.mark.parametrize(
        argnames="source, rule, _EXPECTED",
        argvalues=[
            # NOT ACCEPTED -------------
            # ("None123", ("None00"), "None123"),
            # ("None123", ("None"), "123"),
            # ("None123", ("None", None), "123"),
            # ("None123", ("None", "0"), "0123"),
            #
            # ("1*3", ("\*", "2"), "123"),
            ("1:1", (r"\b(\d+\.?\d*)\b\s*:\s*", r'"\1":'), '"1":1'),
            ("123:1", (r"\b(\d+\.?\d*)\b\s*:\s*", r'"\1":'), '"123":1'),
        ]
    )
    def test__regexp(self, source, rule, _EXPECTED):
        func_link = TextAux(source).sub__regexp
        Lambda(func_link, *rule).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, rule, _EXPECTED",
        argvalues=[
            # NOT ACCEPTED -------------
            ("None123", ("None", "null"), "None123"),
            ("None_123", ("None", "null"), "None_123"),

            # ACCEPTED -------------
            ("null", ("None", "null"), "null"),
            ("None", ("None", "null"), "null"),
            ("None-123", ("None", "null"), "null-123"),

            # CONTAINERS -------------
            ("[null]", ("None", "null"), "[null]"),
            ("[None]", ("None", "null"), "[null]"),
            ("[None, ]", ("None", "null"), "[null, ]"),

            (" None, 123", ("None", "null"), " null, 123"),
            ("[None, null, 123]", ("None", "null"), "[null, null, 123]"),

            ("[None, null, 323]", (r"None.*3", "null"), "[null]"),

            ("[None, null, 3 23]", (r"None.*3", "null"), "[null]"),
            ("[None, null, 3 23]", (r"None.*?3", "null"), "[null 23]"),
        ]
    )
    def test__words(self, source, rule, _EXPECTED):
        func_link = TextAux(source).sub__word
        Lambda(func_link, *rule).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Test__Edit:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (" " * 2, ""),
            (" " * 3, ""),
            ("line   line", "lineline"),

            (" \n ", "\n"),

            (" 1, _\n\n  \n \t  \r  ()", '1,_\n\n\n\t\r()'),
        ]
    )
    def test__spaces_all(self, source, _EXPECTED):
        func_link = TextAux(source).clear__spaces_all
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (" " * 2, " "),
            (" " * 3, " "),
            ("line   line", "line line"),

            (" \n  ", " \n "),

            (" 1, _\n\n  \n \t  \r  ()", ' 1, _\n\n \n \t \r ()'),
        ]
    )
    def test__spaces_duplicates(self, source, _EXPECTED):
        func_link = TextAux(source).clear__space_duplicates
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, pat, _EXPECTED",
        argvalues=[
            (" line1 \n \n line3 ", r".*1.*", "\n \n line3 "),
            (" line1 \n \n line3 ", r".*3.*", " line1 \n \n"),
            # (" line1 \n \t\r\n line3 ", r"", " line1 \n line3 "),
        ]
    )
    def test__lines(self, source, pat, _EXPECTED):
        func_link = TextAux(source).clear__lines
        Lambda(func_link, pat).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # BLANK -----
            ("\n", ""),
            (" \n ", ""),

            # EDGES -----
            ("\n line1", " line1"),
            (" \n line1", " line1"),
            (" line1 \n ", " line1 "),

            # MIDDLE -----
            (" line1 \n\n \nline2 ", " line1 \nline2 "),

            # OTHER -----
            (" line1 \n \n line3 ", " line1 \n line3 "),
            (" line1 \n \t\r\n line3 ", " line1 \n line3 "),
        ]
    )
    def test__lines_blank(self, source, _EXPECTED):
        func_link = TextAux(source).delete__lines_blank
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, cmt, _EXPECTED",
        argvalues=[
            # EnumAdj_CmtStyle.SHARP -------------------------------------------------------
            # ZERO -----
            ("line1 ", EnumAdj_CmtStyle.SHARP, "line1 "),

            # SEPARATED -----
            ("#cmt #", EnumAdj_CmtStyle.SHARP, ""),
            ("##cmt #", EnumAdj_CmtStyle.SHARP, ""),

            ("#cmt ", EnumAdj_CmtStyle.SHARP, ""),
            ("  # cmt 1 ", EnumAdj_CmtStyle.SHARP, ""),

            # INLINE -----
            ("line  # cmt 1 ", EnumAdj_CmtStyle.SHARP, "line"),

            # SEVERAL LINES ====
            ("line1  # cmt1 \n line2 ", EnumAdj_CmtStyle.SHARP, "line1\n line2 "),
            ("line1  # cmt1 \n line2 #cmt2", EnumAdj_CmtStyle.SHARP, "line1\n line2"),
            ("line1  # cmt1 \n #cmt \n line2 #cmt2", EnumAdj_CmtStyle.SHARP, "line1\n line2"),

            # EnumAdj_CmtStyle.REM ---------------------------------------------------------
            # ZERO -----
            ("line1 ", EnumAdj_CmtStyle.REM, "line1 "),

            # SEPARATED -----
            ("REM #", EnumAdj_CmtStyle.REM, ""),
            ("REM  REM #", EnumAdj_CmtStyle.REM, ""),

            # INLINE -----
            ("line  REM 1 ", EnumAdj_CmtStyle.REM, "line"),

            # SEVERAL LINES ====
            ("line1  REM cmt1 \n line2 ", EnumAdj_CmtStyle.REM, "line1\n line2 "),
            ("line1  REM cmt1 \n line2 REM", EnumAdj_CmtStyle.REM, "line1\n line2 REM"),
            ("line1  REM cmt1 \n line2 REM ", EnumAdj_CmtStyle.REM, "line1\n line2"),
            ("line1  REM cmt1 \n REM \n line2 REM ", EnumAdj_CmtStyle.REM, "line1\n line2"),

            # EnumAdj_CmtStyle.C ---------------------------------------------------------
            ("line1  /*cmt*/  \n /*cmt*/  \n line2 /*cmt*/  ", EnumAdj_CmtStyle.C, "line1\n line2"),
            ("line1  /*cmt*/  \n /*\ncmt*/  \n line2 /*cmt*/  ", EnumAdj_CmtStyle.C, "line1\n line2"),
        ]
    )
    def test__clear__cmts(self, source, cmt, _EXPECTED):
        func_link = TextAux(source).delete__cmts
        Lambda(func_link, cmt).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            ("  ", ("", "", "")),
            ("line1  ", ("line1", "line1  ", "line1")),
            ("  line1 ", ("line1", "line1 ", "  line1")),

            ("line1  \n  line2", ("line1\nline2", "line1  \nline2", "line1\n  line2")),
            ("line1  \n  \n  line2", ("line1\nline2", "line1  \nline2", "line1\n  line2")),
        ]
    )
    def test__strip__lines(self, source, _EXPECTED):
        Lambda(TextAux(source).strip__lines).expect__check_assert(_EXPECTED[0])
        Lambda(TextAux(source).lstrip__lines).expect__check_assert(_EXPECTED[1])
        Lambda(TextAux(source).rstrip__lines).expect__check_assert(_EXPECTED[2])


# =====================================================================================================================
class Test__find:
    @pytest.mark.parametrize(
        argnames="source, patt, _EXPECTED",
        argvalues=[
            ("None123", r"\w*", ["None123", ]),
            ("None123", r"\w+(?#*.*)", ["None123", ]),
            ("None123  #cmt", r"\w+", ["None123", "cmt"]),
            ("   None123  #cmt", r"\w+", ["None123", "cmt"]),
        ]
    )
    def test__1(self, source, patt, _EXPECTED):
        func_link = TextAux(source).findall
        Lambda(func_link, patt).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Test__shortcut:
    @pytest.mark.parametrize(
        argnames="p1,p2,p3,p4,_EXPECTED",
        argvalues=[
            (None, 5, "...", EnumAdj_Where3.LAST, "None"),  # DOES NOT METTER!
            ("", 5, "...", EnumAdj_Where3.LAST, ""),
            ("123456", 3, "...", EnumAdj_Where3.LAST, "..."),

            ("123", 3, "#", EnumAdj_Where3.LAST, "123"),

            ("1223", 3, "#", EnumAdj_Where3.FIRST, "#23"),
            ("1223", 3, "#", EnumAdj_Where3.MIDDLE, "1#3"),
            ("1223", 3, "#", EnumAdj_Where3.LAST, "12#"),

            ("1223", 3, "##", EnumAdj_Where3.FIRST, "##3"),
            ("1223", 3, "##", EnumAdj_Where3.MIDDLE, "##3"),
            ("1223", 3, "##", EnumAdj_Where3.LAST, "1##"),

            ("1223", 3, "###", EnumAdj_Where3.FIRST, "###"),
            ("1223", 3, "###", EnumAdj_Where3.MIDDLE, "###"),
            ("1223", 3, "###", EnumAdj_Where3.LAST, "###"),

            ("1223", 1, "###", EnumAdj_Where3.FIRST, "#"),
            ("1223", 1, "###", EnumAdj_Where3.MIDDLE, "#"),
            ("1223", 1, "###", EnumAdj_Where3.LAST, "#"),

            #
            ("123", 1, "##", EnumAdj_Where3.FIRST, "#"),
            ("123", 2, "##", EnumAdj_Where3.FIRST, "##"),
            ("123", 3, "##", EnumAdj_Where3.FIRST, "123"),
            ("123", 4, "##", EnumAdj_Where3.FIRST, "123"),
            ("123", 5, "##", EnumAdj_Where3.FIRST, "123"),
        ]
    )
    def test__1(self, p1,p2,p3,p4,_EXPECTED):
        func_link = TextAux(p1).shortcut
        Lambda(func_link, **dict(maxlen=p2, sub=p3, where=p4)).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Test__try_convert_to_object:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (0, True),
            (1, True),
            (10, True),
            (1.0, True),
            (1.1, True),
            (-1.1, True),
            ("", False),
            ('', False),
            ("hello", False),
            (None, True),
            (True, True),
            (False, True),
            ([None, True, 1, -1.1, "hello", "", ''], True),
            # [None, True, 1, -1.1, "hello", [], {1:1}],  #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 37 (char 36)')=KEYS IS ONLY STRINGS
            ([None, True, 1, -1.1, "hello", [], {"1": 1, "hello": []}], True),

            ([], True),
            # (),     # JSONDecodeError('Expecting value: line 1 column 1 (char 0)') - НЕСУЩЕСТВУЕТ TUPLE???
            ({}, True),
            ({"key": True}, True),
            ({"key": False}, True),
            ({"key": None}, True),
            ({"key": 123}, True),
        ]
    )
    def test__MAIN_GOAL__string_source(self, source, _EXPECTED):
        func_link = TextAux(str(source)).parse__object_stringed  # DONT DELETE STR!!!
        assert Lambda(func_link).expect__check_bool(source) == _EXPECTED

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # SINGLE ---------------------
            ({"key1": 123}, {"key1": 123}),

            ({"1": 123}, {"1": 123}),
            ({1: 123}, {"1": 123}),

            ({"1.1": 123}, {"1.1": 123}),
            ({1.1: 123}, {"1.1": 123}),

            # SEVERAL ---------------------
            ({1:1,2:2,3.3:3}, {"1": 1, "2": 2, "3.3": 3}),
            ({1:{1:1},2:{2:2},3.3:3}, {"1":{"1":1}, "2":{"2":2}, "3.3": 3}),
        ]
    )
    def test__parse_dict_keys(self, source, _EXPECTED):
        func_link = TextAux(source).parse__object_stringed
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # =================================================================================================================
    def base_test__try_convert_to_object(self, source, _EXPECTED):
        func_link = TextAux(source).parse__object_stringed
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, None),
            (True, True),
            (False, False),
            (0, 0),
            ([], []),
            ({"1": 1}, {"1": 1}),   # FIXME: need ref to use always ints in keys!
            # ({1: 1}, {1: 1}),   # FIXME: need ref to use always ints in keys!
        ]
    )
    def test__originals(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            ("null", None),
            ("true", True),
            ("false", False),

            ("None", None),

            # ("['None', 1]", [None, 1]),  #JSONDecodeError('Expecting value: line 1 column 2 (char 1)')    # VALUES only DOUBLEQUOTS!!! accepted!!!    # FIXME:
            # ('["None", 1]', [None, 1]),  #FIXME: dont replace None in any quats
            ("[null, 1]", [None, 1]),
            ("[None, 1]", [None, 1]),

            ("True", True),
            ("False", False),
        ]
    )
    def test__bools(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (0, 0),
            ("0", 0),
            ("00", NoValue),
            ("01", NoValue),
            ("10", 10),

            ("1.0", 1.0),
            ("1.000", 1.0),

            ("1,000", NoValue),
        ]
    )
    def test__nums(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            ("[]", []),
            # ("()", ()),     #JSONDecodeError('Expecting value: line 1 column 1 (char 0)'
            ("{}", {}),
            # ("{1: 1}", {1: 1}), #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
            # ("{'1': 1}", {'1': 1}),   #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
            ('{"1": 1}', {'1': 1}),  # KEYS ONLY in DOUBLEQUOTS!!!
        ]
    )
    def test__containers(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        ("None1", ["None1", ]),
        ("None1   #cmt", ["None1", ]),
        ("   None1   #cmt", ["None1", ]),
        ("#cmt      None2", []),
        ("#cmt \n \n None1 #cmt   hello \n   None2", ["None1", "None2", ]),

        ("None>=1.1", ["None>=1.1", ]),
        ("None>=1.1 #cmt \n None=[1.2, ]", ["None>=1.1", "None=[1.2, ]"]),
    ]
)
def test__requirements__get_list(source, _EXPECTED):
    func_link = TextAux(source).parse__requirements_lines
    Lambda(func_link).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Test__ParseNum:
    @pytest.mark.parametrize(
        argnames="source, fpoint, _EXPECTED",
        argvalues=[
            (0, None, 0),
            ("0", None, 0),
            (123, None, 123),
            ("123", None, 123),
            (1.1, None, 1.1),
            ("1.1", None, 1.1),
            ("1,1", None, 1.1),
            ("1,1.", None, 1.1),
            ("1.1.", None, 1.1),
            ("1.1,", None, 1.1),

            ("   0   ", None, 0),
            ("   000   ", None, 0),
            ("-aa001cc", None, 1),
            ("-aa001.000cc", None, 1.0),
            ("-aa001,000cc", None, 1.0),
            ("   -aa001.200cc   ", None, 1.2),
            ("   -aa001.200cc   ", ",", None),
            ("   -aa001,200cc   ", ",", 1.2),
            ("   -aa--001,200cc   ", ",", -1.2),
        ]
    )
    def test__num(self, source, fpoint, _EXPECTED):
        func_link = TextAux(source).parse__number_single
        Lambda(func_link, fpoint).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Test__ParseDict:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, None),
            (0, None),
            (1, None),
            ("", None),
            ("1", None),
            (INI_EXAMPLES.INT_KEY__TEXT, INI_EXAMPLES.INT_KEY__DICT_MERGED),
            (INI_EXAMPLES.MESHED__TEXT, INI_EXAMPLES.MESHED__DICT_MERGED),
            (INI_EXAMPLES.NOT_MESHED__TEXT, INI_EXAMPLES.NOT_MESHED__DICT_MERGED),
        ]
    )
    def test__ini(self, source, _EXPECTED):
        Lambda(TextAux(source).parse__dict_ini).expect__check_assert(_EXPECTED)
        Lambda(TextAux(source).parse__dict).expect__check_assert(_EXPECTED)


# =====================================================================================================================
