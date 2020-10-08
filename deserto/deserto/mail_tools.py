"""Mail tools."""

import imaplib
from random import choice

from deserto.config import PASS_MAIL, USER_MAIL, config


def get_mail() -> imaplib.IMAP4_SSL:
    """Get email confirmation link.

    Returns:
        mails in inbox
    """
    mail = imaplib.IMAP4_SSL(config['mail']['imap'])
    mail.login(USER_MAIL, PASS_MAIL)
    mail.list()
    mail.select('inbox')
    return mail


def make_email(email: str) -> str:
    """Make a new email-address with random dots.

    Parameters:
        email: email-address in format {name}@{domain}

    Returns:
        Email-address
    """
    name, domain = email.split('@')

    empty_and_dot = ('', '.')
    new_email = [char + choice(empty_and_dot) for char in name[:-1]]
    new_email.extend([name[-1], '@', domain])

    return ''.join(new_email)
