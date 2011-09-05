"""Simple CSV to ARFF Converter"""
import os
import sys
import csv
import datetime
import StringIO
from optparse import OptionParser
from collections import defaultdict

# Only numeric, string and nominal supported in this version
TYPES = ('numeric', 'string', 'nominal')


def types_valid(types):
    for type_ in types.split(','):
        if type_ not in TYPES:
            return False
    return True


def convert(filename, relation, typespec, header):
    nominal_values = defaultdict(set)
    is_nominal_column = [t == 'nominal' for t in typespec.split(',')]
    with open(filename) as fh:
        reader = csv.reader(fh)
        if header:
            reader.next()
        # In case there are nominal values we need
        # to traverse the data first to collect the values
        data = StringIO.StringIO()
        writer = csv.writer(
            data, doublequote=False,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar='\\')
        while True:
            try:
                line = reader.next()
                for i, (nominal, value) in enumerate(zip(is_nominal_column, line)):
                    if nominal:
                        nominal_values[i].add(value)
            except StopIteration:
                break
            writer.writerow(line)
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
            if nominal_values[i]:
                sys.stdout.write('@attribute x%s {"%s"}\n' % (i, '","'.join(nominal_values[i])))
            else:
                sys.stdout.write('@attribute x%s %s\n' % (i, type_))
        print '%' * 79
        print '@data'
        sys.stdout.write(data.getvalue())


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
