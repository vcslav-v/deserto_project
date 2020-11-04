"""Database tools."""

from datetime import datetime, timedelta
from random import choice

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from deserto import config, mail_tools, models
from deserto.config import SQLALCHEMY_DATABASE_URI, USER_MAIL

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)()


def make_fake_person() -> models.Person:
    """Make a fake person.

    Returns:
        Return new ready fake person
    """
    person = models.Person()
    fake = Faker(choice(config['person']['locals']))
    fake_person = fake.profile(sex=choice(config['person']['gender']))
    person.name = str(fake_person['name'])
    person.login = (
        fake_person['username'] + str(fake_person['birthdate'].year)
    )
    person.password = fake_person['ssn']
    person.gender = fake_person['sex']
    #  TODO user-agent maker
    person.email = mail_tools.make_email(USER_MAIL)
    return person


def update_queues():
    """Check queue. If empty - fulling."""
    if session.query(models.DribbbleQueue).count() == 0:
        persons = session.query(models.Person).all()
        for person in persons:
            session.add(models.DribbbleQueue(person=person))

    if session.query(models.TasksQueue).count() == 0:
        tasks = session.query(models.Task).all()
        for task in tasks:
            session.add(models.TasksQueue(task=task))

    session.commit()


def get_user_and_task():
    """Find person and taks for one.

    Returns:
        (Person, Task)
    """
    next_user_in_queue = session.query(
        models.DribbbleQueue,
    ).order_by(models.DribbbleQueue.id).with_for_update().first()
    if next_user_in_queue:
        user = next_user_in_queue.person
        session.delete(next_user_in_queue)
    else:
        user = None

    next_task_in_queue = session.query(
        models.TasksQueue,
    ).order_by(models.TasksQueue.id).with_for_update().first()
    if next_task_in_queue:
        task = next_task_in_queue.task
        session.delete(next_task_in_queue)
    else:
        task = None

    session.commit()

    if user and task and not ({task} - set(user.task)):
        return (user, None)

    return (user, task)


def get_real_user():
    """Find real person.

    Returns:
        Person
    """
    users = session.query(models.Person).filter_by(is_fake=False).all()
    for user in users:
        print(user.last_activity)
        rest_time = user.last_activity - datetime.utcnow()
        wait_time = timedelta(
            minutes=config.config['break']['real_users_rest'],
        )
        if rest_time > wait_time:
            user.last_activity = datetime.utcnow()
            session.add(user)
            return user
