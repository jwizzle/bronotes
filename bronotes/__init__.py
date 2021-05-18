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


def main():
    """Entry point for bronotes."""
    # Create the CLI argument parser.
    parser = get_main_parser()

    # TODO The amount of comments here indicate that the code should be simpler
    # Nasty things to juggle CLI arguments around for different actions
    # If there's no arguments given just escape this whole mess and parse
    # things directly
    if len(sys.argv) == 1:
        (args, extra_args) = parser.parse_known_args()
    # We need to capture -h and --help because exec eats everything
    # so having it set as a default action prevents -h usage.
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        (args, extra_args) = parser.parse_known_args(['-h'])
    # If the first argument is not in the actionlist pass following arguments
    # to the default action
    elif (
            sys.argv[1][0] != '-' and
            sys.argv[1] not in get_actions(names_only=True)
          ):
        arglist = [cfg.default_action] + sys.argv[1:]
        (args, extra_args) = parser.parse_known_args(arglist)
    # If non of the others apply just parse arguments normally
    else:
        (args, extra_args) = parser.parse_known_args()

    # If no arguments are given always assume the list action because it's
    # basically the only one that works without any arguments.
    if not hasattr(args, 'action'):
        list_action = ActionList
        args.action = list_action
        args.dir = ''

    # Replace the action arg with an instantiated object.
    args.action = args.action()
    args.action.init(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # TODO Figure out a more generic way to handle the 'completions' and 'exec'
    # exceptions that are currently made here
    try:
        if args.action.action == 'completions':
            print(args.action.process(parser))
        elif args.action.action == 'exec':
            print(args.action.process(extra_args))
        else:
            print(args.action.process())
    except Exception as exc:
        logging.debug(exc)
        print("There was an uncaught exception, \
use --debug to show more info. And throw some output and what you \
were doing to the dev while you're at it.")
