### titleCount.py
import glob
import string
import mincemeat
import stopwords
from stopwords import allStopWords

text_files = glob.glob('hw3data/*')

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source = dict((file_name, file_contents(file_name))
        for file_name in text_files)

#source_data = {}

#for file_name in text_files:
    #c = file_contents(file_name)
    #for line in c.splitlines():
         #sect = line.split(':::')
         #title = sect[-1]
         #for author in sect[-2].split('::'):
             #source_data[author] = sect[-1]

def mapfn(key, value):
    w={}
    for line in value.splitlines():
        sect = line.split(':::')
        title = sect[-1]
        for author in sect[-2].split('::'):
            auth = author.lower()
            if auth in w.keys():
                for word in title.split():
                    wrd = word.translate(None, string.punctuation).lower()
                    if wrd in allStopWords.keys():
                        pass
                    else:
                        if wrd in w[auth].keys():
                            w[auth][wrd] += 1
                        else:
                            w[auth][wrd] = 1
            else:
                w[auth] = {}
                for word in title.split():
                    if word in allStopWords.keys():
                        pass
                    else:
                        w[auth][word.translate(None, string.punctuation).lower()] = 1

    for k in w.keys():
        yield k, w[k]
        

def reducefn(key, value):
    new_sum = value.pop()
    for title in value:
        new_sum = dict( (n, new_sum.get(n, 0)+title.get(n, 0)) for n in set(new_sum)|set(title) )
    return key, sorted(new_sum.iteritems(), key=operator.itemgetter(1), reverse=True)

s = mincemeat.Server()
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password='changeme')
print results
