"""Simple CSV to ARFF Converter"""
import os
import sys
import csv
import datetime
import StringIO
from optparse import OptionParser

# Only numeric and string supported in this version
TYPES = ('numeric', 'string')


def types_valid(types):
    for type_ in types.split(','):
        if type_ not in TYPES:
            return False
    return True


def convert(filename, relation, types, header):
    with open(filename) as fh:
        reader = csv.reader(fh)
        if header:
            reader.next()
        print '%'
        print '%% Generated by %s' % sys.argv[0]
        print '%'
        print '%% at %s ' % datetime.datetime.now().isoformat()
        print '%'
        print '%% on %s' % os.uname()[1]
        print '%'
        print '@relation %s' % relation
        print '%'
        for i, type_ in enumerate(typespec.split(',')):
            print '@attribute x%s %s' % (i, type_)
        print '%' * 79
        print '@data'
        writer = csv.writer(
            sys.stdout, doublequote=False,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar='\\')
        while True:
            try:
                line = reader.next()
            except StopIteration:
                break
            writer.writerow(line)


if __name__ == '__main__':
    usage = "usage: %prog [options] filename relationname typespec (comma separated)"
    parser = OptionParser(usage=usage)
    parser.add_option("-H", "--header",
                      dest="header",
                      action="store_true",
                      help="Set to true if file contains a header line. "
                      "Header lines will be ignored, so this must be set "
                      "to avoid the header line being treated as data.",
                      default=False)
    options, args = parser.parse_args()
    if len(args) < 3:
        parser.error('Please specifiy filename, relationship and typespec.')
    if not types_valid:
        parse.error('Valid types are: %s' % (','.join(TYPES)))
    filename, relation, typespec = args
    convert(filename, relation, typespec, options.header)
