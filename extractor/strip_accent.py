#!/usr/bin/env python

import unicodedata
import fileinput
import sys

def strip_accents(s):
    """
    Removes accented characters from a string
    """
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def remove_accents(input_str):
    """
    Converts accented characters to the closest unaccented analogue
    """
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def main():
    for line in fileinput.input():
        sys.stdout.write(remove_accents(unicode(line, errors='ignore')))

if __name__ == '__main__':
    main()
