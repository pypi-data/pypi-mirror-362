from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib

from base_aux.alerts.m1_alert0_base import *
from base_aux.privates.m1_privates import *
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class SmtpServers:
    """well known servers addresses.

    Here we must collect servers like MilRu/GmailCom, and not to create it in any new project.
    """
    MAIL_RU: AttrKit_AddrPort = AttrKit_AddrPort("smtp.mail.ru", 465)


# =====================================================================================================================
class AlertSmtp(Base_Alert):
    """
    GOAL
    ----
    SMTP realisation for sending msg (email).

    :param _subtype: reuse new _subtype instead of default
    """
    # SETTINGS ------------------------------------
    CONN_ADDRESS: AttrKit_AddrPort = SmtpServers.MAIL_RU
    CONN_AUTH: AttrKit_AuthNamePwd = PvLoaderIni_AuthNamePwd(keypath=("AUTH_EMAIL_DEF",))
    TIMEOUT_SEND = 5

    # AUX -----------------------------------------
    _conn:  smtplib.SMTP_SSL
    _subtype: str = "plain"
    SUBJECT: str = None

    def __init__(self, *args, _subtype: str = None, subject: str = None, **kwargs):
        if _subtype is not None:
            self._subtype = _subtype
        if subject is not None:
            self.SUBJECT = subject

        super().__init__(*args, **kwargs)

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = smtplib.SMTP_SSL(self.CONN_ADDRESS.ADDR, self.CONN_ADDRESS.PORT, timeout=self.TIMEOUT_SEND)
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        response = self._conn.login(self.CONN_AUTH.NAME, self.CONN_AUTH.PWD)
        print(response)
        print("=" * 100)
        return response and response[0] in [235, 503]

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(self._msg_compose())
        return True

    def _msg_compose(self) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.CONN_AUTH.NAME
        msg["To"] = self.RECIPIENT
        msg['Subject'] = self.SUBJECT or self.__class__.__name__

        try:
            _subtype = self.MSG_ACTIVE["_subtype"]
        except:
            _subtype = self._subtype
        msg.attach(MIMEText(self.MSG_ACTIVE, _subtype=_subtype))
        return msg

    def _recipient_get(self) -> str:
        return self.CONN_AUTH.NAME


# =====================================================================================================================
if __name__ == "__main__":
    victim = AlertSmtp()
    victim.send_msg("hello")
    victim.send_msg("hello2")
    victim.wait()
    victim.send_msg("hello3")
    victim.wait()


# =====================================================================================================================
