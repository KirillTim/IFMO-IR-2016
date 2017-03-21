#!/usr/bin/env python
import sys
import pickle

import docreader

if __name__ == '__main__':
    encoding = sys.argv[1]
    files = sys.argv[2:]
    reader = docreader.DocumentStreamReader(files)
    data = {'index': dict(), 'urls': []}
    for doc in reader:
        words = set(docreader.extract_words(doc.text))
        words = [w.encode('utf-8') for w in words]
        count = 0
        index = data['index']
        data['urls'].append(doc.url.encode('utf-8'))
        for w in words:
            index[w] = index.get(w, []) + [len(data['urls']) - 1]

    pickle.dump(data, open("index.p", "wb"))
