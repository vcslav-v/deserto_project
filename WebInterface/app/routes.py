import os

from flask import flash, redirect, render_template, url_for

from app import app, models, session
from app.forms import AddDribbbleTaskForm, AddFakePersonsForm


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


@app.route('/secret')
def secret():
    persons = session.query(models.DribbbleQueue).all()
    return render_template('secret.html', persons=persons)


@app.route('/info')
def info():
    queue = session.query(models.DribbbleQueue).all()
    return render_template('info.html', queue=queue)


@app.route('/delete-task/<task_id>')
def delete_task(task_id):
    try:
        task_id = int(task_id)
    except:
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
        title='Deserto 0.1.0',
        add_person_form=add_person_form,
        tasks=tasks,
    )
