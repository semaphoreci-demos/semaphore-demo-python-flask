from flask import render_template, flash, request, redirect, url_for, jsonify
import datetime
from bson.objectid import ObjectId
from semaphoreflask import app, mongo
from semaphoreflask.forms import CreateTaskForm


@app.route('/')
@app.route('/task/all')
def tasks_all():
    tasks_data = []
    if mongo:
        tasks = mongo.db.tasks.find()
        if tasks:
            for task in tasks:
                print(task)
                tasks_data.append({'task_id': task['_id'], 'task_title': task['task_title'], 'task_description': task['task_description'],
                'task_created_at': task['task_created_at']})
    return render_template('tasks_all.html', tasks= tasks_data, title='All Tasks')


@app.route('/task/new', methods = ['GET', 'POST'])
def task_new():
    form = CreateTaskForm()
    if form.validate_on_submit():
        task_title = form.task_title.data
        task_description = form.task_description.data
        task_created_at = datetime.datetime.now()
        mongo.db.tasks.insert_one({'task_title': task_title, 'task_description': task_description,
                                   'task_created_at': task_created_at})
        flash(f'Task { form.task_title.data } has been created successfully!', 'success')
        return redirect(url_for('tasks_all'))
    return render_template('task_create.html', title='Create New Task', form=form, operation='create')


@app.route('/task/<task_id>', methods = ['GET'])
def task_view(task_id):
    if len(task_id) == 24:
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            return render_template('task.html', task = [task], title='Task: {0}'.format(task['task_title']))
        else:
            return render_template('404.html')
    else:
        return render_template('404.html')


@app.route('/task/<task_id>/update', methods = ['GET', 'POST'])
def task_update(task_id): 
    if len(task_id) == 24:
        task_to_update = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task_to_update:
            form = CreateTaskForm()
            if form.validate_on_submit():
                mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, 
                                          { '$set' : {"task_title": form.task_title.data,
                                                      "task_description": form.task_description.data, 
                                                      "task_created_at": datetime.datetime.now()
                                                     }
                                          }, 
                                          upsert=False)
                flash(f'Task has been updated', 'success')
                return redirect(url_for('task_view', task_id=ObjectId(task_id)))
            elif request.method == 'GET':
                form.task_title.data = task_to_update['task_title']
                form.task_description.data = task_to_update['task_description']
                form.task_submit.data = 'Update Task'
        return render_template('task_create.html', title='Update task: {0}'.format(task_to_update['task_title']),
                               form=form, operation='update')
    else:
        return render_template('404.html')


@app.route('/task/<task_id>/delete', methods = ['POST'])
def task_delete(task_id):
    mongo.db.tasks.remove({"_id": ObjectId(task_id)})
    flash(f'Task has been deleted sucessfully', 'success')
    return redirect(url_for('tasks_all'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

