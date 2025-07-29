from typing import *

from base_aux.testplans import *
from base_aux.buses.m1_serial1_client import *

from base_aux.breeders.m3_table_inst import *

from .models import *


# =====================================================================================================================
class Base_Device:
    NAME: str = None
    DESCRIPTION: str = None
    INDEX: int = None

    # PROPERTIES ------------------------------------------------------------------------------------------------------
    DEV_FOUND: bool | None = None

    SN: str = None
    FW: str = None
    MODEL: str = None

    # DUT --------------------
    SKIP: Optional[bool] = None

    DUT_SN: str = None
    DUT_FW: str = None
    DUT_MODEL: str = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, index: int = None, **kwargs):
        """
        :param index: None is only for SINGLE!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

    # CONNECT ---------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    # INFO ------------------------------------------------------------------------------------------------------------
    def dev__load_info(self) -> None:
        """
        GOAL
        ----
        load all important attrs in object.
        for further identification.

        WHERE
        -----
        useful in connect_validate
        """
        pass

    def dev__get_info(self) -> dict[str, Any]:
        """
        GOAL
        ----
        get already loaded data!
        """
        result = {
            "DEV_FOUND": self.DEV_FOUND,
            "INDEX": self.INDEX,
            "SKIP": self.SKIP,

            "NAME": self.NAME or self.__class__.__name__,
            "DESCRIPTION": self.DESCRIPTION or self.__class__.__name__,
            "SN": self.SN or "",
            "FW": self.FW or "",
            "MODEL": self.MODEL or "",

            "DUT_SN": self.DUT_SN or "",
            "DUT_FW": self.DUT_FW or "",
            "DUT_MODEL": self.DUT_MODEL or "",
        }
        return result


# =====================================================================================================================
class DeviceKit(TableKit):
    def __del__(self):
        self.disconnect()

    def connect(self) -> None:
        self("connect")

    def disconnect(self) -> None:
        self("disconnect")

    # -----------------------------------------------------------------------------------------------------------------
    def resolve_addresses(self) -> None:
        """
        GOAL
        ----
        find all devices on Uart ports
        """
        pass


# =====================================================================================================================
class _DeviceColumn_Example(TableColumn):
    """
    NOTE
    ----
    use direct dinamic creation TableColumn(index, TLines)!

    GOAL
    ----
    just an example
    """
    LINES = DeviceKit()


# =====================================================================================================================
