import os

from flask import flash, redirect, render_template, url_for

from app import app, models, session
from app.forms import AddDribbbleTaskForm, DeleteTask


@app.route('/', methods=['GET', 'POST'])
def index():
    add_dribbble_form = AddDribbbleTaskForm()
    tasks = session.query(models.Task).filter_by(is_liked_task=True).all()
    if add_dribbble_form.validate_on_submit():
        session.add(
            models.Task(
                url=add_dribbble_form.url.data,
                counter=add_dribbble_form.amount_like.data,
                is_liked_task=True
            )
        )
        session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        title='Deserto 0.1.0',
        add_dribbble_form=add_dribbble_form,
        tasks=tasks
    )


@app.route('/info')
def info():
    tasks = session.query(models.Task).all()
    persons = session.query(models.Person).all()
    return render_template('info.html', tasks=tasks, persons=persons)


@app.route('/update')
def db_up():
    os.system('alembic revision --autogenerate')
    os.system('alembic upgrade head')
    return redirect(url_for('index'))
