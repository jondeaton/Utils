#!/usr/bin/env python
"""
This basic utility spills the contents of a directory.

Usage: spill myDirectory target

This command would take all files and directories in myDirectory
and move them to the target directory (creating it if it does not already exist)
and then delete myDirectory if it has become empty.
"""

import os
impos sys
import argparse
import logging

__version__ = 1.0
__author__ = "Jonathan Deaton (jdeaton@stanford.edu)"
__license__ = "No license"

logger = logging.getLogger("spill")

def parse_arguments():
    description = "This command line utility spills the contents of a directory"
    parser = argparse.ArgumentParser(description=description)

    file_group = parser.add_argument_group("Files")
    file_group.add_argument("directory", nargs=1, help="The directory to be spilled")
    file_group.add_argument("destination", nargs='?', help="Destination to spill into")

    options_group = parser.add_argument_group("Options")
    options_group.add_argument("-k", "--keep-directory", action="store_true", help="Keep spilled directory")

    console_options_group = parser.add_argument_group("Console Options")
    console_options_group.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    console_options_group.add_argument('--debug', action='store_true', help='Debug console')

    return parser.parse_args()

def setup_logging(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s')
    elif args.verbose:
        logger.setLevel(logging.INFO)
        logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s')
    else:
        logger.setLevel(logging.WARNING)
        logging.basicConfig(format='[log][%(levelname)s] - %(message)s')

def check_permissions():
    pass

def spil_directory(directory, destination=None):
    pass

def main():
    args = parse_arguments()
    setup_logging(args)

    spilled = args.directory[0]

    destination = args.destination if args.destination else os.path.dirname(spilled)

    check_permissions()
    spil_directory(spilled, destination=destination)

if __name__ == "__main__":
    main()