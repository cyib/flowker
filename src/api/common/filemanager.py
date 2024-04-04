import os
    
def save_text_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def delete_text_file(file_path):
    os.remove(file_path)