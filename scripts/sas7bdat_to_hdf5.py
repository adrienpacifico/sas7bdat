#!/usr/bin/env python


import logging
import optparse
import os
import sys

import pandas as pd

from sas7bdat import SAS7BDAT


def main(options, args):
    logLevel = logging.DEBUG if options.debug else logging.INFO
    input_paths = [args[0]]
    if len(args) == 1:
        output_paths = ['%s.csv' % os.path.splitext(args[0])[0]]
    elif len(args) == 2 and (args[1] == '-' or args[1].lower().endswith('.csv')):
        output_paths = [args[1]]
    else:
        assert all(x.lower().endswith('.sas7bdat') for x in args)
        input_paths = args
        output_paths = ['%s.csv' % os.path.splitext(x)[0] for x in input_paths]
    assert len(input_paths) == len(output_paths)
    for input_path , output_path in zip(input_paths, output_paths):
        parser = SAS7BDAT(input_path, logLevel = logLevel)
        if options.header:
            parser.logger.info(str(parser.header))
            continue
        rows_iter = parser.readData()
        columns = rows_iter.next()
        data_frame = pd.DataFrame(
            (
                row
                for row in rows_iter
                if row
                ),
            columns = columns,
            )
        print data_frame


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
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    main(options, args)
