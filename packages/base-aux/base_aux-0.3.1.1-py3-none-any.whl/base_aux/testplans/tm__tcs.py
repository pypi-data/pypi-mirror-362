from base_aux.valid.m1_valid_base import *
from base_aux.translator.m1_translator import Translator
from base_aux.pyqt.m3_tm import TableModelTemplate
from base_aux.breeders.m1_breeder_str2_stack import *
from base_aux.breeders.m1_breeder_str1_series import *
from base_aux.pyqt.m0_static import *


# =====================================================================================================================
class TcResultMsg:
    PASS: str = "Успех"
    FAIL: str = "Ошибка"
    WAIT: str = "..."


# =====================================================================================================================
class TableModel_Tps(TableModelTemplate):
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
            TESTCASE: int = 0
            SKIP: None = None
            ASYNC: None = None
            STARTUP_CLS: None = None
            DUTS: BreederStrSeries = BreederStrSeries(None, self.DATA.STAND.DEV_LINES.COUNT_COLUMNS)
            TEARDOWN_CLS: None = None
            # FIXME: need resolve COUNT over DevicesIndexed!!!

        class HTRus:
            TESTCASE: str = "ТЕСТКЕЙС"
            SKIP: str = "Пропустить"
            ASYNC: str = "Асинхр."
            STARTUP_CLS: str = "Подготовка\nтесткейса"
            TEARDOWN_CLS: str = "Завершение\nтесткейса"

        self.HEADERS = Headers()
        self.HTRANSLATOR = Translator(HTRus)

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.STAND.TCSc_LINE) + 1  # [+1]for finalResults

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

    def flags(self, index: QModelIndex) -> int:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        try:
            tc_cls = list(self.DATA.STAND.TCSc_LINE)[row]
        except:
            tc_cls = None

        row_is_summary: bool = tc_cls is None

        # -------------------------------------------------------------------------------------------------------------
        flags = super().flags(index)

        if row_is_summary:
            pass

        elif col in [self.HEADERS.SKIP, self.HEADERS.ASYNC] or col in self.HEADERS.DUTS:
            flags |= Qt.ItemIsUserCheckable
            # flags |= Qt.ItemIsSelectable
        else:
            # flags -= Qt.ItemIsSelectable
            pass

        # clear SELECTABLE ---------
        return flags

    def get_summary_results__str(self, col: int) -> list[str]:
        result = []
        for row in range(self.rowCount() - 1):
            result_i = self.index(row, col).data()
            result.append(result_i)

        # print(f"{col=}/{result=}")
        return result

    def get_summary_result(self, col: int) -> bool | None:
        for row in range(self.rowCount() - 1):
            result_i = self.index(row, col).data()
            # print(f"{col=}/{row=}/{result_i=}")
            if result_i == TcResultMsg.PASS:
                continue
            if result_i == TcResultMsg.FAIL:
                return False
            if result_i == TcResultMsg.WAIT:
                return
            else:
                return
        return True

    def get_summary_result__str(self, col: int) -> str:
        result = self.get_summary_result(col)
        if result is True:
            return TcResultMsg.PASS
        elif result is False:
            return TcResultMsg.FAIL
        else:
            return ""

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        try:
            tc_cls = list(self.DATA.STAND.TCSc_LINE)[row]
        except:
            tc_cls = None

        row_is_summary: bool = tc_cls is None

        dut = None
        tc_inst = None
        if col in self.HEADERS.DUTS and not row_is_summary:
            index = col - self.HEADERS.DUTS.START_OUTER
            try:
                dut = self.DATA.STAND.DEV_LINES.DUT[index]
                # print(f"{tc_cls.TCSi_LINE=}/{index=}")
                tc_inst = tc_cls.TCSi_LINE[index]
            except:
                return

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == self.HEADERS.TESTCASE:
                # return f"{tc_cls.NAME}\n{tc_cls.DESCRIPTION}"
                if row_is_summary:
                    return "ИТОГ:"
                return f"{tc_cls.DESCRIPTION}"
            if col == self.HEADERS.SKIP:
                if row_is_summary:
                    return
                return '+' if tc_cls.SKIP else '-'
            if col == self.HEADERS.ASYNC:
                if row_is_summary:
                    return
                return '+' if tc_cls.ASYNC else '-'

            # STARTUP -------------------
            if col == self.HEADERS.STARTUP_CLS:
                if row_is_summary:
                    return
                try:
                    group_name = tc_cls._EQ_CLS__VALUE.name or ""
                except:
                    group_name = tc_cls._EQ_CLS__VALUE or ""

                if tc_cls.result__startup_cls is None:
                    return group_name
                if tc_cls.result__startup_cls is EnumAdj_ProcessStateActive.STARTED:
                    return TcResultMsg.WAIT
                if isinstance(tc_cls.result__startup_cls, Valid) and tc_cls.result__startup_cls.check__active():
                    return TcResultMsg.WAIT
                if bool(tc_cls.result__startup_cls) is True:
                    return f'+{group_name}'
                if bool(tc_cls.result__startup_cls) is False:
                    return f'-{group_name}'

            # DUTS -------------------
            if col in self.HEADERS.DUTS:
                if row_is_summary:
                    return self.get_summary_result__str(col)
                if tc_inst:
                    if tc_inst.result is None:
                        return ""
                    elif isinstance(tc_inst.result, Valid):
                        if tc_inst.result.check__active():
                            return TcResultMsg.WAIT

                        elif tc_inst.result.STATE_ACTIVE == EnumAdj_ProcessStateActive.FINISHED:
                            if bool(tc_inst.result):
                                return TcResultMsg.PASS
                            else:
                                return TcResultMsg.FAIL
                        else:
                            return

                    else:
                        if bool(tc_inst.result):
                            return TcResultMsg.PASS
                        else:
                            return TcResultMsg.FAIL

            # TEARDOWN -------------------
            if col == self.HEADERS.TEARDOWN_CLS:
                if row_is_summary:
                    return
                if tc_cls.result__teardown_cls is None:
                    return
                if tc_cls.result__teardown_cls is EnumAdj_ProcessStateActive.STARTED:
                    return TcResultMsg.WAIT
                if isinstance(tc_cls.result__teardown_cls, Valid) and tc_cls.result__teardown_cls.check__active():
                    return TcResultMsg.WAIT
                if bool(tc_cls.result__teardown_cls) is True:
                    return TcResultMsg.PASS
                if bool(tc_cls.result__teardown_cls) is False:
                    return TcResultMsg.FAIL

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.ToolTipRole:
            if col == self.HEADERS.TESTCASE:
                if row_is_summary:
                    return "Результаты суммарные по всем тесткейсам\nдля каждого устройства"
                return f"{tc_cls.DESCRIPTION}"
            if col in self.HEADERS.DUTS:
                if row_is_summary:
                    # return
                    return str(self.get_summary_results__str(col))
                if tc_inst:
                    return f"{tc_inst.result}"

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
            if col == self.HEADERS.TESTCASE:
                if row_is_summary:
                    return ALIGNMENT.CR
                return ALIGNMENT.CL
            else:
                return ALIGNMENT.C

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextColorRole:
            if row_is_summary:
                return
            if tc_cls.SKIP:
                return QColor('#a2a2a2')

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:
            if tc_cls and tc_cls.SKIP:
                return QColor('#e2e2e2')

            # ACTIVE ---------------------
            if col == self.HEADERS.TESTCASE:
                if row_is_summary:
                    return
                if self.DATA.tc_active == tc_cls:
                    return QColor("#FFFF50")

            # STARTUP -------------------
            if col == self.HEADERS.STARTUP_CLS:
                if row_is_summary:
                    return
                if tc_cls.result__startup_cls is None:
                    return
                if tc_cls.result__startup_cls is EnumAdj_ProcessStateActive.STARTED:
                    return QColor("#FFFF50")
                if isinstance(tc_cls.result__startup_cls, Valid) and tc_cls.result__startup_cls.check__active():
                    return QColor("#FFFF50")
                if bool(tc_cls.result__startup_cls) is True:
                    return QColor("#50FF50")
                if bool(tc_cls.result__startup_cls) is False:
                    return QColor("#FF5050")

            # DUTS -------------------
            if col in self.HEADERS.DUTS:
                if row_is_summary:
                    result_i = self.get_summary_result(col)
                    if result_i is True:
                        return QColor("#00FF00")
                    elif result_i is False:
                        return QColor("#FF5050")
                    else:
                        return
                if tc_inst.skip_tc_dut or dut.SKIP or not dut.DEV_FOUND:
                    return QColor('#e2e2e2')
                if tc_inst.result__startup is not None and not bool(tc_inst.result__startup):
                    return QColor("#FFa0a0")
                if tc_inst.isRunning():
                    return QColor("#FFFF50")
                if bool(tc_inst.result) is True:
                    return QColor("#00FF00")
                if bool(tc_inst.result) is False:
                    if tc_inst.result is None:
                        return
                    else:
                        return QColor("#FF5050")
                # elif

            # TEARDOWN -------------------
            if col == self.HEADERS.TEARDOWN_CLS:
                if row_is_summary:
                    return
                if tc_cls.result__teardown_cls is None:
                    return
                if tc_cls.result__teardown_cls is EnumAdj_ProcessStateActive.STARTED:
                    return QColor("#FFFF50")
                if isinstance(tc_cls.result__teardown_cls, Valid) and tc_cls.result__teardown_cls.check__active():
                    return QColor("#FFFF50")
                if bool(tc_cls.result__teardown_cls) is True:
                    return QColor("#50FF50")
                if bool(tc_cls.result__teardown_cls) is False:
                    return QColor("#FF5050")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            # -------------------------
            if row_is_summary:
                return
            if not self.open__settings:
                return

            # -------------------------
            if col == self.HEADERS.SKIP:
                if tc_cls.SKIP:
                    return Qt.Checked
                else:
                    return Qt.Unchecked

            if col == self.HEADERS.ASYNC:
                if tc_cls.ASYNC:
                    return Qt.Checked
                else:
                    return Qt.Unchecked

            if col in self.HEADERS.DUTS:
                if (tc_cls and tc_cls.SKIP) or (dut and dut.SKIP):
                    return

                if tc_inst.skip_tc_dut:
                    return Qt.Unchecked
                else:
                    return Qt.Checked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.FontRole:
            if tc_cls == self.DATA.tc_active:
                # QFont("Arial", 9, QFont.Bold)
                font = QFont()

                font.setBold(True)
                # font.setItalic(True)

                # font.setOverline(True)  # надчеркнутый
                # font.setStrikeOut(True)  # зачеркнутый
                # font.setUnderline(True)  # подчеркнутый

                # не понял!! --------------------
                # font.setStretch(5)
                # font.setCapitalization()

                return font

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        try:
            tc_cls = list(self.DATA.STAND.TCSc_LINE)[row]
        except:
            tc_cls = None

        row_is_summary: bool = tc_cls is None

        dut = None
        tc_inst = None
        if col in self.HEADERS.DUTS and not row_is_summary:
            index = col - self.HEADERS.DUTS.START_OUTER
            try:
                dut = self.DATA.STAND.DEV_LINES.DUT[index]
                # print(f"{tc_cls.TCSi_LINE=}/{index=}")
                tc_inst = tc_cls.TCSi_LINE[index]
            except:
                return True

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if row_is_summary:
                return True
            if col == self.HEADERS.SKIP:
                tc_cls.SKIP = value == Qt.Checked

            if col == self.HEADERS.ASYNC:
                tc_cls.ASYNC = value == Qt.Checked

            if col in self.HEADERS.DUTS:
                if tc_inst:
                    tc_inst.skip_tc_dut = value == Qt.Unchecked

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================
