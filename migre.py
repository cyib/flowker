import sys, os
from src.db.scripts import migration_runner

command = None
step = None
if(len(sys.argv) > 1):
    command = sys.argv[1]

if(len(sys.argv) > 2):
    step = sys.argv[2]
    print(f'[Running migration for {step} steps]')

if(command == 'run' or command == None):
    migration_runner.runner('up', step)
if(command == 'undo'):
    migration_runner.runner('down', step)

if(command == 'remake'):
    migration_runner.runner('down', step)
    migration_runner.runner('up', step)