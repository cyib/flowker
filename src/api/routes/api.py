from flask import Blueprint
from src.api.controllers.runners import run_node

bp = Blueprint("api", __name__)

@bp.route("/api/<string:id>", methods=["GET"])
def runEndpoint(id):
    return run_node(id, includeExecutionParams=False, forceRemapOutput=True)