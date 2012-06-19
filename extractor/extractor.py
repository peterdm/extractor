"""
The purpose of this class is to identify phrases from a dictionary in text
"""

import time
import re
from bloomfilter import BloomFilter
from ngramfilter import NGramFilter
from searcher import Searcher
from strip_accent import remove_accents

# ask for string, filter for ngrams, for each ngram, collect if bf && searcher, return collection

class Extractor:
    """
    Extractor Constants:    

    When you instantiate a BloomFilter, you will see the false-positive rate displayed.
    False-positives do not introduce any error, since all 'positive' terms are searched in
    the dictionary.  However, more false-positives means more unnecessary dictionary lookups,
    which will slow down extracts.

    The false-positive rate of the BloomFilter may be tuned with the parameters below:
    (Right now these settings reflect a dictionary size of approximately 10MM entries)

    BF_HASHES: The number of hash functions used by the BloomFilter.   The higher this number 
    is, the lower the false-positive rate drops.  However each hash must be computed for every 
    lookup, so keeping a smaller number of hashes speeds things up.

    BF_BYTES:  
    This is the size of the bitset in use by the BloomFilter.  The bigger the bitset, the lower
    the false-positive rate.  However, the larger the bitset, the more data needs to be read
    into memory at startup (and checked when searched)
    """

    BF_HASHES  = 5
    BF_BYTES   = 8192 * 1024  # 8MB


    def __init__(self, max_gram_size, dictionary_file, stopwords_file, use_bloomfilter=False):
        """
        Constructor arguments:
        max_gram_size -- The longest phrase (in words) you want to search for in the dictionary.
        The longer your grams, the more permutations generated (to be searched) adding time to the extract.

        dictionary_file -- The path to your dictionary file.  A sorted, lower-cased, list of phrases.

        stopwords_file -- The path to your stopwords file (words or phrases to be excluded).
        This file should also be sorted and lower-cased.

        use_bloomfilter -- Whether or not to use a BloomFilter.  If True extracts will run several
        times faster.  This takes several minutes to build the very first time you run it.
        """

        self.ngfilter = NGramFilter(max_gram_size)
        self.searcher = Searcher(dictionary_file)
	self.stopwords = Searcher(stopwords_file)
        if use_bloomfilter:
            f = open(dictionary_file)
            self.bloom = BloomFilter(self.BF_BYTES, self.BF_HASHES, iter(f))
        else:
            self.bloom = None
    


    def extract(self, text, case_sensitive=False, timing=False):
        """
        Extracts any phrases found in the dictionary (and not in the stopwords) from the text provided.

        text -- The text to be searched
        case_sensitive -- Whether or not matches must be case-sensitive (requires provided dictionary
        to be case-sensitive as well.)
        """
        
        extracts = []

        if timing:
            t1 = time.time()

        try:
            text = remove_accents(unicode(text))
        except:
            pass

        if (not case_sensitive):
            text = text.lower()

        for gram in self.ngfilter.filter(text):
            if (self.bloom and not gram in self.bloom):
                continue
            elif (gram in self.searcher and gram not in self.stopwords):
                extracts.append(gram)

        if timing:
            t2 = time.time()
            print 'extract returned in %0.3f ms' % ((t2-t1)*1000.0)

        return set(extracts)


    # Uses BS4:  ($ sudo easy_install beautifulsoup4 html5lib)
    def extract_url(self, url):
        """
        Extracts any phrases found in the dictionary (and not in the stopwords) from information in the page
        referenced by url.
        """
        import HTMLParser
        from bs4 import BeautifulSoup
        from urllib import urlopen

        h = HTMLParser.HTMLParser()
        soup = BeautifulSoup(urlopen(url).read(), "html5lib")

        results = {}
 
        title = soup.title.string
        results["title"] = self.extract(h.unescape(title))

        md = soup.find('meta', attrs={'name':re.compile("^description$", re.I)})
        results["meta-description"] = self.extract(h.unescape(md['content'])) if md and md.has_key('content') else None

        mk = soup.find('meta', attrs={'name':re.compile("^keywords$", re.I)})
        results["meta-keywords"] = self.extract(h.unescape(mk['content'])) if mk and mk.has_key('content') else None

        ot = soup.find('meta', attrs={'property':re.compile("^og:title$", re.I)})
        results["og:title"] = self.extract(h.unescape(ot['content'])) if ot and ot.has_key('content') else None

        od = soup.find("meta", attrs={'property':re.compile("^og:description$", re.I)})
        results["og:description"] = self.extract(h.unescape(od['value'])) if od and od.has_key('value') else None

        return results



def main():
    e = Extractor(3, '../data/dictionary.txt', '../data/stopwords.txt', True, True)
    print e.extract('The Band played on the waterfront')
    print e.extract('Fanta Orange is the Chess Club soda fountain favorite')
    print e.extract('the baby sitting Bull jumped over the Crazy Horse')
    print e.extract_url('http://www.theatlantic.com/technology/archive/12/06/hey-brother-can-you-spare-a-hubble-dod-sure-have-two/258061/')
    print e.extract_url('http://money.cnn.com/2012/06/04/technology/groupon-stock-6-billion/index.htm')
    print e.extract_url('http://www.chateau-st-martin.com')
    print e.extract_url('http://www.foodandwine.com/articles/rose-underrated-or-overhyped')

if __name__ == "__main__":
    main()
