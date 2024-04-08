import json
from src.env.environment import FLOWKER_SNAPSHOTS_PATH
from src.api.common.filemanager import read_text_file, save_text_file

def get_snapshot_by_id(nodeId: str):
    snapshotPath = f'{FLOWKER_SNAPSHOTS_PATH}\\{nodeId}.json'
    content = read_text_file(snapshotPath)
    return json.loads(content)

def save_snapshot_by_id(nodeId: str, content: str):
    snapshotPath = f'{FLOWKER_SNAPSHOTS_PATH}\\{nodeId}.json'
    save_text_file(snapshotPath, content)