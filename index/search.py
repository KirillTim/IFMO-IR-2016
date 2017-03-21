#!/usr/bin/env python
import pickle
import sys

import encoders


def merge(a, b):
    rv = []
    i, j = (0, 0)
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            rv.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return rv

if __name__ == '__main__':
    index = pickle.load(open("index_15.p", "rb"))
    sys.stderr.write("index loaded\n")

    for query in sys.stdin:
        words = [w.strip() for w in query.split('&')]
        words = [w.decode('utf-8').lower().encode('utf-8') for w in words]
        docs = []
        for w in words:
            if w in index['index']:
                docs.append(encoders.vb_decode(index['index'][w]))

        docs = sorted(docs, key=lambda x: len(x))
        while len(docs) > 1 and len(docs[0]) > 0:
            rv = merge(docs[0], docs[1])
            docs = docs[1:]
            docs[0] = rv
        print (query[:-1])
        if len(docs) > 0:
            print (len(docs[0]))
            for d in docs[0]:
                print(index['urls'][d])
        else:
            print (0)


