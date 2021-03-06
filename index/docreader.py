#!/usr/bin/env python
from __future__ import print_function
import argparse
import gzip
import re
import struct

import document_pb2

SPLIT_RGX = re.compile(r'\w+', re.U)


def extract_words(text):
    words = re.findall(SPLIT_RGX, text)
    return map(lambda s: s.lower(), words)


class DocumentStreamReader:
    def __init__(self, paths):
        self.paths = paths

    def open_single(self, path):
        return gzip.open(path, 'rb') if path.endswith('.gz') else open(path, 'rb')

    def __iter__(self):
        for path in self.paths:
            with self.open_single(path) as stream:
                while True:
                    sb = stream.read(4)
                    if sb == '':
                        break

                    size = struct.unpack('i', sb)[0]
                    msg = stream.read(size)
                    doc = document_pb2.document()
                    doc.ParseFromString(msg)
                    yield doc


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()


if __name__ == '__main__':
    reader = DocumentStreamReader(parse_command_line().files)
    for doc in reader:
        print ("%s\t%d bytes" % (doc.url, len(doc.text)))

