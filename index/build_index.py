#!/usr/bin/env python
import sys
import pickle

import docreader
import simple9
import varbyte

if __name__ == '__main__':
    encoding = sys.argv[1]
    files = sys.argv[2:]
    data = {'encoding': encoding, 'index': {}, 'urls': []}
    reader = docreader.DocumentStreamReader(files)
    buf = dict()  # for simple9
    for doc in reader:
        words = set(docreader.extract_words(doc.text))
        data['urls'].append(doc.url.encode('utf-8'))
        words = [w.encode('utf-8') for w in words]
        url_pos = len(data['urls']) - 1
        for w in words:
            if encoding == 'varbyte':
                if w in data['index']:
                    data['index'][w] += varbyte.vb_encode(url_pos)
                else:
                    data['index'][w] = varbyte.vb_encode(url_pos)
            elif encoding == 'simple9':
                if w in data['index']:
                    buf[w].append(url_pos)
                    if len(buf[w]) >= 1000:
                        data['index'][w].append((len(buf), simple9.encode_arr(buf[w])))
                        buf[w] = []
                else:
                    buf[w] = [url_pos]
                    data['index'][w] = []

    if encoding == 'simple9': # compress rest buffers
        for w, nums in buf.items():
            data['index'][w].append((len(nums), simple9.encode_arr(nums)))

    pickle.dump(data, open("index_15.p", "wb"))
