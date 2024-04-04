import json
from src.env.environment import FLOWKER_SCRIPTS_PATH
from src.api.common.filemanager import read_text_file, save_text_file

def get_script_by_id(nodeId: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_PATH}\\{nodeId}.{ext}'
    content = read_text_file(scriptPath)
    return content

def save_script_by_id(nodeId: str, content: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_PATH}\\{nodeId}.{ext}'
    save_text_file(scriptPath, content)