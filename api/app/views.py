from flask import Blueprint, request
from .responses import response, not_found, bad_request
from .models.task import Task

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')


@api_v1.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()

    return response(
        [task.serialize() for task in tasks]
    )


@api_v1.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.filter_by(id=id).first()

    if task:
        return response(task.serialize())

    return not_found()


@api_v1.route('/tasks', methods=['POST'])
def create_tasks():
    json = request.get_json(force=True)

    if json.get('title') is None or len(json['title']) > 50:
        return bad_request()

    if json.get('description') is None:
        return bad_request()

    if json.get('deadline') is None:
        return bad_request()

    t = Task.new(**json)
    if t.save():
        return response(t.serialize())

    return bad_request()


@api_v1.route('/tasks/<id>', methods=['PUT'])
def update_tasks(id):
    task = Task.query.filter_by(id=id).first()

    if task:
        json = request.get_json(force=True)
        task.title = json.get('title', task.title)
        task.description = json.get('description', task.description)
        task.deadline = json.get('deadline', task.deadline)

        if task.save():
            return response(task.serialize())

        return bad_request()

    return not_found()


@api_v1.route('/tasks/<id>', methods=['DELETE'])
def delete_tasks(id):
    task = Task.query.filter_by(id=id).first()

    if task:
        if task.delete():
            return response(task.serialize())

        return bad_request()

    return not_found()
