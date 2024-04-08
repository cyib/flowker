import sys, os
from src.db.scripts import migration_runner
from typing import Union

command = None
step = None
path = 'migrations'
if(len(sys.argv) > 1):
    command = sys.argv[1]

if(len(sys.argv) > 2):
    path = sys.argv[2]
    print(f'[Run path: {path}]')

if(len(sys.argv) > 3):
    step = sys.argv[3]
    print(f'[Running migration for {step} steps]')

if(command == 'run' or command == None):
    migration_runner.runner('up', step, path)
if(command == 'undo'):
    migration_runner.runner('down', step, path)

if(command == 'remake'):
    migration_runner.runner('down', step, path)
    migration_runner.runner('up', step, path)