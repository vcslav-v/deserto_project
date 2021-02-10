"""Browser tools."""

import json
from random import choice
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from deserto.config import (ANTICAPTCHA_TOKEN,  # noqa I001
                            PROXY_GET_JSON_URL, URL_SELENOID, config)  # noqa WPS318
from deserto.models import Person


class WebDriver(object):
    """Browser driver."""

    def __init__(
        self,
        user: Person = None,
        proxy: bool = False,
    ) -> webdriver:
        """Open the browser and set the necessary parameters.

        Parameters:
            user: person for register
            proxy: flag use proxy
        """
        capabilities = {
            'browserName': 'chrome',
            'version': '86.0',
            'enableVNC': True,
            'enableVideo': False,
        }
        print('options')
        browser_options = webdriver.chrome.options.Options()
        if user and user.user_agent:
            browser_options.add_argument(
                'user-agent={user_agent}'.format(user_agent=user.user_agent),
            )
        if proxy:
            browser_options.add_argument(
                'proxy-server={proxy}'.format(proxy=get_proxy()),
            )

        browser_options.add_extension(config['anticaptcha']['name'])
        print('Remote')
        self.driver = webdriver.Remote(
            command_executor=URL_SELENOID,
            desired_capabilities=capabilities,
        )
        print('anticaptcha')
        self.driver.get(config['anticaptcha']['blank_url'])
        message = {
            'receiver': 'antiCaptchaPlugin',
            'type': 'setOptions',
            'options': {'antiCaptchaApiKey': ANTICAPTCHA_TOKEN},
        }
        if self.is_on_page_xpath(config['anticaptcha']['xpath']['check']):
            self.driver.execute_script(
                'return window.postMessage({message});'.format(
                    message=json.dumps(message),
                ),
            )
            sleep(config['break']['middle'])
            self.is_successful = True
        else:
            self.is_successful = False

    def is_on_page_xpath(self, xpath: str) -> bool:
        """Find xpath on the current page.

        Parameters:
            xpath: xpath for find on current page

        Returns:
            If found one - True, otherwise False
        """
        try:
            self.driver.find_element_by_xpath(xpath)
        except Exception:
            return False
        return True

    def fill_forms(self, instuctions: dict, **kwards):
        """Fill forms on the current page.

        Parameters:
            instuctions: dict in format {keyword_for_insert:'xpath'}
            kwards: dict for format instuctions
        """
        #  TODO instuctions discription all form in page,
        #  but we must fill only kwards-forms

        for name, xpath in instuctions.items():
            element = self.driver.find_element_by_xpath(xpath)
            element.send_keys(kwards[name])
            sleep(config['break']['short'])

    def click(self, xpath: str):
        """Click to element.

        Parameters:
            xpath: xpath element
        """
        element = self.driver.find_element_by_xpath(xpath)
        element.click()
        sleep(config['break']['middle'])

    def set_cookies(self, user: Person, url: str):
        """Set person cookies.

        Parameters:
            user: user with cookies
            url: target domain
        """
        self.driver.get(url)
        #  TODO добавить проверку по url
        for cookie in user.cookies:
            if cookie.get('expiry'):
                try:
                    cookie['expiry'] = int(cookie['expiry'])
                except ValueError:
                    continue

            self.driver.add_cookie(cookie)

    def wait_xpath(
        self,
        xpath: str,
        timeout: int = config['break']['for_wait'],  # noqa WPS404
    ) -> bool:
        """Wait for xpath to appear.

        Parameters:
            xpath: xpath element for waiting
            timeout: seconds for waiting

        Returns:
            If waited - True, otherwise False
        """
        try:
            WebDriverWait(
                self.driver,
                timeout,
            ).until(lambda element: element.find_element_by_xpath(xpath))
        except Exception:
            return False
        return True


def get_proxy() -> str:
    """Get new proxy.

    Returns:
        proxy in format IP PORT
    """
    response = requests.get(PROXY_GET_JSON_URL)
    proxies = json.loads(response.text)
    proxy = choice(proxies)
    return '{hostname}:{port}'.format(**proxy)
