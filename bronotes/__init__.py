"""Contain the main function of bronotes."""
import argparse
import logging
import sys
import os
import importlib
import inspect
from bronotes.config import cfg
from bronotes.actions.list import ActionList


def get_actions(names_only=False):
    """Generate action classes.

    This scrapes the bronotes/actions folder for files. Then extracts
    all classes that contain 'Action' (except BronoteAction) and yields
    them.

    Parameters:
        names_only: Return only the actions name/command, default is False.

    Yields:
        BronoteAction: An uninstantiated bronote action.
        String: Or just the command/name of the actions.
    """
    ignore_files = ['__init__.py', 'base_action.py']

    for file in os.listdir('bronotes/actions/'):
        if file in ignore_files:
            continue

        for name, cls in inspect.getmembers(
            importlib.import_module(f"bronotes.actions.{file[:-3]}"),
            inspect.isclass
        ):
            if 'Action' in name and name != 'BronoteAction':
                if names_only:
                    yield cls.action
                else:
                    yield cls


def get_main_parser():
    """Get the main parser.

    Loops through actions to create subparsers.
    """
    cfg.init()
    parser = argparse.ArgumentParser(prog='bnote')
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Set loglevel to debug.'
    )
    subparsers = parser.add_subparsers(
        help='Bronote actions.', metavar='action')

    for action in get_actions():
        action.add_subparser(subparsers)

    return parser


def parse_args(parser):
    """Parse CLI arguments."""
    parser_args = None

    if len(sys.argv) == 1:
        parser_args = ['list']
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        parser_args = ['-h']
    elif (
            sys.argv[1][0] != '-' and
            sys.argv[1] not in get_actions(names_only=True)
          ):
        parser_args = [cfg.default_action] + sys.argv[1:]

    return parser.parse_known_args(parser_args)


def main():
    """Entry point for bronotes."""
    parser = get_main_parser()
    (args, extra_args) = parse_args(parser)

    # Replace the action arg with an instantiated object.
    args.action = args.action()
    args.action.init(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        print(args.action.process(
            parser=parser,
            extra_args=extra_args
        ))
    except Exception as exc:
        logging.debug(exc)
        print("There was an uncaught exception, \
use --debug to show more info. And throw some output and what you \
were doing to the dev while you're at it.")
