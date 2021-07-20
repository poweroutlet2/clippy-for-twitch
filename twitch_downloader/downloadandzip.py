import requests
import shutil
import os


def download_file(url, filename):
    local_filename = filename + '.mp4'
    
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename
    
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

def delete_files_in_dir(dir):
    # Delete all files in given directory
    # dir: full path to directory
    for f in os.listdir(dir):
        try:
            os.remove(os.path.join(dir, f))
        except OSError:
            pass


