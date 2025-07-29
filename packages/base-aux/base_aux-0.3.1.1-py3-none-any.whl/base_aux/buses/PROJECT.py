from typing import *


# =====================================================================================================================
class PROJECT:
    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "bus_user"
    KEYWORDS: list[str] = [
        "serial", "serial bus", "pyserial", "serial port", "com port", "comport", "rs232", "UART", "TTL",
        "serial client", "serial server", "serial emulator",
        "i2c",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "work with equipment over buses like Serial/i2c/... as client and server"
    DESCRIPTION_LONG: str = """
    ###
NOTE: IT SEEMS THIS IS OLD DATA! see tests for actual usage!
    
!. MOST APPROPRIATE COMMAND PROTOCOL
other protocols mot recommended

1. all cmds must be as params (preferred) in equipment or as special command
2. [<CMD_NAME>] - read param value or run special command  
    [IDN] - read value IDN  
    [DUMP] - run special command 
3. [<CMD_NAME> <VALUE>] - write value in parameter or run special cmd with param  
    [VOUT 12.3] - set value into parameter VOUT  
4. [<CMD_NAME> ?] - get available values to write into parameter  
    [MODE ?] - return [0 1 2 3]
5. all command sent must return answer  
    [OK] - if no value was asked
    [<VALUE>] - if asked some value, returned without measurement unit
    [FAIL] - any common not specified error
    [FAIL 0123] - any specified error without description
    [FAIL 02 VALUE OUT OF RANGE] - any specified error with description (full variant)
"""
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        ["[SerialClient]",
            "keep all found ports in base class!",
        ],
        ["Serial",
            "Client+Server",
            "connect with Enum__AddressAutoAcceptVariant FIRST_FREE/FIRST_FREE__ANSWER_VALID",
            "set/get params by SlashOrSpacePath addressing",
            "handle BackSpace send manually from terminal",
         ],
        ["SerialServer values",
         "as Callable",
         "ValueUnit",
         "ValueVariants",
         "list_results",
         ],
        ["SerialServer cmd",
         "NONE is equivalent for SUCCESS",
         "no need params (like line_parsed as before)",
         "help - for show all variants (Units/Variants/Callables)!"
         ]
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 4, 16)
    TODO: list[str] = [
        "add all other port settings into SerialClient",
        "fix all tests! fix EMU",
    ]
    FIXME: list[str] = [
        "add timeout into connect for AndreiK bluetooth comports stack",
    ]
    NEWS: list[str] = [
        "[SerialClient.writeReadLast*] fix timeoutRead on only first read! after first char timeout set default",
    ]


# =====================================================================================================================
