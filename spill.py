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

def query_yes_no(prompt, default="yes"):
    """
    This function queries the user for a yes/no via the console
    :param prompt: The prompt to ask the user
    :param default: The default answer that is selected by pressing enter
    :return: True if the user responded to the prompt with yes, false if no
    """
    yes = {"yes", "y", "ye"}
    no = {"no", "n"}
    exit_responses = {"exit", "quit", "stop"}

    if default is True or default in yes:
        yes.add("")
        options_text = "Y/n"
    elif default is False or default in no:
        no.add("")
        options_text = "y/N"
    elif default is None:
        options_text = "y/n"
    else:
        raise ValueError

    stdout = "{prompt} [{options}] ".format(prompt=prompt, options=options_text)

    while True:
        response = input(stdout).lower()
        if response in yes:
            return True
        elif response in no:
            return False
        elif response in exit_responses:
            exit()
        else:
            print("Answer with yes/no/exit.")

def parse_arguments():
    description = "This command line utility spills the contents of a directory"
    parser = argparse.ArgumentParser(description=description)

    file_group = parser.add_argument_group("Files")
    file_group.add_argument("directory", nargs=1, help="The directory to be spilled")
    file_group.add_argument("destination", nargs='?', help="Destination to spill into")

    options_group = parser.add_argument_group("Options")
    options_group.add_argument("-k", "--keep-directory", dest="keep", action="store_true", help="Keep spilled directory")
    options_group.add_argument("-f", "--overwrite", action="store_true", help="Overwrite files")

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
        logging.basicConfig(format='[spill][%(levelname)s] - %(message)s')

def cant_modify(path):
    return not os.access(path, os.R_OK) or not os.access(path, os.W_OK)

def check_permissions(spilled, destination=None):
    logger.debug("Checking permissions: %s" % spilled)

    if not os.path.isdir(spilled):
        logger.error("Not a directory: %s" % spilled)
        exit(1)

    if cant_modify(spilled):
        logger.error("Cannot modify: %s, exiting without spilling" % spilled)
        exit(1)

    if destination:
        if os.path.exists(destination) and not os.path.isdir(destination):
            logger.error("Destination: %s exists and is not a directory. Exiting" % destination)
            exit(1)
        if not os.path.exists(destination): return
        else:
            logger.debug("Checking permissions: %s" % destination)
            if cant_modify(destination):
                logger.error("Cannot modify destination: %s" % destination)
                exit(1)


def spill_directory(directory, destination, keep=False, overwrite=False):

    if (destination and not os.path.exists(destination)):
        logger.info("Making directory: %s" % destination)
        try: os.makedirs(destination)
        except:
            logger.error("Could not create create directory: %s exiting without spilling" % destination)
            exit()

    num_files_moved = 0
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)

        if cant_modify(full_path):
            logger.warning("Could not move %s: permission denied" % file)
            keep=True
            continue

        new_filename = os.path.join(destination, file)
        if os.path.exists(new_filename):
            if not overwrite and not query_yes_no("%s exists. Overwrite?" % new_filename, default="no"):
                logger.info("Did not move: %s" % new_filename)
                continue

        logger.info("Moving %s..." % file)
        os.rename(full_path, new_filename)
        num_files_moved += 1

    if not keep and os.listdir(directory) == []:
        logger.info("Removing %s (now empty)" % directory)
        os.rmdir(directory)
    else:
        logger.info("Not removing: %s" % directory)

    logger.info("Spill complete. Files moved: %d" % num_files_moved)

def main():
    args = parse_arguments()
    setup_logging(args)

    spilled = os.path.abspath(args.directory[0])
    destination = args.destination if args.destination else os.path.dirname(spilled)

    check_permissions(spilled, destination=destination)
    spill_directory(spilled, destination, keep=args.keep, overwrite=args.overwrite)

if __name__ == "__main__":
    main()