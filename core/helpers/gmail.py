import re
import time
import imaplib
import email as email_lib
from typing import Optional
from email.message import Message
from datetime import datetime as dt, timedelta as td


def get_confirmation_code(
    email: str,
    password: str,
    sent_time_utc: dt = dt.utcnow(),
    wait_timeout: int = 60,
) -> str:
    imap_url = "imap.gmail.com"
    conn: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(host=imap_url)
    conn.login(user=email, password=password)
    conn.select(mailbox="INBOX")
    criteria = (
        "FROM info@x.com",
        f"SINCE {sent_time_utc.strftime('%d-%b-%Y')}",
    )
    msg = _get_latest_email_message(conn, *criteria)
    start = time.time()
    while (
        abs(_get_email_date(msg) - sent_time_utc) > td(minutes=1)
        and time.time() - start < wait_timeout
    ):
        time.sleep(3)
        conn.noop()
        msg = _get_latest_email_message(conn, *criteria)

    match = re.search(
        r"by entering the following single-use code\.\n\n(\w{8})\n\n",
        msg.get_payload()[0].as_string(),
    )
    return match.groups()[0]


def _get_latest_email_message(conn: imaplib.IMAP4_SSL, *criteria) -> Optional[Message]:
    _, ids = conn.search(None, *criteria)
    if ids:
        latest_id = ids[0].split()[-1].decode()
        body = conn.fetch(message_set=latest_id, message_parts="(RFC822)")[1][0][1]
        msg: email_lib.message.Message = email_lib.message_from_bytes(s=body)
    else:
        msg = None
    return msg


def _get_email_date(msg: email_lib.message.Message) -> dt:
    date_string = re.findall(r"\d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2}", msg["Date"])[0]
    return dt.strptime(date_string, "%d %b %Y %H:%M:%S")
