"""Contain the main function of bronotes.

Todo:
    * Create a better search method for when a file is not found
"""
import argparse
import logging
import sys
from bronotes.config import cfg
from bronotes.actions.add import ActionAdd
from bronotes.actions.rm import ActionDel
from bronotes.actions.edit import ActionEdit
from bronotes.actions.list import ActionList
from bronotes.actions.mv import ActionMove
from bronotes.actions.exec import ActionExec
from bronotes.actions.set import ActionSet
from bronotes.actions.completions import ActionCompletions
from bronotes.actions.show import ActionShow
from bronotes.actions.sync import ActionSync

actions = [
    ActionAdd(cfg),
    ActionDel(cfg),
    ActionList(cfg),
    ActionEdit(cfg),
    ActionMove(cfg),
    ActionSet(cfg),
    ActionCompletions(cfg),
    ActionShow(cfg),
    ActionSync(cfg),
    ActionExec(cfg),
]
actionlist = [action.action for action in actions]


def get_main_parser():
    """Get the main parser."""
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

    for action in actions:
        action.add_subparser(subparsers)

    return parser


def main():
    """Entry point for bronotes."""
    parser = get_main_parser()

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
            sys.argv[1] not in actionlist
          ):
        arglist = [cfg.default_action] + sys.argv[1:]
        (args, extra_args) = parser.parse_known_args(arglist)
    # If non of the others apply just parse arguments normally
    else:
        (args, extra_args) = parser.parse_known_args()

    if not hasattr(args, 'action'):
        list_action = ActionList(cfg)
        args.action = list_action
        args.dir = ''

    args.action.init(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

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
