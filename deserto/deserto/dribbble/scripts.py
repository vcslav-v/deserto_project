"""Tools for dribbble."""

from deserto import (data_base, mail_tools,  # noqa I001
                    models, resource_tools, web_browser)  # noqa WPS318
from deserto.config import config
from deserto.dribbble import tools, web_scripts
from datetime import datetime
from time import sleep

dribbble_cfg = config['dribbble']


def make_user(task: models.Task):
    """Make new user and sign in on Dribbble.

    Parameters:
        task: for registration task
    """
    user = data_base.make_fake_person()
    browser = web_browser.WebDriver(
        user=user,
        proxy=True,
    )
    try:
        is_sign_in = web_scripts.sign_in(user, browser)
    except Exception:
        is_sign_in = False

    if is_sign_in:
        user.is_dribbble_user = True

        try:
            web_scripts.set_userpic(browser)
        except Exception:
            user.is_dribbble_set_pic = False
        else:
            user.is_dribbble_set_pic = True

        try:
            user.is_dribbble_email_confirm = tools.is_email_confirm(user.email)
        except Exception:
            user.is_dribbble_email_confirm = False

        tools.save_cookies(user, browser.driver.get_cookies())
        task.counter -= 1
        data_base.session.add(task)
    browser.driver.close()


def like_and_comment(user: models.Person, task: models.Task):
    """Do dribbble tasks.

    Parameters:
        user: dribbble user
        task: dribbble task
    """
    print('browser')
    browser = tools.get_dribbble_ready_browser(user)
    # if not browser or not browser.is_successful:
    #     return
    # elif not browser.is_successful:
    #     browser.driver.close()
    #     sleep(config['break']['long'])
    print('is_successful')
    if task.is_liked_task:
        print(task)
        web_scripts.like(browser, task)
    user.task.append(task)
    tools.save_cookies(user, browser.driver.get_cookies())
    browser.driver.close()


def do_real_user_flow(user: models.Person):
    """Real user live flow.

    Parameters:
        user: dribbble user
    """
    browser = tools.get_dribbble_ready_browser(user, proxy=False)
    if not browser:
        return
    unliked_urls = web_scripts.get_unliked_shots(browser)
    if unliked_urls:
        for url in unliked_urls:
            task = models.Task(
                url=url,
                counter=1,
            )
            web_scripts.like(browser, task)
    user.last_activity = datetime.utcnow()
    data_base.session.add(user)
