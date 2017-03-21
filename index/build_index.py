#!/usr/bin/env python
import sys
import pickle

import docreader
import encoders

if __name__ == '__main__':
    encoding = encoding = sys.argv[1]
    files = sys.argv[2:]
    data = {'index': {}, 'urls': []}
    reader = docreader.DocumentStreamReader(files)
    for doc in reader:
        words = set(docreader.extract_words(doc.text))
        data['urls'].append(doc.url)
        words = [w.encode('utf-8') for w in words]
        url_pos = len(data['urls'])
        for w in words:
            if w in data['index']:
                data['index'][w] += encoders.vb_encode(url_pos)
            else:
                data['index'][w] = encoders.vb_encode(url_pos)

    pickle.dump(data, open("index_15.p", "wb"))
