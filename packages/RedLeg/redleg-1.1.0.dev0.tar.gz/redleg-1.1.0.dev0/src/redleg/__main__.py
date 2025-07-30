#!/usr/bin/env python3
"""Simple ledger application"""

import sys
import logging
import argparse
from .ui import UI

__version__ = "1.1.0-dev0"

# ? Constants
# The format for the logging msg
LOGGING_FORMAT = "[%(levelname)s]: %(message)s"


# Set up argument parser with the program details
parser = argparse.ArgumentParser(
    prog="RedLeg",  # Program name
    description="The simple ledger application",  # Description
    epilog="..."  # Epilog (did'nt really know what to put their)
)
# Version argument
parser.add_argument(
    "--version",
    action="version",  # Make sure argparse knows its for the version
    version=__version__,  # Pass it the version
    help="Displays the version then exits"
)
parser.add_argument(
    "file",
    help="The ledger file"
)
# Set up subparser
subparsers = parser.add_subparsers(
    required=True,
    dest="command"  # Put this here so we know what command is called
)
# Subparser for register command
registerCommand = subparsers.add_parser(
    "register",
    help="Prints the register"
)
# Subparser for transaction command
transactionCommand = subparsers.add_parser(
    "transaction",
    help="Make a transaction"
)
# Subparser for account command
accountCommand = subparsers.add_parser(
    "accounts",
    help="Print the value of all accounts"
)
# Subparser for statement command
statementCommand = subparsers.add_parser(
    "statement",
    help="Prints out a statement"
)

# If no arguments are passed
if len(sys.argv) == 1:  # Set to 1 cause sys.argv[0] is the program name
    parser.print_help()
    sys.exit(2)  # Exit 2 cause of argparse error
else:  # Else parser the  args
    args = parser.parse_args()

# Get the logger for the module
logger = logging.getLogger(__name__)
# Set up the formatter object
formatter = logging.Formatter(fmt=LOGGING_FORMAT)
# Set up console handler
streamHandler = logging.StreamHandler()
# Set the formatter for the console handler
streamHandler.setFormatter(formatter)
# Add the handler to logger
logger.addHandler(streamHandler)
# Set logging level
if __debug__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.info)


def main() -> int:
    """Handles text user interface"""
    try:
        ui = UI(args.file)
        ui.command(args.command)
    # In case ctrl+c is pressed
    except KeyboardInterrupt:
        logger.error("\nCtrl+C pressed, quitting...")
        return 3221225786  # Ctrl+c exit code
    # In case they tamper with the ledger file and we get a key error
    except KeyError as e:
        logger.critical("Key: '%s' was missing from ledger file.", e)
        return 1  # Error
    finally:
        exit_code = ui.done()

    return exit_code  # Success


def tui() -> int:
    """Handles curses code"""
    pass


# In case we are executing this script by itself
if __name__ == "__main__":
    # Take care of exiting just like in the hatch generated script
    sys.exit(main())
