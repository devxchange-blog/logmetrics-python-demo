from flask import Flask, jsonify, abort, request, make_response, url_for, g
# from flask_httpauth import HTTPBasicAuth
from logmetrics_sdk.logmetrics import LogMetrics
import logging


app = Flask(__name__, static_url_path="")

# auth = HTTPBasicAuth()
logging.basicConfig(level=logging.DEBUG)


# @auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


# @auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@LogMetrics
@app.route('/todo/api/v1/tasks', methods=['GET'])
# @auth.login_required
@LogMetrics
def get_tasks():
    return jsonify(tasks)


@app.route('/todo/api/v1/tasks/<int:task_id>', methods=['GET'])
# @auth.login_required
@LogMetrics
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})


@app.route('/todo/api/v1/tasks', methods=['POST'])
# @auth.login_required
@LogMetrics
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)})


@app.route('/todo/api/v1/tasks/<int:task_id>', methods=['DELETE'])
# @auth.login_required
@LogMetrics
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
