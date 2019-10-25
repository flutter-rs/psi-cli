#!/usr/bin/env python3
import os
import glob
import subprocess
from ..utils import look_for_proj_dir, tmpl_file
from ..utils.download import download_flutter_engine

REPO = 'https://github.com/flutter-rs/flutter-app-template'

def get_tmpl_config(proj_dir):
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

def tmpl_proj(proj_dir, config):
    tmplfiles = get_tmpl_config(proj_dir)

    for pattern in tmplfiles:
        for fp in glob.iglob(os.path.join(proj_dir, pattern)):
            fp = os.path.join(proj_dir, fp)
            if os.path.isfile(fp):
                tmpl_file(fp, config)

def create_project(args):
    proj_name = args.proj.replace('_', '-')
    lib_name = proj_name.replace('-', '_')

    subprocess.run(['git', 'clone', REPO])

    config = {
        "name": proj_name,
        "lib_name": lib_name, # underlined version of name
    }

    proj_dir = os.path.join(os.getcwd(), proj_name)
    tmpl_proj(proj_name, config)
    
    # remove .tmplfile, useless now
    tmplfile_path = os.path.join(proj_dir, '.tmplfiles')
    os.remove(tmplfile_path)

def run(args):
    print('🔮  Creating files')
    create_project(args)

    print('🧩  Downloading flutter-engine')
    download_flutter_engine()

    print('🍭  Done! Happy coding.')
