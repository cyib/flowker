import uuid, json
from flask import jsonify
from src.db.config.engine import create_session, Session
from src.api.common.utils import compare_versions, filter_nodes_by_version
from sqlalchemy import inspect
from src.api.controllers.snapshot import get_snapshot_by_id, save_snapshot_by_id
from src.api.controllers.script import get_script_by_id, save_script_by_id

# MODELS IMPORT
from src.api.models.node import Node as NodeModel
from src.api.models.iomap import IoMap as IOMapModel
# MODELS IMPORT

def get_all_nodes():
    session: Session = create_session()
    try:
        session.begin()
        nodes = session.query(NodeModel).all()
        nodes = filter_nodes_by_version(nodes, ['name', 'author'])
        result = []
        for node in nodes:
            versions = get_node_versions(session, node)
            result.append({
                'id': node.id,
                'type': node.nodeType,
                'nodeVersion': node.nodeVersion,
                'name': node.name,
                'description': node.description,
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

def get_node_versions(session, node):
    originalNode = session.query(NodeModel).filter_by(id=(node.originalNodeId or node.id)).first()
    versions = session.query(NodeModel).filter_by(originalNodeId=(node.originalNodeId or node.id)).filter(NodeModel.id != node.id)
    versions = [{ 'id': v.id, 'version': v.nodeVersion, 'original': False} for v in versions]
    if(originalNode.id != node.id):
        versions.insert(0, { 'id': originalNode.id, 'version': originalNode.nodeVersion, 'original': True})
    versions = sorted(versions, key=lambda x: x['version'], reverse=True)
    return versions

def get_node_by_id(node_id, pure=False, snapshot=False):
    session: Session = create_session()

    try:
        session.begin()
        node = session.query(NodeModel).filter_by(id=node_id).first()
        versions = get_node_versions(session, node)

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
            'versions': versions
        }

        # Buscar inputs e outputs
        inputs = session.query(IOMapModel).filter_by(nodeId=node_id, ioType='input').all()
        outputs = session.query(IOMapModel).filter_by(nodeId=node_id, ioType='output').all()

        input_list = []
        for io in inputs:
            input_list.append({
                'id': io.id,
                'nodeId': io.nodeId,
                'ioType': io.ioType,
                'name': io.name,
                'datatype': io.datatype,
                'required': io.required,
                'defaultValue': io.defaultValue
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
                'defaultValue': io.defaultValue
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
        originalNodeId=originalNodeId
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
