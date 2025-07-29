from typing import *
from base_aux.testplans.devices import *
from base_aux.buses.m1_serial2_client_derivatives import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid, Base_Device):  # IMPORTANT! KEEP Serial FIRST Nesting!
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    EOL__SEND = b"\n"

    REWRITEIF_READNOANSWER = 0
    REWRITEIF_NOVALID = 0

    # INFO --------------------------------
    NAME: str = "PTB"
    DESCRIPTION: str = "PTB for PSU"

    # @property
    # def DUT_SN(self) -> str:      # TODO: USE DIRECT FINDING!!!???
    #     return f"SN_{self.INDEX}"

    def __init__(self, index: int = None, **kwargs):    # FIXME: decide to delete this!!!
        """
        :param index: None is only for SINGLE!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    # DETECT --------------------------------
    @property
    def DEV_FOUND(self) -> bool:
        return self.address_check__resolved()

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX+1:02d}:"

    # def address__validate(self) -> bool:  # NO NEED! only for manual!
    #     result = (
    #             self.write_read__last_validate("get name", self.NAME, prefix="*:")
    #             and
    #             self.write_read__last_validate("get addr", EqValid_NumParsedSingle_Success(self.INDEX+1), prefix="*:")
    #             # and
    #             # self.write_read__last_validate("get prsnt", "0")
    #     )
    #     if result:
    #         self.dev__load_info()
    #
    #     return result

    def dev__load_info(self) -> None:
        if not self.SN:
            self.SN = self.write_read__last("get SN")
            self.FW = self.write_read__last("get FW")
            self.MODEL = self.write_read__last("get MODEL")

            self.DUT_SN = self.write_read__last("get PSSN")
            self.DUT_FW = self.write_read__last("get PSFW")
            self.DUT_MODEL = self.write_read__last("get PSMODEL")

    def connect__validate(self) -> bool:
        result = (
            self.address_check__resolved()  # fixme: is it really need here???
            and
            self.write_read__last_validate("get prsnt", "1")
        )
        if result:
            self.dev__load_info()

        return result


# =====================================================================================================================
class DeviceDummy(SerialClient_FirstFree_AnswerValid, Base_Device):  # IMPORTANT! KEEP Serial FIRST Nesting!
    @property
    def DEV_FOUND(self) -> bool:
        return True

    def address__validate(self) -> bool:
        return True

    def connect__validate(self) -> bool:
        return True

    def connect(self, *args, **kwargs) -> bool:
        return True


# =====================================================================================================================
def _explore():
    pass

    # emu = Ptb_Emulator()
    # emu.start()
    # emu.wait()

    dev = Device(0)
    print(f"{dev.connect()=}")
    print(f"{dev.ADDRESS=}")
    print(f"{dev.address_check__resolved()=}")

    if not dev.address_check__resolved():
        return

    # dev.write_read__last("get sn")
    # dev.write_read__last("get fru")
    # dev.write_read__last("test sc12s")
    # dev.write_read__last("test ld12s")
    # dev.write_read__last("test gnd")
    # dev.write_read__last("test")
    # dev.write_read__last("get status")
    # dev.write_read__last("get vin")


if __name__ == "__main__":
    _explore()


# =====================================================================================================================
