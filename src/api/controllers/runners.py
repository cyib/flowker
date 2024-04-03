import uuid, time
from src.api.common.utils import groupByKey
from flask import jsonify
from src.api.controllers.manager import get_table_by_id, get_node_by_id
from src.db.config.engine import create_session, Session
from engine.concept.node import Node, IoMap, Command, InputReferenceConversor as IRC
from typing import Union
from src.api.models.node import Node as NodeModel

def run_current_script(node, inputsParams = {}, useIdOutput = False):
    currentNode = Node(
        id=node['id'], 
        name=node['name'],
        inputsMap=list(map(lambda x: IoMap(x['name'], x['ioType'], x['required'], x['defaultValue']), node['inputs'])),
        outputsMap=list(map(lambda x: IoMap(x['name'], x['ioType'], x['required'], x['defaultValue']), node['outputs'])),
        script=node['script']
    )
    
    start_time = time.time()
    try:
        response = currentNode.run(inputsParams)
        if(useIdOutput == True):
            res = {}
            for i, output in enumerate(response):
                finder = list(filter(lambda out: out['name'] == output, node['outputs']))
                if(len(finder) > 0):
                    res[finder[0]['id']] = response[output]
            response = res
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        response = {
            '__execution__params__': {
                'terminal_output': f"Configuration error: {str(e)}",
                'execution_duration': duration,
                'status': 'error'
            }
        }
    
    return jsonify(response)

def remove_items(original_list, remove_list, key):
    for item in remove_list:
        for i in range(len(original_list)):
            if original_list[i][key] == item[key]:
                original_list.pop(i)
                break
    return original_list

def run_node(nodeId: str, inputs = {}, includeExecutionParams = True, useIdOutput = False, forceRemapOutput = False):
    node: NodeModel = get_node_by_id(nodeId, snapshot=True).json
    if node['nodeType'] == "script":
        res = run_current_script(node, inputs, useIdOutput).json
        if((includeExecutionParams == False) and ('__execution__params__' in res)):
            del res['__execution__params__']
        return res
    elif node['nodeType'] == "group":
        res = run_sequence(node['snapshot']['edges'], inputs, node['outputs'], remapBy='id')
        if(forceRemapOutput):
            res = remapOutput(res, node['outputs'])
        return res

def remapOutput(params: list, outputMap: list, remapBy: str = 'name'):
    remappedRes: dict = {}
    alreadyOutputs = list(params.keys())
    mappedList = list(filter(lambda output: (output['id'] in alreadyOutputs), outputMap))
    for item in mappedList:
        remappedRes[item[remapBy]] = params[item['id']]
    return remappedRes
        
    

def run_sequence(sequence, params = {}, outputsMap: list = [], remapBy: str = 'name'):
    #sequence = list(map(lambda e:{**e, 'done': False, 'outputs': []}, sequence))
    groupedNodesToRun = groupByKey(sequence, 'target')
    groupedIds = list(groupedNodesToRun.keys())
    nodes = list(map(lambda fId: { 'id': fId, 'inputs': groupedNodesToRun[fId], 'done': False }, groupedIds))
    nodes.append({ 'id': 'action-start', 'inputs': {}, 'outputs': {}, 'done': True })
    
    #NOTE - PREPARE ALL RUNNERS
    ioMapIds = list(map(lambda x: x['sourceHandle'], sequence)) + list(map(lambda x: x['targetHandle'], sequence))
    ioMapIds = list(filter(lambda x: 'connector' not in x, ioMapIds))
    iomaps = get_table_by_id('iomap', ioMapIds)
    nodeIds = list(set(map(lambda x: x['nodeId'], iomaps)))
    runners = get_table_by_id('node', nodeIds)
    
    #NOTE - RUN NODES RECURSIVE 
    leftNodes = getNodesLeft(nodes)
    while len(leftNodes) > 0:
        currentRunner = leftNodes[0]
        inputsEdge = currentRunner['inputs']
        readySources = list(map(lambda e: e['id'], list(filter(lambda n: n['done'] == True, nodes))))  
        checkerList = list(map(lambda i: (i['source'] in readySources), inputsEdge))
        readyToRun = ((False in checkerList) == False)
        
        ioReference = list(filter(lambda io: io['id'] == inputsEdge[0]['targetHandle'], iomaps))
        runnerNodeId = ioReference[0]['nodeId'] if len(ioReference) > 0 else None
        finalOutputs = []
        
        if currentRunner['done'] == False:
            if(readyToRun):
                print(f'{len(leftNodes)}) {runnerNodeId} - ready to run')
                output = {}
                if(runnerNodeId and (currentRunner['id'] != 'action-finish')):
                    remapInput = remapInputParams(params, inputsEdge, iomaps, remapBy='name')
                    output = run_node(runnerNodeId, remapInput, includeExecutionParams=False, useIdOutput=True)
                    params = params | output
                    
                if(currentRunner['id'] == 'action-finish'):
                    remapInput = remapInputParams(params, inputsEdge, outputsMap, remapBy=remapBy)
                    finalOutputs = remapInput
                    
                currentRunner['outputs'] = output
                currentRunner['done'] = True
            else:
                print(f'{len(leftNodes)}) {runnerNodeId} - not ready')
        
        nodes.remove(currentRunner)
        nodes.append(currentRunner)
        
        leftNodes = getNodesLeft(nodes)
    
    print('all done :)')
        
    #TODO - NEEDS TO ADJUST THIS RETURN AFTER IMPLEMENT INPUT AND OUTPUTS TO SPECIAL NODES (START/FINISH) IN FRONT
    return finalOutputs
    
def remapInputParams(allParams: dict, inputEdges: list, iomaps: list, remapBy: str = 'name') -> dict:
    """
    Function to remap inputs to send the necessary to node execution.

    Parameters:
    allParams (dict): list of outputs from all nodes execution.
    inputEdges (list): list of edges from current node to execution.
    iomaps (list): list of iomaps that can be used by all the sequence.

    Returns:
    dict: a dict with only the useful params to run the current node.
    """
    remapInput: dict = {}
    alreadyOutputs = list(allParams.keys())
    for i, _edge in enumerate(inputEdges):
        if(_edge['sourceHandle'] in alreadyOutputs):
            _ios = list(filter(lambda io: io['id'] == _edge['targetHandle'], iomaps))
            if(len(_ios) > 0):
                _io = _ios[0]
                remapInput[_io[remapBy]] = allParams[_edge['sourceHandle']]
    return remapInput

def getNodesLeft(nodes) -> list:
    nodesToRun = list(filter(lambda n: n['done'] == False, nodes))
    return nodesToRun

def run_childs_by_sourceId(flowId: str):
    pass