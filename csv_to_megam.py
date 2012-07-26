#!/usr/bin/env python

# Script that converts from CSV to MegaM format

# Author: Dan Blanchard, dblanchard@ets.org, June 2012

import argparse
import sys


def sanitize_name(feature_name):
    '''
        Replaces bad characters in feature names.
    '''
    return feature_name.replace(" ", "_").replace("#", "HASH")


if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Takes a delimited file with a header line and converts it to MegaM.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infile', help='MegaM input file', type=argparse.FileType('r'), default='-', nargs='?')
    parser.add_argument('-c', '--classfield', help='Index of class field in CSV file. Note: fields are numbered starting at 0.', default=-1, type=int)
    parser.add_argument('-d', '--delimiter', help='The column delimiter.', default=',')
    parser.add_argument('-i', '--idfield', help='Index of ID field in CSV file (if there is one). This will be included as a comment before each line. Note: fields are numbered starting at 0.', type=int)
    args = parser.parse_args()

    if args.infile.isatty():
        print >> sys.stderr, "You are running this script interactively. Press CTRL-D at the start of a blank line to signal the end of your input. For help, run it with --help\n"

    # Initialize variables
    classes = set()
    instances = []
    fields = []

    # Iterate through input file
    first = True
    for line in args.infile:
        split_line = line.strip().split(args.delimiter)
        if first:
            fields = split_line[1:] if split_line[0] == '#' else split_line  # Check for weird commented-out header
            fields = [sanitize_name(field) for field in fields]
            # Delete extra fields
            if args.idfield is not None:
                # Have to sort descending so that we don't screw up the indices
                for i in sorted((args.idfield, args.classfield), reverse=True):
                    del fields[i]
            else:
                del fields[args.classfield]
            first = False
        else:
            # Delete extra fields
            if args.idfield is not None:
                # Print id field
                print "# {}".format(split_line[args.idfield])

                # Print class
                sys.stdout.write('{}\t'.format(split_line[args.classfield]))

                # Have to sort descending so that we don't screw up the indices
                for i in sorted((args.idfield, args.classfield), reverse=True):
                    del split_line[i]
            else:
                # Print class
                sys.stdout.write('{}\t'.format(split_line[args.classfield]))
                del split_line[args.classfield]

            # Print features
            print ' '.join(['{} {}'.format(field, value) for field, value in zip(fields, split_line) if value not in ['.', '?'] and float(value) != 0])
