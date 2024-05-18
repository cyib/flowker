import psutil
from src.env.environment import FLOWKER_SCRIPTS_PATH, FLOWKER_SCRIPTS_EXTERNAL_PATH
from src.api.common.filemanager import read_text_file, save_text_file, delete_text_file, save_text_file_with_look

def get_script_by_id(nodeId: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_PATH}\\{nodeId}.{ext}'
    content = read_text_file(scriptPath)
    return content

def get_external_script_by_id(filename: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_EXTERNAL_PATH}\\{filename}.{ext}'
    content = read_text_file(scriptPath)
    return content

def save_script_by_id(filename: str, content: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_PATH}\\{filename}.{ext}'
    save_text_file(scriptPath, content)
    
def save_external_script_by_id(filename: str, content: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_EXTERNAL_PATH}\\{filename}.{ext}'
    save_text_file_with_look(scriptPath, content)
    
def delete_script_by_id(nodeId: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_PATH}\\{nodeId}.{ext}'
    delete_text_file(scriptPath)

def delete_external_script_by_id(filename: str, ext: str = 'py'):
    scriptPath = f'{FLOWKER_SCRIPTS_EXTERNAL_PATH}\\{filename}.{ext}'
    delete_text_file(scriptPath)

def is_file_open(file_path):
    for process in psutil.process_iter(['pid', 'name']):
        try:
            open_files = process.open_files()
        except psutil.AccessDenied:
            continue
        else:
            for file in open_files:
                if file.path == file_path:
                    return True
    return False
