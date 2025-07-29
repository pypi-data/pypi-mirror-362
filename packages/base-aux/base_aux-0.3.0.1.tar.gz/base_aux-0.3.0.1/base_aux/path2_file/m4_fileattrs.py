import pathlib

from base_aux.aux_attr.m4_kits import AttrKit_Blank
from base_aux.base_nest_dunders.test__m1_attr3_lambda_resolve import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.path2_file.m3_filetext import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_kwargs import *


# =====================================================================================================================
class FileAttrs_Loader(TextFile, NestCall_Resolve):
    """
    GOAL
    ----
    load attrs as parsed dict
    main usage is final key values!
    used for get settings from file into NestInit_AnnotsAttrByKwArgsIc
    """
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = AttrKit_Blank
    STYLE: EnumAdj_DictTextFormat = EnumAdj_DictTextFormat.AUTO
    KEYPATH: tuple[str | int, ...]

    FILEPATH: pathlib.Path
    TEXT: str

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            target: type | Any = None,
            keypath: tuple[str | int, ...] = None,     # path to exact dict in dict
            style: EnumAdj_DictTextFormat = None,

            **kwargs,       # init File/Text
    ) -> None | NoReturn:
        super().__init__(**kwargs)

        self.init_style(style)

        if target is not None:
            self.TARGET = target

        if keypath is not None:
            self.KEYPATH = keypath
        else:
            self.KEYPATH = tuple()

    def init_style(self, style: EnumAdj_DictTextFormat) -> None:
        if style is not None:
            self.STYLE = EnumAdj_DictTextFormat(style)

        if self.STYLE == EnumAdj_DictTextFormat.EXTENTION:
            for item in EnumAdj_DictTextFormat:
                if self.FILEPATH.name.lower().endswith(str(item.value).lower()):
                    self.STYLE = item
                    break

        if self.STYLE is None:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self) -> NestInit_AnnotsAttrByKwArgs | Any | NoReturn:
        # get dict -------
        data = self.parse__dict(self.STYLE)
        if data is None:
            raise Exx__Incompatible(f"{self.STYLE=}/{self.TEXT=}")

        # load keypath ---
        if self.KEYPATH:
            data = IterAux(data).value__get(*self.KEYPATH)

        # load args -------
        if TypeAux(self.TARGET).check__class() and issubclass(self.TARGET, NestInit_AnnotsAttrByKwArgs):
            # used for check Annots all inited!

            result = self.TARGET(**data)
        else:
            AttrAux_AnnotsAll(self.TARGET).sai__by_args_kwargs(**data)
            result = self.TARGET

        return result


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
