import os, sys, subprocess
import importlib
import tempfile
import zipfile
from string import Template
import requests
from . import get_flutter_version

def should_download(ver):
    if sys.platform == 'linux':
        fn = 'libflutter_engine.so'
        path = os.path.join(lib_path(), ver, fn)
        exist = os.path.isfile(path)
    elif sys.platform == 'darwin':
        fn = 'FlutterEmbedder.framework'
        path = os.path.join(lib_path(), ver, fn)
        exist = os.path.isdir(path)
    elif sys.platform == 'win32':
        fn = 'flutter_engine.dll'
        path = os.path.join(lib_path(), ver, fn)
        exist = os.path.isfile(path)
    return not exist

DIR = 'flutter-engine'
def lib_path():
    if sys.platform == 'linux':
        return os.path.expanduser('~/.cache/' + DIR)
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Caches/' + DIR)
    elif sys.platform == 'win32':
        # is this right?
        return os.path.expanduser('~/AppData/local/' + DIR)
    raise Exception("Unsupported platform")

def get_download_url(version):
    base_url = os.environ.get('FLUTTER_STORAGE_BASE_URL') or "https://storage.googleapis.com"
    if sys.platform == 'linux':
        tmpl = "${base_url}/flutter_infra/flutter/${version}/linux-x64/linux-x64-embedder"
    elif sys.platform == 'darwin':
        tmpl = "${base_url}/flutter_infra/flutter/${version}/darwin-x64/FlutterEmbedder.framework.zip"
    elif sys.platform == 'win32':
        tmpl = "${base_url}/flutter_infra/flutter/${version}/windows-x64/windows-x64-embedder.zip"
    else:
        return ''
    return Template(tmpl).substitute(version = version, base_url = base_url)

def download_and_extract(url, dest, strip=False):
    # requests = importlib.import_module('requests')
    req = requests.get(url)
    print(url + ' downloaded')

    os.makedirs(dest, exist_ok=True)

    fp = tempfile.NamedTemporaryFile(delete=True)
    fp.write(req.content)
    fp.seek(0)

    print('Extracting files')
    with zipfile.ZipFile(fp) as zf:
        parts = []
        if strip:
            files = zf.namelist()
            print(files)
            if not files:
                raise Exception('Empty zip!')
            root = files[0]
            for info in zf.infolist():
                if info.filename.startswith(root):
                    info.filename = info.filename[len(root):]
                if info.filename:
                    parts.append(info)
        if parts:
            zf.extractall(dest, parts)
        else:
            zf.extractall(dest)

    fp.close()

def download_flutter_engine():
    ver = get_flutter_version()
    if not should_download(ver):
        print('flutter-engine already downloaded.')
        return

    url = get_download_url(ver)
    dest = os.path.join(lib_path(), ver)
    print('Downloading flutter engine from', url, 'to', dest)
    download_and_extract(url, dest)

    # zip on mac is a double zip file
    if sys.platform == 'darwin':
        subprocess.run([
            'unzip', 'FlutterEmbedder.framework.zip',
            '-d', 'FlutterEmbedder.framework'], stdout=subprocess.DEVNULL, cwd=dest)