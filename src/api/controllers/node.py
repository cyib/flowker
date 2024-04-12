import uuid, json
from flask import jsonify
from src.db.config.engine import create_session, Session
from src.api.common.utils import compare_versions, filter_nodes_by_version
from sqlalchemy import inspect
from src.api.controllers.snapshot import get_snapshot_by_id, save_snapshot_by_id
from src.api.controllers.script import get_script_by_id, save_script_by_id, delete_script_by_id
from src.api.controllers.environment import get_all_environments

# MODELS IMPORT
from src.api.models.node import Node as NodeModel
from src.api.models.iomap import IoMap as IOMapModel
# MODELS IMPORT

def get_all_nodes(onlyEndpoints: bool = False):
    session: Session = create_session()
    try:
        session.begin()
        nodes = None
        envs = get_all_environments()
        alreadyIncludesId = []
        if onlyEndpoints:
            nodes = session.query(NodeModel).filter(NodeModel.isEndpoint == True).order_by(NodeModel.originalNodeId.desc(), NodeModel.nodeVersion.desc()).all()
        else:
            nodes = session.query(NodeModel).order_by(NodeModel.originalNodeId.desc(), NodeModel.nodeVersion.desc()).all()
        #nodes = filter_nodes_by_version(nodes, ['name', 'author'])
        result = []
        for node in nodes:
            node: NodeModel = node
            if (node.id in alreadyIncludesId):
                continue
            
            versions = get_node_versions(session, node, envs)
            alreadyIncludesId.append(node.id)
            for version in versions:
                alreadyIncludesId.append(version.get('id'))
                
            envName = next((env['name'] for env in envs if env['id'] == node.environmentId), None)
            result.append({
                'id': node.id,
                'type': node.nodeType,
                'nodeVersion': node.nodeVersion,
                'name': node.name,
                'description': node.description,
                'environmentId': node.environmentId,
                'environmentName': envName,
                'isEndpoint': node.isEndpoint,
                'endpointType': node.endpointType,
                'author': node.author,
                'versions': versions
            })
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()

    return jsonify(result)

def get_table_by_id(tableName, id: str|list) -> any:
    result = []
    session: Session = create_session()
    try:
        session.begin()
        model = None
        if(tableName == 'iomap'):
            model = IOMapModel
        if(tableName == 'node'):
            model = NodeModel
        
        res = []
        typeof = type(id).__name__
        if(typeof == 'str'):
            res = session.query(model).filter(model.id.in_(id)).first()
            result = res
        if(typeof == 'list'):
            res = session.query(model).filter(model.id.in_(id)).all()
        
            for item in res:
                mapper = inspect(item)
                mappedItem = {column.key: getattr(item, column.key) for column in mapper.attrs}
                result.append(mappedItem)
        
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()

    return result

def get_env_by_id(environmentId: str, environments: list):
    return next((env['name'] for env in environments if env['id'] == environmentId), None)

def get_node_versions(session, node, environments):
    originalNode = session.query(NodeModel).filter_by(id=(node.originalNodeId or node.id)).first()
    versions = session.query(NodeModel).filter_by(originalNodeId=(node.originalNodeId or node.id)).filter(NodeModel.id != node.id)
    versions = [{ 'id': v.id, 'name': v.name, 'version': v.nodeVersion, 'original': False, 'endpointType': v.endpointType, 'environmentId': v.environmentId, 'environmentName': get_env_by_id(v.environmentId, environments) } for v in versions]
    if(originalNode.id != node.id):
        originalModel = { 'id': originalNode.id, 'name': originalNode.name, 'version': originalNode.nodeVersion, 'original': True, 'endpointType': originalNode.endpointType, 'environmentId': originalNode.environmentId, 'environmentName': get_env_by_id(originalNode.environmentId, environments) }
        versions.insert(0, originalModel)
    versions = sorted(versions, key=lambda x: x['version'], reverse=True)
    return versions

def get_script_raw_by_id(node_id):
    return get_script_by_id(node_id)

def get_node_by_id(node_id, pure=False, snapshot=False):
    session: Session = create_session()

    try:
        session.begin()
        node = session.query(NodeModel).filter_by(id=node_id).first()
        envs = get_all_environments()
        versions = get_node_versions(session, node, envs)

        if node is None:
            return jsonify({"message": "Node not found"}), 404

        result = {
            'id': node.id,
            'nodeVersion': node.nodeVersion,
            'name': node.name,
            'author': node.author,
            'description': node.description,
            'nodeType': node.nodeType,
            'originalNodeId': node.originalNodeId,
            'environmentId': node.environmentId,
            'isEndpoint': node.isEndpoint,
            'endpointType': node.endpointType,
            'versions': versions
        }

        # Buscar inputs e outputs
        inputs = session.query(IOMapModel).filter_by(nodeId=node_id, ioType='input').order_by(IOMapModel.orderNumber.asc()).all()
        outputs = session.query(IOMapModel).filter_by(nodeId=node_id, ioType='output').order_by(IOMapModel.orderNumber.asc()).all()

        input_list = []
        for io in inputs:
            input_list.append({
                'id': io.id,
                'nodeId': io.nodeId,
                'ioType': io.ioType,
                'name': io.name,
                'datatype': io.datatype,
                'required': io.required,
                'defaultValue': io.defaultValue,
                'orderNumber': io.orderNumber
            })

        output_list = []
        for io in outputs:
            output_list.append({
                'id': io.id,
                'nodeId': io.nodeId,
                'ioType': io.ioType,
                'name': io.name,
                'datatype': io.datatype,
                'required': io.required,
                'defaultValue': io.defaultValue,
                'orderNumber': io.orderNumber
            })

        result['inputs'] = input_list
        result['outputs'] = output_list
        
        if node.nodeType == 'script':
            result['script'] = get_script_by_id(node_id)

        # Se o node for do tipo 'group' buscar sequências
        if node.nodeType == 'group':            
            if(snapshot == True):
                snapshot = get_snapshot_by_id(node_id)
                snapshotJson = snapshot
                result['snapshot'] = snapshotJson
        
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()

    if(pure):
        return result
    
    return jsonify(result)

def save_node(json_body, version_type: str):
    nodeId = str(uuid.uuid4())
    
    originalNodeId = None
    version = '0.0.1'
    if json_body['originalNodeId'] or json_body['id']:
        originalNodeId = json_body['originalNodeId'] or json_body['id']
        #TODO - Melhorar sistema de versionamento baseado no node original
        # Buscar na base antes pra fazer a checagem de versão
        #TODO - Criar uma função para fazer o gerenciamento das versões dos blocos
        version = json_body['version']
        vSplit = version.split('.')
        major = int(vSplit[0])
        release = int(vSplit[1])
        minor = int(vSplit[2])
        
        if(version_type == 'major'):
            major = major + 1
            release = 0
            minor = 0
        if(version_type == 'release'):
            release = release + 1
            minor = 0
        if(version_type == 'minor' or version_type == 'temp'):
            minor = minor + 1
            
        version = f'{major}.{release}.{minor}'
    
    if version_type == 'temp':
        version = f'{version}-temp'
        
    node = NodeModel(
        id=nodeId,
        nodeVersion=version,
        name=json_body['name'],
        description=json_body['description'],
        nodeType=json_body['nodeType'],
        originalNodeId=originalNodeId,
        environmentId=json_body['environmentId'],
        isEndpoint=bool(json_body['isEndpoint']),
        endpointType=json_body['endpointType']
    )
    
    iomaps = []
    replaceIOList = []
    
    if json_body.get('inputs'):
        _inputs = json_body['inputs']
        for i, io in enumerate(_inputs):
            inputId = str(uuid.uuid4())
            if 'id' in io:
                replaceIOList.append({ 'type': 'input', 'from': io['id'], 'to': inputId })
            iomap = IOMapModel(
                id=inputId,
                nodeId=nodeId,
                ioType='input',
                name=io['name'],
                datatype=io['datatype'],
                required=io['required'],
                defaultValue=io['defaultValue'],
                orderNumber=io['orderNumber'],
            )
            iomaps.append(iomap)
            
    if json_body.get('outputs'):
        _outputs = json_body['outputs']
        for i, io in enumerate(_outputs):
            outputId = str(uuid.uuid4())
            if 'id' in io:
                replaceIOList.append({ 'type': 'output', 'from': io['id'], 'to': outputId })
            iomap = IOMapModel(
                id=outputId,
                nodeId=nodeId,
                ioType='output',
                name=io['name'],
                datatype=io['datatype'],
                required=io['required'],
                defaultValue=io['defaultValue'],
                orderNumber=io['orderNumber'],
            )
            iomaps.append(iomap)
    
    
    script = None
    if json_body.get('script'):
        formatedScript= str(json_body['script'])
        script = formatedScript
    
    snapshot = None
    if json_body.get('snapshot'):
        formatedSnapshot= str(json.dumps(json_body['snapshot']))
        for replacer in replaceIOList:
            formatedSnapshot = formatedSnapshot.replace(replacer['from'], replacer['to'])
        snapshot = formatedSnapshot
        
    session: Session = create_session()

    try:
        session.begin()
        
        if(node.nodeType == 'script'):
            session.add(node)
            session.add_all(iomaps)
            if(script):
                save_script_by_id(nodeId, script)
        
        if(node.nodeType == 'group'):
            session.add(node)
            session.add_all(iomaps)
            if(snapshot):
                save_snapshot_by_id(nodeId, snapshot)
        
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
    
    if(version_type == 'minor' or version_type == 'temp'):
        return nodeId
    
    return jsonify({"message": "Node created successfully", "nodeId": nodeId })

def delete_node(node_id):
    session: Session = create_session()
    try:
        session.begin()

        # Delete the input and output mappings associated with the node
        iomaps = session.query(IOMapModel).filter_by(nodeId=node_id).all()
        for iomap in iomaps:
            session.delete(iomap)

        # Delete the node itself
        node = session.query(NodeModel).filter_by(id=node_id).first()
        if node is None:
            return jsonify({"message": "Node not found"}), 404
        
        delete_script_by_id(node_id)
        session.delete(node)

        # Commit the transaction
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
    return jsonify({"message": "Node and associated data deleted successfully"})
