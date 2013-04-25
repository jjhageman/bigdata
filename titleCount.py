### titleCount.py
import glob
import string
import mincemeat


text_files = glob.glob('hw3data/*')

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source_data = {}

for file_name in text_files:
    c = file_contents(file_name)
    for line in c.splitlines():
         sect = line.split(':::')
         title = sect[-1]
         for author in sect[-2].split('::'):
             source_data[author] = sect[-1]

def mapfn(key, value):
    for word in value.split():
        #if word in allStopWords:
            #pass
        #else:
            yield word.translate(None, string.punctuation).lower(), 1

def reducefn(key, value):
    return key, len(value)

s = mincemeat.Server()
s.datasource = source_data
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password='changeme')
print results
