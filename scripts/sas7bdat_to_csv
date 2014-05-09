#!/usr/bin/env python


import csv
import logging
import optparse
import os
import sys

from sas7bdat import SAS7BDAT


def convert_file(parser, output_path, delimiter=',', stepSize=100000):
    parser.logger.debug("Input: %s\nOutput: %s", parser.path, output_path)
    output_file = None
    try:
        if output_path == '-':
            output_file = sys.stdout
        else:
            output_file = open(output_path, 'w')
        out = csv.writer(output_file, lineterminator='\n', delimiter=delimiter)
        output_index = 0
        for input_index, row in enumerate(parser.readData(), 1):
            if not row:
                continue
            if not input_index % stepSize:
                parser.logger.info('%.1f%% complete', float(input_index) / parser.header.rowcount * 100.0)
            try:
                out.writerow(row)
            except IOError:
                parser.logger.warn('Wrote %d lines before interruption', output_index)
                break
            output_index += 1
        parser.logger.info('[%s] wrote %d of %d lines', os.path.basename(output_path), input_index - 1,
            parser.header.rowcount)
    finally:
        if output_file is not None:
            output_file.close()


def main(options, args):
    if options.debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    input_paths = [args[0]]
    if len(args) == 1:
        output_paths = ['%s.csv' % os.path.splitext(args[0])[0]]
    elif len(args) == 2 and (args[1] == '-' or
                             args[1].lower().endswith('.csv')):
        output_paths = [args[1]]
    else:
        assert all(x.lower().endswith('.sas7bdat') for x in args)
        input_paths = args
        output_paths = ['%s.csv' % os.path.splitext(x)[0] for x in input_paths]
    assert len(input_paths) == len(output_paths)
    for input_path , output_path in zip(input_paths, output_paths):
        parser = SAS7BDAT(input_path, logLevel=logLevel)
        if options.header:
            parser.logger.info(str(parser.header))
            continue
        convert_file(parser, output_path,
                     delimiter=options.delimiter,
                     stepSize=options.progress_step)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.set_usage("""%prog [options] <infile> [outfile]

  Convert sas7bdat files to csv. <infile> is the path to a sas7bdat file and
  [outfile] is the optional path to the output csv file. If omitted, [outfile]
  defaults to the name of the input file with a csv extension. <infile> can
  also be a glob expression in which case the [outfile] argument is ignored.

  Use --help for more details""")
    parser.add_option('-d', '--debug', action='store_true', default=False,
                      help="Turn on debug logging")
    parser.add_option('--header', action='store_true', default=False,
                      help="Print out header information and exit.")
    parser.add_option('--delimiter', action='store', default=',',
                      help="Set the delimiter in the output csv file. "
                           "Defaults to '%default'.")
    parser.add_option('--progress-step', action='store', default=100000,
                      metavar='N', type='int',
                      help="Set the progress step size. Progress will be "
                           "displayed every N steps. Defaults to %default.")
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    main(options, args)
