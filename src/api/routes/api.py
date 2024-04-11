from flask import Blueprint, request
from src.api.controllers.runners import run_node
from src.api.controllers.node import get_node_by_id
from src.api.models.node import Node as NodeModel

bp = Blueprint("api", __name__)

@bp.route("/api/<string:id>", methods=["GET"])
def runGetEndpoint(id):
    node = get_node_by_id(id, pure=True)
    inputs = {}
    if node.get('endpointType') == 'GET':
        print('inputs:', request.args)
        for i, param in enumerate(request.args): 
            val = request.args.get(param)
            if '[' in val:
                val = list(val.replace('[', '').replace(']', '').split(','))
                val = [float(x) if isinstance(x, (int, float, str)) else x for x in val]
            if isinstance(val, str) and val.replace('.', '').isnumeric():
                val = float(val)
            inputs[param] = val
        return run_node(id, inputs=inputs, includeExecutionParams=False, forceRemapOutput=True)
    else:
        return { 'message': 'Bad request to this endpoint.' }, 400

@bp.route("/api/<string:id>", methods=["POST"])
def runPostEndpointP(id):
    node = get_node_by_id(id, pure=True)
    if node.get('endpointType') == 'POST':
        inputs = request.get_json()
        print('inputs:', inputs)
        return run_node(id, inputs=inputs, includeExecutionParams=False, forceRemapOutput=True)
    else:
        return { 'message': 'Bad request to this endpoint.' }, 400
    