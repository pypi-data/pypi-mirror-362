from base_aux.valid.m1_valid_base import *
from base_aux.translator.m1_translator import Translator
from base_aux.pyqt.m3_tm import TableModelTemplate
from base_aux.breeders.m1_breeder_str2_stack import *
from base_aux.breeders.m1_breeder_str1_series import *
from base_aux.pyqt.m0_static import *


# =====================================================================================================================
class TableModel_Devs(TableModelTemplate):
    DATA: "TpManager"
    HEADERS: "Headers"
    HTRANSLATOR: Translator

    # AUX -------------------------------------------
    open__settings: Optional[bool] = None

    def __init__(self, data: "TpManager" = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reinit(data)

    def reinit(self, data: "TpManager" = None) -> None:
        """
        GOAL
        ----
        separate inition!
        """
        if data is not None:
            self.DATA = data

        class Headers(BreederStrStack):
            NAME: int = 0
            DEVICE: BreederStrSeries = BreederStrSeries(None, self.DATA.STAND.DEV_LINES.COUNT_COLUMNS)

        class HTRus:
            NAME: str = "Имя"

        self.HEADERS = Headers()
        self.HTRANSLATOR = Translator(HTRus)

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.STAND.DEV_LINES)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return self.HEADERS.count()

    # def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
    #     if role == Qt.DisplayRole:
    #         # ------------------------------
    #         if orientation == Qt.Horizontal:
    #             return self.HEADERS[section]
    #
    #         # ------------------------------
    #         if orientation == Qt.Vertical:
    #             return str(section + 1)

    # def flags(self, index: QModelIndex) -> int:
    #     # PREPARE -----------------------------------------------------------------------------------------------------
    #     col = index.column()
    #     row = index.row()
    #
    #     dev_group_name: str | None = None
    #     try:
    #         dev_group_name = self.DATA.STAND.DEV_LINESS.names()[row]
    #     except:
    #         pass
    #
    #     row_is_summary: bool = dev_group_name is None
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #     flags = super().flags(index)
    #
    #     if row_is_summary:
    #         pass
    #
    #     elif col in [self.HEADERS.DEVICE, self.HEADERS.ADDRESS] or col in self.HEADERS.CONNECTED:
    #         flags |= Qt.ItemIsUserCheckable
    #         # flags |= Qt.ItemIsSelectable
    #     else:
    #         # flags -= Qt.ItemIsSelectable
    #         pass
    #
    #     # clear SELECTABLE ---------
    #     return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        dev_group_name: str | None = None
        dev_inst: Any | None = None

        try:
            # print(f"{self.DATA.STAND.DEV_LINES.names()=}")
            dev_group_name = self.DATA.STAND.DEV_LINES.names()[row]
        except:
            pass

        if dev_group_name and col in self.HEADERS.DEVICE:
            index = col - self.HEADERS.DEVICE.START_OUTER
            try:
                dev_inst = self.DATA.STAND.DEV_LINES[dev_group_name][index]
            except:
                dev_inst = self.DATA.STAND.DEV_LINES[dev_group_name]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == self.HEADERS.NAME:
                # return f"{tc_cls.NAME}\n{tc_cls.DESCRIPTION}"
                return f"{dev_group_name}"
            if col in self.HEADERS.DEVICE:
                if dev_inst and dev_inst.DEV_FOUND:
                    return dev_inst.ADDRESS
                else:
                    return "-"

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextAlignmentRole:
            """
            VARIANTS ALIGN
            --------------
            not exists NAME!!!} = 0         # (LEFT+TOP) [[[[[[[[DEFAULT IS [LEFT+TOP]]]]]]]]]
            
            AlignLeft=AlignLeading = 1      # LEFT(+TOP)
            AlignRight=AlignTrailing = 2    # RIGHT(+TOP)

            AlignTop = 32       # TOP(+LEFT)
            AlignBottom = 64    # BOT(+LEFT)

            AlignHCenter = 4    # HCENTER(+TOP)
            AlignVCenter = 128  # VCENTER(+LEFT)
            AlignCenter = 132   # VCENTER+HCENTER

            # =====MAYBE DID NOT FIGURED OUT!!!
            AlignAbsolute = 16      # (LEFT+TOP) == asDEFAULT
            AlignBaseline = 256     # (LEFT+TOP) == asDEFAULT

            AlignJustify = 8        # (LEFT+TOP) == asDEFAULT

            AlignHorizontal_Mask = 31   # TOP+RIGHT
            AlignVertical_Mask = 480    # LEFT+VCENTER
            """
            if col == self.HEADERS.NAME:
                return ALIGNMENT.CL
            else:
                return ALIGNMENT.C

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:
            if col in self.HEADERS.DEVICE:
                if dev_inst:
                    if dev_inst.DEV_FOUND:
                        return QColor('#50FF50')
                    else:
                        return QColor('#FF5050')


# =====================================================================================================================
