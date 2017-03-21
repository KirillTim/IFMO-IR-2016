#!/usr/bin/env python
import sys
import pickle
from pprint import pprint

if __name__ == '__main__':
    data = pickle.load(open("index.p", "rb"))
    index = data['index']
    urls = data['urls']
    sys.stderr.write("index loaded\n")

    for query in sys.stdin:
        words = [w.strip() for w in query.split('&')]
        words = [w.decode('utf-8').lower().encode('utf-8') for w in words]
        docs = []
        for w in words:
            if w in index:
                docs.append(index[w])
        print (query[:-1])
        if len(docs) > 0:
            rv = set(docs[0])
            for d in docs[1:]:
                rv &= set(d)
            print (len(rv))
            rv = list(sorted(rv))
            for idx in rv:
                print (urls[idx])
        else:
            print (0)
