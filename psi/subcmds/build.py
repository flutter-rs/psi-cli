#!/usr/bin/env python3
import os, sys
import toml
import argparse
from ..utils import look_for_proj_dir, get_flutter_version, get_workspace_dir, flutter_proj_dir
import subprocess

FLUTTER = 'flutter.bat' if sys.platform == 'win32' else 'flutter'

def collect_env(args):
    PROJ_DIR = flutter_proj_dir()
    RUST_PROJ_DIR = os.path.join(PROJ_DIR, 'rust')
    RUST_ASSETS_DIR = os.path.join(RUST_PROJ_DIR, 'assets')
    TOML_FILE = os.path.join(RUST_PROJ_DIR, 'Cargo.toml')
    META = toml.loads(open(TOML_FILE).read())
    CONFIG = toml.loads(open(os.path.join(RUST_PROJ_DIR, 'build.toml')).read())
    NAME = META['package']['name']
    VERSION = META['package']['version']
    DESCRIPTION = META['package']['description']

    DEBUG = not args.release
    RELEASE = args.release

    TARGET_DIR = os.path.join(RUST_PROJ_DIR, 'target')
    WORKSPACE = get_workspace_dir(RUST_PROJ_DIR)
    WORKSPACE_TARGET_DIR = os.path.join(WORKSPACE, 'target') if WORKSPACE else None
    OUTPUT_DIR = os.path.join(TARGET_DIR, 'debug' if DEBUG else 'release')
    FLUTTER_LIB_VER = get_flutter_version()
    FLUTTER_ASSETS = os.path.join(os.path.dirname(RUST_PROJ_DIR), 'build', 'flutter_assets')
    return locals()

def cargo_build(cwd, release = False):
    args = ['cargo', 'build']
    if release:
        args.append('--release')
    subprocess.run(args, cwd = cwd)

def build_flutter(envs):
    subprocess.run([FLUTTER, 'build', 'bundle'], cwd = envs['PROJ_DIR'])

def run(args):
    envs = collect_env(args)

    print('🍀  Building flutter bundle')
    build_flutter(envs)

    print('🦀  Building rust project')
    cargo_build(envs['RUST_PROJ_DIR'], envs['RELEASE'])

    print('🐶  Creating distribution')
    # prepare has a chance to modify envs
    if args.dist == 'mac':
        from ..utils.build_mac import prepare, build
        envs = prepare(envs)
        output = build(envs)
    elif args.dist == 'dmg':
        from ..utils.build_mac import prepare, build
        envs = prepare(envs)
        build(envs)

        from ..utils.build_dmg import prepare, build
        envs = prepare(envs)
        output = build(envs)
    elif args.dist == 'snap':
        from ..utils.build_snap import prepare, build
        envs = prepare(envs)
        output = build(envs)
    elif args.dist == 'nsis':
        from ..utils.build_nsis import prepare, build
        envs = prepare(envs)
        output = build(envs)
    print('🍭  {} distribution generated at {}'.format(args.dist, output))
