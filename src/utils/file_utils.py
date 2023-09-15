import requests
import tempfile
import os

def delete_file(filename):
    try:
        os.remove(filename)
    except OSError:
        print(f"file {filename} does not exist. Cannot delete.")

def get_temporary_filename(suffix=''):
    fd, out_filename = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    delete_file(out_filename)
    return out_filename


def download_file(file_url: str, local_file_path = None):
    
    response = requests.get(file_url)
    if local_file_path is None:
        local_file_path = get_temporary_filename('')
    
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)        
        print(f"File downloaded to {local_file_path}")        
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        raise RuntimeError(f"File not available for download at:{file_url}")
    return local_file_path
    