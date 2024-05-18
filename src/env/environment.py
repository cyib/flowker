import os, shutil
parent_dir = os.path.abspath(os.path.join(os.getcwd())).replace('\\', '/')

DB_NAME = 'flowker'
FLOWKER_BASE_PATH = parent_dir #f'D:/Projects/flowker'

FLOWKER_CLIENT_PATH = f'{FLOWKER_BASE_PATH}/client'
FLOWKER_SNAPSHOTS_PATH = f'{FLOWKER_CLIENT_PATH}/snapshots'
FLOWKER_SCRIPTS_PATH = f'{FLOWKER_CLIENT_PATH}/scripts'
FLOWKER_SCRIPTS_EXTERNAL_PATH = f'{FLOWKER_SCRIPTS_PATH}/external'
FLOWKER_ENVIRONMENTS_PATH = f'{FLOWKER_CLIENT_PATH}/environments'
FLOWKER_DATABASE_PATH = f'{FLOWKER_CLIENT_PATH}/database'
FLOWKER_DATABASE_COMPLETE_PATH = f'{FLOWKER_DATABASE_PATH}/{DB_NAME}.db'


FLOWKER_INIT_DATABASE_PATH = f'{FLOWKER_BASE_PATH}/src/db/base/database_init.db'
FLOWKER_INIT_REQUIREMENTS_PATH = f'{FLOWKER_BASE_PATH}/src/db/base/requirements_init.txt'