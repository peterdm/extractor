import extractor
import csv
import pprint
import sys

def read_file(filename):

    fieldnames = ('url', 'title', 'description', 'keywords', 'oldextract')
    
    pp = pprint.PrettyPrinter(indent=4)
    e = extractor.Extractor(5, '../data/dictionary.txt', '../data/stopwords.txt', True)

    with open(filename, 'r') as f:
        reader = csv.DictReader(f, fieldnames)
        for row in reader:
            
            currentSet = manually_parse_for_badly_quoted_keywords(row['keywords'])

            testSet = e.extract(row['keywords'])
#            testSet.update(e.extract(row['title']))
#            testSet.update(e.extract(row['description']))

            if ( testSet != currentSet ):

                print row['url']
                if 'title' in row:
                    print 'Title: ' + row['title']
                if 'description' in row:
                    print 'Description: ' + row['description']
                if 'keywords' in row:
                    print 'Keywords: ' + row['keywords']

                adds = testSet.difference(currentSet)
                subs = currentSet.difference(testSet)

                if adds:
                    print '---------------------------------------'
                    print 'Test Code Adds: '
                    pp.pprint(adds)

                if subs:
                    print '---------------------------------------'
                    print 'Test Code Filters Out: '
                    pp.pprint(subs)

                print '=======================================\n'

def manually_parse_for_badly_quoted_keywords(str):
    if str:
        kw = [ s.strip(' "\'').lower() for s in str.split(',') ]
        return set(filter(None, kw))
    else:
        return set()

def main():
    read_file(sys.argv[1])



if __name__ == "__main__":
    main()
