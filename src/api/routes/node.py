import uuid
from flask import Blueprint, request
from src.api.controllers.node import get_all_nodes, get_node_by_id, save_node, delete_node, get_script_raw_by_id
from src.api.controllers.runners import run_current_script, run_sequence, run_node

bp = Blueprint("node", __name__)

@bp.route("/repository", methods=["GET"])
def repository():
    onlyEndpoints = True if request.args.get('onlyendpoints') == 'true' else False
    return get_all_nodes(onlyEndpoints=onlyEndpoints)

@bp.route("/node/get/<string:id>", methods=["GET"])
def getById(id):
    return get_node_by_id(id)

@bp.route("/node/get/script/raw/<string:id>", methods=["GET"])
def getScriptRawById(id):
    return get_script_raw_by_id(id)

@bp.route("/node/get/snapshot/<string:nodeId>", methods=["GET"])
def getSnapshotByNodeId(nodeId):
    return get_node_by_id(nodeId, snapshot=True)

@bp.route("/node/create/<string:version>", methods=["POST"])
def create(version):
    data = request.get_json()
    return save_node(data, version_type=version)

@bp.route("/node/run/script/current", methods=["POST"])
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

@bp.route("/node/run/node/<string:id>", methods=["GET"])
def runNodeById(id):
    return run_node(id, includeExecutionParams=False, forceRemapOutput=True)

@bp.route("/node/run/sequence", methods=["POST"])
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

@bp.route("/node/delete/<string:id>", methods=["GET"])
def delete(id):
    return delete_node(id)