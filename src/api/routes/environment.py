from flask import Blueprint, request
from src.api.controllers.environment import upgrade_requirements_by_id, get_environment_by_id, get_all_environments, create_new_environment, get_requirements_by_id, save_requirements_by_id

bp = Blueprint("environment", __name__)

@bp.route("/environment/get/all", methods=["GET"])
def getAllEnvironment():
    environments = get_all_environments()
    return { 'environments': environments }

@bp.route("/environment/get/<string:id>", methods=["GET"])
def getEnvironment(id):
    environment = get_environment_by_id(id)
    return { 'environment': environment }

@bp.route("/environment/create", methods=["POST"])
def createEnvironment():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    color = data.get('color')
    msg, status = create_new_environment(name=name, description=description, color=color)
    return { 'message': msg }, status

@bp.route("/environment/requirements/<string:id>", methods=["GET"])
def getRequirements(id):
    requirements = get_requirements_by_id(environmentId=id)
    return { 'requirements': requirements }

@bp.route("/environment/update/requirements/<string:id>", methods=["POST"])
def updateRequirements(id):
    data = request.get_json()
    content = data.get('content')
    msg, status = save_requirements_by_id(environmentId=id, content=content)
    return { 'message': msg }, status

@bp.route("/environment/upgrade/requirements/<string:id>", methods=["GET"])
def upgradeRequirements(id):
    resp = upgrade_requirements_by_id(id)
    return { 'upgradeLog': resp, 'message': 'upgrade completed successfully' }, 200