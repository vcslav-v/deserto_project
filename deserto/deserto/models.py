"""SQLAlchemy models."""
from datetime import datetime

from sqlalchemy import (ARRAY, JSON, Boolean, Column,
                        DateTime, ForeignKey, Integer, String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


association_table = Table(
    'association',
    Base.metadata,
    Column('person_id', Integer, ForeignKey('person.id', ondelete="CASCADE")),
    Column('task_id', Integer, ForeignKey('task.id', ondelete="CASCADE")),
)


class Person(Base):
    """Web person."""

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)  # noqa WPS125
    name = Column(String)
    login = Column(String)
    email = Column(String)
    password = Column(String)
    gender = Column(String(length=1))
    user_agent = Column(String)
    cookies = Column(ARRAY(JSON), default=[])
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_fake = Column(Boolean, default=True)
    is_dribbble_user = Column(Boolean, default=False)
    is_dribbble_email_confirm = Column(Boolean, default=False)
    is_dribbble_set_pic = Column(Boolean, default=False)
    dribbble_queue = relationship(
        'DribbbleQueue',
        uselist=False,
        back_populates='person',
    )
    task = relationship(
        'Task',
        secondary=association_table,
        back_populates='person',
        cascade="all, delete",
    )


class DribbbleQueue(Base):
    """Queue person ready for dribbble work."""

    __tablename__ = 'dribbble_queue'

    id = Column(Integer, primary_key=True)  # noqa WPS125
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='dribbble_queue')


class Task(Base):
    """Task for workers."""

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)  # noqa WPS125
    url = Column(String(length=100))
    counter = Column(Integer)
    is_dribbble_reg = Column(Boolean, default=False)
    is_liked_task = Column(Boolean, default=False)
    person = relationship(
        'Person',
        secondary=association_table,
        back_populates='task',
    )
    tasks_queue = relationship(
        'TasksQueue',
        uselist=False,
        back_populates='task',
    )

    def is_done(self) -> bool:
        """Check task counter.

        Returns:
            If task done True, overwise False
        """
        return self.counter <= 0


class TasksQueue(Base):
    """Queue tasks."""

    __tablename__ = 'tasks_queue'

    id = Column(Integer, primary_key=True)  # noqa WPS125
    task_id = Column(Integer, ForeignKey('task.id'))
    task = relationship('Task', back_populates='tasks_queue')
