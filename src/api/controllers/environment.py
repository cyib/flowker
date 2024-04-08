import json, uuid, subprocess
from typing import Union
from sqlalchemy import inspect
from src.db.config.engine import create_session, Session
from src.env.environment import FLOWKER_ENVIRONMENTS_PATH
from src.api.common.filemanager import create_folder, save_text_file, read_text_file
from src.api.models.environment import Environment as EnvironmentModel

def create_new_environment(name: str, description: Union[None, str] = None, color: Union[None, str] = None):
    environmentId = str(uuid.uuid4())
    environment = EnvironmentModel(
        id=environmentId,
        name=name,
        description=description,
        color=color
    )
    
    name_checker =  get_environment_by_name(name)
    if(name_checker):
        return 'environment name is already being used', 409
    
    try:
        session: Session = create_session()
        session.begin()
        session.add(environment)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
    
    create_folder(FLOWKER_ENVIRONMENTS_PATH, environmentId)
    create_folder(f'{FLOWKER_ENVIRONMENTS_PATH}\\{environmentId}', 'libraries')
    save_text_file(f'{FLOWKER_ENVIRONMENTS_PATH}\\{environmentId}\\requirements.txt', '')
    
    return 'successfully created environment', 200

def get_environment_by_id(id: Union[str, list]) -> any:
    return get_environment_by_attr(attr='id', keys=id)

def get_environment_by_name(name: Union[str, list]) -> any:
    return get_environment_by_attr(attr='name', keys=name)

def get_environment_by_attr(attr: Union[str,'id','name'], keys: Union[str, list]) -> any:
    result = []
    typeof = type(keys).__name__
    session: Session = create_session()
    try:
        session.begin()
        model = EnvironmentModel
        
        res = []
        res = session.query(model).filter(getattr(model, attr).in_([keys] if typeof == 'str' else keys)).all()
        
        for item in res:
            mapper = inspect(item)
            mappedItem = {column.key: getattr(item, column.key) for column in mapper.attrs}
            result.append(mappedItem)
        
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
        
    if typeof == 'list':
        return result 
    
    if typeof == 'str' and len(result) > 0:
        return result[0]
    else:
        return None
        
def get_all_environments() -> any:
    result = []
    session: Session = create_session()
    try:
        session.begin()
        model = EnvironmentModel
        
        res = []
        res = session.query(model).all()
    
        for item in res:
            mapper = inspect(item)
            mappedItem = {column.key: getattr(item, column.key) for column in mapper.attrs}
            result.append(mappedItem)
        
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()

    return result

def get_requirements_by_id(environmentId: str):
    content = read_text_file(f'{FLOWKER_ENVIRONMENTS_PATH}\\{environmentId}\\requirements.txt')
    return content

def save_requirements_by_id(environmentId: str, content: str):
    save_text_file(f'{FLOWKER_ENVIRONMENTS_PATH}\\{environmentId}\\requirements.txt', content=content)
    return 'successfully requirements updated', 200

def upgrade_requirements_by_id(environmentId: str):
    REQUIREMENTS_PATH = f'{FLOWKER_ENVIRONMENTS_PATH}\\{environmentId}\\requirements.txt'.replace('\\', "/")
    LIBS_FOLDER_PATH = f'{FLOWKER_ENVIRONMENTS_PATH}\\{environmentId}\\libraries'.replace('\\', "/")

    completed_process = subprocess.run(["pip", "install", "-r", REQUIREMENTS_PATH, "-t", LIBS_FOLDER_PATH], capture_output=True, text=True)
    terminal_response = completed_process.stdout
    
    print(terminal_response)
    return terminal_response