import os

HOME    = os.path.expanduser("~")
DESKTOP = HOME + "/Desktop/"
OUTPUT  = HOME + "/FRIDAY/outputs/"

def create_file(filename, content="", folder=OUTPUT):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, 'w') as f:
        f.write(content)
    return path

def open_file(path):
    os.system(f'xdg-open "{path}"')

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def find_file(name, search_path=HOME):
    results = []
    for root, dirs, files in os.walk(search_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if name.lower() in file.lower():
                results.append(os.path.join(root, file))
        if len(results) >= 5:
            break
    return results

def list_folder(path=DESKTOP):
    if os.path.exists(path):
        return os.listdir(path)
    return []