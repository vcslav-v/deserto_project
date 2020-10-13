"""Manage resourse tools."""

import os
import re
from random import choice

import requests
from bs4 import BeautifulSoup

from deserto import data_base, models
from deserto.config import config


def get_soup(url: str) -> BeautifulSoup:
    """Do beautiful soup from url.

    Parameters:
        url: target url

    Returns:
        beautiful soup
    """
    response = requests.get(config['dribbble']['url']['recent'])
    return BeautifulSoup(response.text)


def download_new_user_pics():  # noqa WPS210
    """Download user pics from dribbble."""
    soup = get_soup(config['dribbble']['url']['recent'])
    for a_tag in soup.find_all('a', attrs={'rel': 'contact'}):
        print(a_tag)
        img_url = a_tag.img.attrs['src']
        img_url = img_url.replace('mini', 'normal')
        print(img_url)
        names = re.search(config['dribbble']['regex']['userpic'], img_url)
        print(names)

        if not os.path.exists(config['path']['userpic']):
            os.mkdir(config['path']['userpic'])

        img = requests.get(img_url)
        with open(
            os.path.join(config['path']['userpic'], names[1]),
            'wb',
        ) as image_file:
            image_file.write(img.content)


def get_userpic_path() -> str:
    """Choice a userpic from local storage.

    Returns:
        path to userpic image
    """
    list_dir = os.listdir(config['path']['userpic'])
    if len(list_dir) < data_base.session.query(models.Person).count():
        download_new_user_pics()
        list_dir = os.listdir(config['path']['userpic'])

    userpics_path = list(filter(
        lambda img: img.split('.')[-1].lower() in (
            config['common']['img_extension']
        ),
        list_dir,
    ))
    return os.path.join(config['path']['userpic'], choice(userpics_path))
