#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    Davis runner

"""
__version__ = 0.1

import sys
import urllib
import json
import webbrowser

URL = "http://localhost:8080/"

def usage():
    prog_name = sys.argv[0]
    return '''Usage: %(prog_name)s [--label "this is title"] [--lines|--bars] data
''' % locals()

def argv2param(argv):
    label = None
    data  = []

    # iterate over arguments
    i = 0
    while i < len(argv):
        if argv[i] == '--label':
            label = argv[i+1]
            i += 1
        else:
            data.append(argv[i])
        i += 1


    # create param dictionary
    param_d = { 'data': ",".join(data) }
    if label:
        param_d['label'] = label
    return param_d

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print usage()
        sys.exit(1)

    param_d = argv2param(sys.argv[1:])
    param = urllib.urlencode(param_d)
    webbrowser.open(URL + '?%s' % param)


# vim: sts=4 et
