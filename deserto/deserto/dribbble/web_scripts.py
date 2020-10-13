"""Tools for dribbble."""

from time import sleep

from deserto import (data_base, mail_tools,  # noqa I001
                     models, resource_tools, web_browser)  # noqa WPS318
from deserto.config import config

dribbble_cfg = config['dribbble']


def sign_in(user, browser: web_browser.WebDriver) -> bool:
    """Register user on Dribble.

    Parameters:
        user: User object
        browser: Browser object

    Returns:
        If successful - True otherwise False
    """
    xpath_sign_in = config['dribbble']['xpath']['sign_in']
    browser.driver.get(dribbble_cfg['url']['sign_in'])

    if browser.is_on_page_xpath(  # noqa WPS337
        xpath_sign_in['check_old_browser'],
    ):
        return False

    browser.fill_forms(
        xpath_sign_in['fields'],
        name=user.name,
        login=user.login,
        email=user.email,
        password=user.password,
    )

    browser.click(xpath_sign_in['checkbox'])
    browser.click(xpath_sign_in['submit'])

    if browser.wait_xpath(xpath_sign_in['check_done']):
        return True
    return False


def set_userpic(browser: web_browser.WebDriver):
    """Set userpic in user profile.

    Parameters:
        browser: with user cookies
    """
    browser.driver.get(dribbble_cfg['url']['profile'])
    print('get')
    browser.fill_forms(
        dribbble_cfg['xpath']['profile']['fields'],
        userpic_path=resource_tools.get_userpic_path(),
    )
    print('fill')
    browser.click(dribbble_cfg['xpath']['profile']['userpic_submit'])
    print('click')
    sleep(config['break']['long'])


def like(browser: web_browser.WebDriver, task: models.Task):
    """Like dribbble item.

    Parameters:
        browser: ready for dribbble
        task: like task
    """
    browser.driver.get(task.url)
    sleep(config['break']['short'])
    try:
        browser.click(dribbble_cfg['xpath']['item']['like'])
    except Exception:
        task.counter += 1
    else:
        task.counter -= 1
