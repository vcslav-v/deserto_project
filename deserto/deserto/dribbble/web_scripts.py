"""Tools for dribbble."""

from time import sleep
from typing import List

from deserto import (data_base, mail_tools,  # noqa I001
                     models, resource_tools, web_browser)  # noqa WPS318
from deserto.config import config
from deserto.logger import logger

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
    browser.fill_forms(
        dribbble_cfg['xpath']['profile']['fields'],
        userpic_path=resource_tools.get_userpic_path(),
    )
    browser.click(dribbble_cfg['xpath']['profile']['userpic_submit'])
    sleep(config['break']['long'])


def like(browser: web_browser.WebDriver, task: models.Task):
    """Like dribbble item.

    Parameters:
        browser: ready for dribbble
        task: like task
    """
    logger.info('Заходим на {url}'.format(url=task.url))
    browser.driver.get(task.url)
    sleep(config['break']['short'])
    try:
        logger.info('Лайкаем')
        browser.click(dribbble_cfg['xpath']['item']['like'])
    except Exception:
        task.counter += 1
    else:
        task.counter -= 1


def get_unliked_shots(browser: web_browser.WebDriver) -> List[str]:
    """Find unliked shots.

     Parameters:
        browser: ready for dribbble

    Returns:
        list of urls with unlike shots
    """
    browser.driver.get(dribbble_cfg['url']['recent'])
    attempt = 0
    attempts = config['common']['attempts']
    while attempt < attempts:
        urls = resource_tools.get_dont_like_urls(browser.driver.page_source)
        if urls:
            return urls
        browser.driver.execute_script(
            'window.scrollTo(0, 100);',
        )
        sleep(config['break']['long'])
        attempt += 1
