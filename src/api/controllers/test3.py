from flask import jsonify, request
from engine.concept.node import Node, IoMap, Command, InputReferenceConversor as IRC

def run_test(name: str):
    response = None
    query_dict = request.args.to_dict()
    
    node_sum = Node(
        'a', 
        'SUM',
        [
            IoMap('p1', 'float', False, 0),
            IoMap('p2', 'float', False, 0)
        ],
        [
            IoMap('output', 'float', True)
        ],
        """
        output = p1 + p2
        """
    )
    
    node_group_sum = Node(
        'c', 
        'GROUP_SUM',
        [
            IoMap('p1', 'float', False, 0),
            IoMap('p2', 'float', False, 0),
            IoMap('p3', 'float', False, 0)
        ],
        [
            IoMap('output', 'float', True)
        ],
        [
            Command(node_sum),
            Command(node_sum, [
                IRC('output', 'p1'),
                IRC('p3', 'p2')
            ])
        ]
    )
    
    node_twice = Node(
        'd', 
        'TWICE',
        [
            IoMap('p1', 'float', False, 0),
            IoMap('p2', 'float', False, 0),
            IoMap('p3', 'float', False, 0)
        ],
        [
            IoMap('output', 'float', True)
        ],
        [
            Command(node_group_sum),
            Command(node_group_sum, [IRC('output', 'p1'),IRC('p1', 'p2'),IRC('p2', 'p3')]),
            Command(node_sum, [IRC('output', 'p1'),IRC('p3', 'p2')])
        ]
    )
    
    response = node_twice.run(query_dict)
    
    return jsonify(response)
