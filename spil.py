#!/usr/bin/env python
"""
This basic utility spills the contents of a directory.

Usage: spill myDirectory target

This command would take all files and directories in myDirectory
and move them to the target directory (creating it if it does not already exist)
and then delete myDirectory if it has become empty.
"""

import os
import sys
import argparse
import logging

__version__ = 1.0
__author__ = "Jonathan Deaton (jdeaton@stanford.edu)"
__license__ = "None"

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
        logging.basicConfig(format='[%(asctime)s][%(levelname)s] - %(message)s')
    else:
        logger.setLevel(logging.WARNING)
        logging.basicConfig(format='[log][%(levelname)s] - %(message)s')

def cant_modify(path):
    return not os.access(path, os.R_OK) or not os.access(path, os.W_OK)

def check_permissions(spilled, destination=None):
    logger.debug("Checking permissions of: %s")

    if not os.path.isdir(spilled):
        logger.error("No directory: %s" % spilled)
        exit(1)

    if cant_modify(spilled):
        logger.error("Cannot modify: %s, exiting without spilling" % spilled)
        exit(1)

    if destination:
        logger.debug("coisjf")


def spill_directory(directory, destination, keep=False):

    for file in os.listdir(directory):
        full_path = os.path.join(directory)
        if cant_modify(full_path):
            logger.warning("Could not move: %s" % file)


def main():
    args = parse_arguments()
    setup_logging(args)

    spilled = os.path.abspath(args.directory[0])
    destination = args.destination if args.destination else os.path.dirname(spilled)

    check_permissions(spilled, destination=destination)
    spill_directory(spilled, destination, keep=args.keep)

if __name__ == "__main__":
    main()