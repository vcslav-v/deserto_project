"""Tools for dribbble."""

import re
from typing import List

import requests
from deserto import (data_base, mail_tools,  # noqa I001
                     models, resource_tools, web_browser)  # noqa WPS318

from deserto.config import config

dribbble_cfg = config['dribbble']


def is_email_confirm(email: str) -> bool:
    """Confirm email.

    Parameters:
        email: unique TO field

    Returns:
        if Confirm email - true, otherwise False
    """
    response = requests.get(get_confirmation_link(email))
    return response.ok


def get_confirmation_link(email: str) -> str:
    """Get confirmation link from email.

    Parameters:
        email: unique TO field

    Returns:
        link for сonfirmation email
    """
    mail = mail_tools.get_mail()
    _, uids = mail.uid('search', None, 'TO', "'{email}'".format(email=email))
    latest_email_uid = uids[0].split()[-1]
    _, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    link_confirm = re.findall(
        dribbble_cfg['regex']['email_confirm'],
        str(email_data[0][1]),
    )
    return link_confirm[2].replace(r'=\r\n', '')


def save_cookies(
    person: models.Person,
    cookies: List[dict],
):
    """Save person cookies and return to queue.

    Parameters:
        person: who need return to queue
        cookies: what need save
    """
    #  TODO do not remove all old cookies
    person.cookies = cookies
    data_base.session.add(person)


def get_dribbble_ready_browser(user, proxy=True) -> web_browser.WebDriver:
    """Ready up browser with user cookies.

    Parameters:
        user: person with dribbbler cookies

    Returns:
        browser with set cookies user or None
    """
    try:
        browser = web_browser.WebDriver(user=user, proxy=proxy)
    except Exception as e:
        print(e)
        return None

    try:
        browser.set_cookies(
            user, dribbble_cfg['url']['main'],
        )
    except Exception as e:
        print(e)
        browser.driver.close()
        return None

    browser.driver.get(
        dribbble_cfg['url']['main'] + user.login,
    )
    xpath_check_session = dribbble_cfg['xpath']['new_session']['check_done']
    print(browser.is_on_page_xpath(xpath_check_session))
    if browser.is_on_page_xpath(xpath_check_session):
        return browser

    browser.driver.get(dribbble_cfg['url']['new_session'])
    browser.fill_forms(
        dribbble_cfg['xpath']['new_session']['fields'],
        login=user.login,
        password=user.password,
    )
    browser.click(dribbble_cfg['xpath']['new_session']['submit'])

    if browser.wait_xpath(xpath_check_session):
        return browser
