import os, shutil
from src.env.environment import FLOWKER_CLIENT_PATH, FLOWKER_SNAPSHOTS_PATH, FLOWKER_SCRIPTS_PATH, FLOWKER_ENVIRONMENTS_PATH, FLOWKER_DATABASE_PATH, FLOWKER_INIT_DATABASE_PATH, FLOWKER_DATABASE_COMPLETE_PATH, FLOWKER_INIT_REQUIREMENTS_PATH

def check_flowker_folders():
    folders = [FLOWKER_CLIENT_PATH, FLOWKER_SNAPSHOTS_PATH, FLOWKER_SCRIPTS_PATH, FLOWKER_ENVIRONMENTS_PATH, FLOWKER_DATABASE_PATH]
    for folder in folders:
        if not os.path.exists(folder):
            print(folder)
            os.makedirs(folder)
            
    if not os.path.exists(FLOWKER_DATABASE_COMPLETE_PATH):
        shutil.copy(FLOWKER_INIT_DATABASE_PATH, FLOWKER_DATABASE_COMPLETE_PATH)
    
    DEFAULT_ENV_PATH = f'{FLOWKER_ENVIRONMENTS_PATH}/00000000-0000-0000-0000-000000000001'
    if not os.path.exists(DEFAULT_ENV_PATH):
        os.makedirs(DEFAULT_ENV_PATH)
        LIBRARIES_PATH = f'{DEFAULT_ENV_PATH}/libraries'
        os.makedirs(LIBRARIES_PATH)
        shutil.copy(FLOWKER_INIT_REQUIREMENTS_PATH, f'{DEFAULT_ENV_PATH}/requirements.txt')