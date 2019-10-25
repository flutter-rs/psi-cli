import os, sys, subprocess
from string import Template

import collections

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


def pkg_assets_dir():
    d = __file__
    d = os.path.dirname(d)
    d = os.path.dirname(d)
    return os.path.join(d, 'assets')

def look_for_proj_dir(d, fn = 'Cargo.toml'):
    while not os.path.isfile(os.path.join(d, fn)):
        p = os.path.dirname(d)
        if not p or p == d:
            return None
        d = p
    return d

def flutter_proj_dir():
    d = look_for_proj_dir(os.getcwd(), 'pubspec.yaml')
    if d is None:
        raise Exception('Cannot find flutter directory')
    return d

def read_sdk_version(root):
    fp = os.path.join(root, 'bin', 'internal', 'engine.version')
    with open(fp) as f:
        return f.read().strip()

def guess_sdk_path():
    try:
        output = subprocess.check_output([
            'where.exe' if sys.platform == 'win32' else 'which',
            'flutter'
        ], encoding = 'utf8')
        lines = output.strip().split()
        path = lines[0]
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        return path
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

# Read engine version from FLUTTER_ROOT first
# otherwise use FLUTTER_ENGINE_VERSION env variable
def get_flutter_version():
    if 'FLUTTER_ENGINE_VERSION' in os.environ:
        return os.environ.get('FLUTTER_ENGINE_VERSION')

    root = os.environ.get('FLUTTER_ROOT')
    if root:
        return read_sdk_version(root)
    else:
        sdk = guess_sdk_path()
        print("sdk is proballby at", sdk)
        if sdk:
            return read_sdk_version(sdk)
        else:
            raise Exception('Cannot find flutter engine version. flutter cli not in PATH. You may need to set either FLUTTER_ROOT or FLUTTER_ENGINE_VERSION')

def get_workspace_dir(proj_dir):
    return look_for_proj_dir(os.path.dirname(proj_dir))


def tmpl_file(fp, config):
    with open(fp, 'r+') as f:
        s = Template(f.read()).substitute(**config)
        f.seek(0)
        f.truncate()
        f.write(s)
