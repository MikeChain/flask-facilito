from flask import jsonify


def response(data: dict | list):
    return jsonify({
        'success': True,
        'data': data
    }), 200


def not_found():
    code = 404
    return jsonify({
        'success': False,
        'data': {},
        'message': 'Resource not found',
        'code': code
    }), code


def bad_request():
    code = 400
    return jsonify({
        'success': False,
        'data': {},
        'message': 'Bad request',
        'code': code
    }), code
