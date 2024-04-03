from flask import jsonify
from engine.autoproc.srb import Srb
from engine.autoproc.gsr import Grb

def run_test(name: str):
    sumNode = Srb('SUM', 'Simple SUM', """
                    pA = this['inputs']['pA']
                    pB = this['inputs']['pB']
                    this['outputs']['pA'] = pA + pB
                """)
    
    sum2Node = Grb(
        'SUM2NODE', 
        '2x SUM', 
        [sumNode], 
        [
            { "id": "SUM", "nexts": ["SUM"] }, 
            { "id": "SUM", "nexts": None }
        ],
        { 'pA': 1, 'pB': 2 }
    )
    
    sum2GRB =  Grb(
        'sum2GRB', 
        '2x GRB', 
        [sum2Node], 
        [
            { "id": "SUM2NODE", "nexts": ["SUM2NODE"] }, 
            { "id": "SUM2NODE", "nexts": None }
        ],
        { 'pB': 7 }
    )
      
    
    resonse = sum2GRB.run()
    
    return jsonify(resonse)
