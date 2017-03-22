#!/usr/bin/env python
import pickle
import sys
import time

import numpy as np

import simple9
import varbyte


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
    start_time = time.time()
    index = pickle.load(open("index_20.p", "rb"))
    sys.stderr.write("index loaded, take {} seconds\n".format(time.time() - start_time))
    encoding = index['encoding']
    for query in sys.stdin:
        words = [w.strip() for w in query.split('&')]
        words = [w.decode('utf-8').lower().encode('utf-8') for w in words]
        docs = []
        for w in words:
            if w in index['index']:
                if encoding == 'varbyte':
                    docs.append(varbyte.vb_decode(index['index'][w]))
                elif encoding == 'simple9':
                    compressed_bytes = index['index'][w][0]
                    urls_count = index['index'][w][1]
                    ints = np.fromstring(compressed_bytes, dtype=np.dtype(int))
                    docs.append(simple9.decode_arr(ints)[:urls_count])
                    # buffers = index['index'][w]
                    # data = []
                    # for sz, buf in buffers:
                    #    data.append(simple9.decode_arr(buf)[:sz])
                    # docs.append(sum(data, []))  # flatmap

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


