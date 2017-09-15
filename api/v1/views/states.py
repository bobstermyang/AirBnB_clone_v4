#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models import storage, CNC


@app_views.route('/states',
                 methods=['GET', 'POST'])
@swag_from('swagger_yaml/states_no_id_get.yml', methods=['GET'])
@swag_from('swagger_yaml/states_no_id_post.yml', methods=['POST'])
def states_no_id():
    """
        states route to handle http method for requested states no id provided
    """
    if request.method == 'GET':
        all_states = storage.all('State')
        all_states = list(obj.to_json() for obj in all_states.values())
        return jsonify(all_states)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        State = CNC.get("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/states_id_get.yml', methods=['GET'])
@swag_from('swagger_yaml/states_id_del.yml', methods=['DELETE'])
@swag_from('swagger_yaml/states_id_put.yml', methods=['PUT'])
def states_with_id(state_id=None):
    """
        states route to handle http method for requested state by id
    """
    state_obj = storage.get('State', state_id)

    if request.method == 'GET':
        if state_id and state_obj is None:
            abort(404, 'Not found')
        elif state_obj:
            return jsonify(state_obj.to_json())

    if request.method == 'DELETE':
        if state_obj is None:
            abort(404, 'Not found')
        state_obj.delete()
        del state_obj
        return jsonify({})

    if request.method == 'PUT':
        req_json = request.get_json()
        if state_obj is None:
            abort(404, 'Not found')
        if req_json is None:
            abort(400, 'Not a JSON')
        state_obj.bm_update(req_json)
        return jsonify(state_obj.to_json())
