#!/usr/bin/env python3
import os
import glob
import subprocess
import shutil
import tempfile
from ..utils import look_for_proj_dir, tmpl_file
from ..utils.download import download_flutter_engine, download_and_extract

ARCHIVE = 'https://github.com/flutter-rs/flutter-app-template/archive/v0.3.5.zip'

def get_tmpl_files(proj_dir):
    tmplfile_path = os.path.join(proj_dir, '.tmplfiles')
    try:
        with open(tmplfile_path) as f:
            tmplfiles = []
            for line in f.readlines():
                line = line.strip()

                if os.path.isdir(os.path.join(proj_dir, line)):
                    line = os.path.join(line, '*')

                tmplfiles.append(line)
    except:
        tmplfiles = []

    return tmplfiles

def tmpl_proj(proj_dir, config, tmplfiles=[]):
    if not tmplfiles:
        tmplfiles = get_tmpl_files(proj_dir)

    for pattern in tmplfiles:
        for fp in glob.iglob(os.path.join(proj_dir, pattern)):
            fp = os.path.join(proj_dir, fp)
            if os.path.isfile(fp):
                tmpl_file(fp, config)

def create_project(proj_dir, config):
    download_and_extract(ARCHIVE, proj_dir, strip=True)

    tmpl_proj(proj_dir, config)
    
    # remove .tmplfile, .git
    os.remove(os.path.join(proj_dir, '.tmplfiles'))

def patch_project(proj_dir, config):
    ''' add to existing flutter proj
    '''
    with tempfile.TemporaryDirectory() as tmpdir:
        download_and_extract(ARCHIVE, tmpdir, strip=True)
        tmplfiles = get_tmpl_files(tmpdir)
        tmpl_proj(tmpdir, config, tmplfiles)
        shutil.move(os.path.join(tmpdir, 'rust'), proj_dir)

def run(args):
    if args.proj == '.':
        # add flutter-rs to existing dir
        proj_dir = os.getcwd()
        proj_name = os.path.basename(proj_dir) \
            .replace('_', '-')
        created = False
    else:
        proj_name = args.proj.replace('_', '-')
        proj_dir = os.path.join(os.getcwd(), proj_name)
        created = True

    print('🔮  Creating files')
    lib_name = proj_name.replace('-', '_')
    config = {
        "name": proj_name,
        "lib_name": lib_name, # underlined version of name
    }
    if created:
        create_project(proj_dir, config)
    else:
        patch_project(proj_dir, config)

    print('🧩  Downloading flutter-engine')
    download_flutter_engine()

    print('🍭  Done! Happy coding.')
    print('')
    print('Start developing with:')
    pad = ' ' * 4
    if created:
        print(pad + 'cd %s' % proj_name)
        print(pad + 'psi run --vscode')
    else:
        print(pad + 'psi run --vscode')
        print('PS: You will probably need to override platform with: debugDefaultTargetPlatformOverride = TargetPlatform.android;')
