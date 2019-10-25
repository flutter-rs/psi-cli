import argparse
from .subcmds.create import run as run_create
from .subcmds.build import run as run_build
from .subcmds.run import run as run_run
from .subcmds.precache import run as run_precache

def main():
    parser = argparse.ArgumentParser(prog='psi', description='flutter-rs devtool')
    subparsers = parser.add_subparsers(title="Subcommands")

    create_parser = subparsers.add_parser('create', description='Create a flutter-rs app', help='Create a flutter-rs app')
    create_parser.add_argument('proj', help='A new project name')
    create_parser.set_defaults(func=run_create)

    run_parser = subparsers.add_parser('run', description='Run a flutter-rs app in dev mode', help='Run a flutter-rs app in dev mode')
    run_parser.add_argument('--vscode', action='store_true', help='Generate vscode launch.json file')
    run_parser.set_defaults(func=run_run)

    build_parser = subparsers.add_parser('build', description='Bundle a flutter-rs app for distribution', help='Bundle a flutter-rs app for distribution')
    build_parser.add_argument('dist', choices=['mac', 'dmg', 'nsis', 'snap'], help='distribution type')
    build_parser.add_argument('--release', action='store_true', help='build release package')
    build_parser.set_defaults(func=run_build)

    precache_parser = subparsers.add_parser('precache', description='Precache flutter engine library', help='Precache flutter engine library')
    precache_parser.set_defaults(func=run_precache)
    
    args = parser.parse_args()
    if hasattr(args, 'func') and callable(args.func):
        args.func(args)
    else:
        parser.print_help()
