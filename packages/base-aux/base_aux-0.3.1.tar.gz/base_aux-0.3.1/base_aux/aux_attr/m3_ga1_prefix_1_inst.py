from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *
from base_aux.base_types.m1_type_aux import TypeAux

from base_aux.aux_attr.m1_annot_attr1_aux import AttrAux_Existed


# =====================================================================================================================
# FIXME: rebuild to separated special class RaiseIfPositive
#   by now it seems to sophisticated!


# =====================================================================================================================
class NestGa_Prefix:
    """
    this is just a Base!

    EXAMPLES
    --------
    see NestGa_Prefix_RaiseIf with tests
    """
    GETATTR_PREFIXES: list[str] = []

    def __getattr__(self, item: str) -> Any | Callable | NoReturn:
        """
        SHARING PARAMS BETWEEN CALLABLE PREFIX/ITEM
        -------------------------------------------
        you can not use params! and not use callables (static attributes are available)!
        args - all - goes for ITEM
        kwargs - all uppercase - goes for PREFIX (after changing by lower())
        kwargs - others - goes for ITEM directly (without changing case)!

        if you provide not existed args/kwargs - you will get direct corresponding exception like "print(hello=1) -> TypeError: 'hello' is an invalid keyword argument for print() "

        NOTE
        ----
        0. CaseInSensitive!
        1. prefix - callable with first parameter as catching item_value (may be callable or not).
        2.You always need to CALL prefixed result! even if you access to not callable attribute!
        """
        # print("-"*10)
        # print(f"{item=}start")
        # pretend DIRECT anycase name/prefix ----------
        item_original = AttrAux_Existed(self).name_ic__get_original(item)
        if item_original:
            if item_original.lower() == item.lower():
                return getattr(self, item_original)

        # pretend PREFIX ----------
        for prefix in self.GETATTR_PREFIXES:
            # print(f"{prefix=}start")
            prefix_original = AttrAux_Existed(self).name_ic__get_original(prefix)
            if not prefix_original:
                continue

            prefix_meth = getattr(self, prefix_original)

            # direct prefix ----------
            # if item.lower() == prefix.lower():
            #     return lambda *prefix_args, **prefix_kwargs: Lambda(prefix_meth).resolve_raise(*prefix_args, **prefix_kwargs)

            # prefix ----------
            if item.lower().startswith(prefix.lower()):
                item_name = item[len(prefix):]
                item_value = AttrAux_Existed(self).gai_ic(item_name)

                return lambda *meth_args, **meth_kwargs: Lambda(
                    prefix_meth,
                    *[Lambda(item_value, *meth_args, **{k: v for k, v in meth_kwargs.items() if not k.isupper()}).resolve__raise(), ],
                    **{k.lower(): v for k, v in meth_kwargs.items() if k.isupper()}
                ).resolve__raise()

        # print(3)
        raise AttributeError(item)


# =====================================================================================================================
class NestGa_Prefix_RaiseIf(NestGa_Prefix):
    """
    RULES
    -----
    """
    GETATTR_PREFIXES = ["raise_if__", "raise_if_not__"]     # dont use name like _*__*!

    # -----------------------------------------------------------------------------------------------------------------
    def raise_if__(self, source: Any, _reverse: bool | None = None, comment: str = "") -> None | NoReturn:
        result = Lambda(source).resolve__exx()
        if TypeAux(result).check__exception() or bool(result) != bool(_reverse):
            raise Exx__GetattrPrefix_RaiseIf(f"[raise_if__/{_reverse=}]met conditions ({source=}/{comment=})")

    def raise_if_not__(self, source: Any, comment: str = "") -> None | NoReturn:
        return self.raise_if__(source=source, _reverse=True, comment=comment)


# =====================================================================================================================
def _example():
    class GetattrPrefixInst_RaiseIf_data(NestGa_Prefix_RaiseIf):
        ATTR0 = 0
        ATTR1 = 1

        TRUE = True
        FALSE = False
        NONE = None

        def meth(self, value: Any = None):
            return value

        def METH(self, arg1=1, arg2=2):
            return arg1 == arg2

    assert GetattrPrefixInst_RaiseIf_data().TRUE is True
    assert GetattrPrefixInst_RaiseIf_data().true is True
    assert GetattrPrefixInst_RaiseIf_data().raise_if__none() is None

    # ON ATTRIBUTE --------------------
    # apply prefix+item
    GetattrPrefixInst_RaiseIf_data().raise_if__attr0()  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__attr1()  # Exx__GetattrPrefix_RaiseIf

    # ON METH -------------------------
    # args - one
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(0)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2)  # Exx__GetattrPrefix_RaiseIf

    # args - several
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1,2)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2,2)  # Exx__GetattrPrefix_RaiseIf

    # kwargs
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1, arg2=2)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2, arg2=2)  # Exx__GetattrPrefix_RaiseIf

    # send kwarg for PREFIX ----------
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1, arg2=2, comment="WRONG!")    # RAISE comment argument invalid for meth()!!!
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1, arg2=2, COMMENT="CORRECT!")  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2, arg2=2, COMMENT="CORRECT!")  # Exx__GetattrPrefix_RaiseIf


# =====================================================================================================================
if __name__ == "__main__":
    _example()


# =====================================================================================================================
