import uuid
from flask import Blueprint, request
from src.api.controllers.node import get_all_nodes, get_node_by_id, save_node, delete_node
from src.api.controllers.runners import run_current_script, run_sequence, run_node

bp = Blueprint("manager", __name__)

@bp.route("/repository", methods=["GET"])
def repository():
    return get_all_nodes()

@bp.route("/get/<string:id>", methods=["GET"])
def getById(id):
    return get_node_by_id(id)

@bp.route("/get/snapshot/<string:nodeId>", methods=["GET"])
def getSnapshotByNodeId(nodeId):
    return get_node_by_id(nodeId, snapshot=True)

@bp.route("/create/<string:version>", methods=["POST"])
def create(version):
    data = request.get_json()
    return save_node(data, version_type=version)

@bp.route("/run/script/current", methods=["POST"])
def runScript():
    res = None
    try:
        data = request.get_json()
        tempNodeId = save_node(data, version_type='temp')
        node = get_node_by_id(tempNodeId).json
        res = run_current_script(node)
        delete_node(tempNodeId)
    except Exception as e:
        print(f'[ERROR HERE] >> {e}')
        res = e
    return res

@bp.route("/run/node/<string:id>", methods=["GET"])
def runNodeById(id):
    return run_node(id, includeExecutionParams=False, forceRemapOutput=True)

@bp.route("/api/<string:id>", methods=["GET"])
def runEndpoint(id):
    return run_node(id, includeExecutionParams=False, forceRemapOutput=True)

@bp.route("/run/sequence", methods=["POST"])
def runGroup():
    res = None
    try:
        payload = request.get_json()
        sequence = payload['sequence']
        inputs = payload['inputs']
        outputs = payload['outputs']
        res = run_sequence(sequence, params={}, outputsMap=outputs)
        print(res)
    except Exception as e:
        res = e
    return res

@bp.route("/delete/<string:id>", methods=["GET"])
def delete(id):
    return delete_node(id)