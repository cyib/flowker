from flask import jsonify
from engine.autoproc.srb import Srb
from engine.autoproc.gsr import Grb

def run_test(name: str):
    node1 = Srb('GET_PID', 'Get Process Id', """
                    structures = this['inputs']['structures']
                    print(structures)
                    this['outputs']['pid'] = 123456
                """)
    node2 = Srb('RUN_SQL_W_PID', 'Run SQL with Process Id', """
                    sql = this['inputs']['sql']
                    pid = this['inputs']['pid']
                    print('The code pass here')
                    print(pid)
                    print(sql)
                    this['outputs']['response'] = [1, 2, 3]
                """)
    node3 = Grb(
        'GETPID_RUNSQL', 
        'Get Process Id + Run SQL', 
        [node1, node2], 
        [{ "id": "GET_PID", "nexts": ["RUN_SQL_W_PID"] }, { "id": "RUN_SQL_W_PID", "nexts": None }],
        { 'structures': 'A,B,C', 'sql': 'select * from user' }
    )
    
    resonse = node3.run()
    
    node4 = Srb('GET_PROCESS_NAME', 'Get Process Name', """
                    smart = this['inputs']['smart']
                    print(smart)
                    this['outputs']['processName'] = 'SMART_PHONE'
                """)
    
    node5 = Grb(
        'TEST', 
        'Run test',
        [node3, node4],
        [{ "id": "GETPID_RUNSQL", "nexts": ["GET_PROCESS_NAME"] }, { "id": "GET_PROCESS_NAME", "nexts": None }],
        { 'smart': node3.output['response'] }
    )
        
    new_response = node5.run()
    
    return jsonify(new_response)
