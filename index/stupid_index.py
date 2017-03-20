import sys
import pickle

import docreader

if __name__ == '__main__':
    files = sys.argv[1:]
    reader = docreader.DocumentStreamReader(files)
    index = dict()
    for doc in reader:
        words = set(docreader.extract_words(doc.text))
        for w in words:
            index[w] = index.get(w, []) + [doc.url]

    print(len(index))

    pickle.dump(index, open("index.p", "wb"))
