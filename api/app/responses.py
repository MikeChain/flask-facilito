from flask import jsonify

def response(data: dict | list):
    return jsonify({
        'success': True,
        'data': data
    }), 200