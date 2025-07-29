from base_aux.base_nest_dunders.m1_init0_reinit2_lambdas_resolve import NestInit_AttrsLambdaResolve
from base_aux.privates.m1_privates import *
from base_aux.aux_attr.m4_kits import *
from base_aux.alerts.m1_alert0_base import *

import telebot


# =====================================================================================================================
class RecipientTgID(Base_AttrKit):
    MyTgID: str


# =====================================================================================================================
class AlertTelegram(Base_Alert):
    """realisation for sending Telegram msg
    """
    # SETTINGS ------------------------------------
    CONN_ADDRESS: AttrKit_AuthNamePwd = PvLoaderIni_AuthTgBot(keypath=("TGBOT_DEF", ))
    RECIPIENT: AttrKit_AuthNamePwd = PvLoaderIni(target=RecipientTgID, keypath=("TG_ID",))

    # AUX -----------------------------------------
    _conn: telebot.TeleBot

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = telebot.TeleBot(token=self.CONN_ADDRESS.TOKEN)
        return True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(chat_id=self.RECIPIENT.MyTgID, text=self._msg_compose())
        return True


# =====================================================================================================================
if __name__ == "__main__":
    victim = AlertTelegram()
    victim.send_msg("hello")
    victim.send_msg("hello2")
    victim.wait()
    victim.send_msg("hello3")
    victim.wait()


# =====================================================================================================================
