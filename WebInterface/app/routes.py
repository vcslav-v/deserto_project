from flask import flash, redirect, render_template, url_for

from app import app, session, models
from app.forms import AddDribbbleTaskForm, AddFakePersonsForm


@app.route('/', methods=['GET', 'POST'])
def index():
    add_dribbble_form = AddDribbbleTaskForm()
    add_person_form = AddFakePersonsForm()
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
        'index.html',
        title='Deserto 0.1.0',
        add_dribbble_form=add_dribbble_form,
        add_person_form=add_person_form
    )

@app.route('/info')
def info():
    tasks = session.query(models.Task).all()
    persons = session.query(models.Person).all()
    return render_template('info.html', tasks=tasks, persons=persons)