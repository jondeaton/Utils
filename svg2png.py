#!/usr/bin/python
'''
svg2png.py

This is a wrapper script that turns svgs in to pngs
Dependencies: librsvg
'''

import os
import sys
import argparse
import logging

__version__ = 1.0
__author__ = "Jonathan Deaton (jonpauldeaton@gmail.com)"
__license__ = "No license"

logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def convert_svg_to_png(svg_file, png_file):
    command = "rsvg-convert -h 2000 {SVG} > {PNG}".format(SVG=svg_file, PNG=png_file)
    os.system(command)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', required=True, help='Input directory or files containing SVG files')
    parser.add_argument('-out', '--output', required=False, help='Output directory where the PNG files will be placed.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    if os.path.exists(args.input):
        if os.path.isfile(args.input):
            svg_files = [os.path.abspath(args.input)]
            output_dir = os.path.dirname(args.input)
        elif os.path.isdir(args.input):
            svg_files = [file for file in os.listdir(args.input) if file.endswith('.svg')]
            output_dir = args.input
        else:
            logger.error("Not a file or directory: %s" % args.input)
            exit()
    else:
        logger.error("%s does not exist" % args.input)
        exit()

    output = os.path.expanduser(args.output)
    if args.output is not None and os.path.exists(output) and os.path.isdir(output):
        output_dir = output

    num_files = len(svg_files)
    for i in xrange(num_files):
        svg_file = svg_files[i]
        png_file = "%s.png" % os.path.splitext(os.path.basename(svg_file))[0]
        if output_dir is not None:
            png_file = os.path.join(output_dir, png_file)
        if args.verbose:
            logger.info("Converting: %s (%d of %d)" % (file, i, num_files))
        convert_svg_to_png(svg_file, png_file)

if __name__ == '__main__':
    main()
