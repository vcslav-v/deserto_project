import os

from flask import flash, redirect, render_template, url_for

from app import app, models, session
from app.forms import (AddDribbbleTaskForm, AddFakePersonsForm,
                       AddRealPersonsForm)


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
        title='Deserto 0.2.0',
        add_dribbble_form=add_dribbble_form,
        tasks=tasks
    )


# @app.route('/secret')
# def secret():
#     queue = session.query(models.DribbbleQueue).all()
#     return render_template('secret.html', queue=queue)


@app.route('/add-acc',  methods=['GET', 'POST'])
def add_acc():
    add_person_form = AddRealPersonsForm()
    persons = session.query(models.Person).filter_by(is_fake=False).all()
    if add_person_form.validate_on_submit():
        session.add(
            models.Person(
                name=add_person_form.name.data,
                login=add_person_form.login.data,
                password=add_person_form.password.data,
                is_fake=False,
            )
        )
        session.commit()
        flash('New user have been saved.')
        return redirect(url_for('add_acc'))
    return render_template(
        'add_acc.html',
        title='Deserto 0.2.0',
        add_person_form=add_person_form,
        persons=persons,
    )


@app.route('/info')
def info():
    queue = session.query(models.DribbbleQueue).all()
    return render_template('info.html', queue=queue)


@app.route('/delete-person/<person_id>')
def delete_person(person_id):
    try:
        person_id = int(person_id)
    except Exception:
        return redirect(url_for('index'))
    person = session.query(models.Person).filter_by(id=person_id).first()
    session.delete(person)
    session.commit()
    return redirect(url_for('add_acc'))


@app.route('/delete-task/<task_id>')
def delete_task(task_id):
    try:
        task_id = int(task_id)
    except Exception:
        return redirect(url_for('index'))
    task = session.query(models.Task).filter_by(id=task_id).first()
    session.delete(task)
    session.commit()
    return redirect(url_for('index'))


@app.route('/update')
def db_up():
    os.system('alembic revision --autogenerate')
    os.system('alembic upgrade head')
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    add_person_form = AddFakePersonsForm()
    tasks = session.query(models.Task).filter_by(is_dribbble_reg=True).all()
    if add_person_form.validate_on_submit():
        session.add(
            models.Task(
                counter=add_person_form.amount_persons.data,
                is_dribbble_reg=True
            )
        )
        session.commit()
        print(add_person_form.amount_persons.data)
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template(
        'admin.html',
        title='Deserto 0.2.0',
        add_person_form=add_person_form,
        tasks=tasks,
    )
