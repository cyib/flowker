import os
    
def save_text_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    while not os.path.exists(file_path):
        pass  # Wait until the file is created
    
def save_text_file_with_look(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    while not os.path.exists(file_path):
        pass  # Wait until the file is created

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def delete_text_file(file_path):
    os.remove(file_path)
    
def create_folder(path, folder_name):
    final_path = os.path.join(path, folder_name)
    os.makedirs(final_path)