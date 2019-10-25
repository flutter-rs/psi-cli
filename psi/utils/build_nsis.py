import os
import subprocess
import tempfile
from shutil import copyfile, copytree, rmtree
from . import pkg_assets_dir

def prepare(envs):
    name = envs['NAME']
    output_dir = envs['OUTPUT_DIR']
    assets_dir = envs['RUST_ASSETS_DIR']
    win_config = envs['CONFIG']['win']
    return dict(
        NAME = name,
        VERSION = envs['VERSION'],
        FILE1 = os.path.join(output_dir, name + '.exe'),
        FILE2 = os.path.join(output_dir, 'flutter_engine.dll'),
        FILE3 = os.path.join(assets_dir, 'icudtl.dat'),
        ICON = os.path.join(assets_dir, 'icon.ico'),
        FLUTTER_ASSETS = envs['FLUTTER_ASSETS'],
        OUTPUT_FILE = os.path.join(output_dir, 'Installer.exe'),
        LOCALE_APPNAME = win_config['locale_app_name'],
        PUBLISHER = win_config['publisher'],
    )

def build(envs):
    subprocess.run([
        'makensis',
        os.path.join(pkg_assets_dir(), 'installer.nsi')
    ], env = envs)

    return envs['OUTPUT_FILE']

