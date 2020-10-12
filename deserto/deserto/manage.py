#!/usr/bin/env python3
"""Deserto manage app."""

from deserto import data_base
from deserto.dribbble import scripts


def main():
    """Check tasks and up workers."""
    #  data_base.up()
    data_base.update_queues()
    user, task = data_base.get_user_and_task()
    if not task:
        return
    if task.is_liked_task:
        scripts.like_and_comment(user, task)
    elif task.is_dribbble_reg:
        scripts.make_user(task)
    if task.is_done():
        data_base.session.delete(task)
    data_base.session.commit()


if __name__ == '__main__':
    main()
