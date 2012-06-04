import time
from bloomfilter import BloomFilter
from ngramfilter import NGramFilter
from searcher import Searcher
from strip_accent import remove_accents

# ask for string, filter for ngrams, for each ngram, collect if bf && searcher, return collection

class Extractor:
    BF_HASHES  = 5
    BF_BYTES   = 8192 * 1024  # 8MB

    def __init__(self, max_gram_size, dictionary_file, stopwords_file, use_bloomfilter=False):
        self.ngfilter = NGramFilter(max_gram_size)
        self.searcher = Searcher(dictionary_file)
	self.stopwords = Searcher(stopwords_file)
        if use_bloomfilter:
            f = open(dictionary_file)
            self.bloom = BloomFilter(self.BF_BYTES, self.BF_HASHES, iter(f))
        else:
            self.bloom = None
    

    def extract(self, text, case_sensitive=False):
        extracts = []

	t1 = time.time()

        text = remove_accents(unicode(text))

        if (not case_sensitive):
            text = text.lower()

        for gram in self.ngfilter.filter(text):
            if (self.bloom and not gram in self.bloom):
                continue
            elif (gram in self.searcher and gram not in self.stopwords):
                extracts.append(gram)

        t2 = time.time()
        print 'extract returned in %0.3f ms' % ((t2-t1)*1000.0)

        return set(extracts)


    # Uses BS4:  ($ sudo easy_install beautifulsoup4 html5lib)
    def extract_url(self, url, taglist=['title', 'meta.keywords', 'og:title', 'og:description'] ):
        from bs4 import BeautifulSoup, SoupStrainer
        from urllib import urlopen

        only_head = SoupStrainer("head")
        soup = BeautifulSoup(urlopen(url).read(), "html5lib", parse_only=only_head)

        results = {}

 
        title = soup.title.string
        results["title"] = self.extract(title)

        md = soup.find("meta", attrs={"name":"description"})
        results["meta-description"] = self.extract(md['content']) if md and md.has_key('content') else None

        mk = soup.find("meta", attrs={"name":"keywords"})
        results["meta-keywords"] = self.extract(mk['content']) if mk and mk.has_key('content') else None

        ot = soup.find("meta", attrs={"property":"og:title"})
        results["og:title"] = self.extract(ot['content']) if ot and ot.has_key('content') else None

        od = soup.find("meta", attrs={"property":"og:description"})
        results["og:description"] = self.extract(od['value']) if od and od.has_key('value') else None

        return results


def main():
    e = Extractor(3, '../data/dictionary.txt', '../data/stopwords.txt', True)
    print e.extract('The Band played on the waterfront')
    print e.extract('Fanta Orange is the Chess Club soda fountain favorite')
    print e.extract('the baby sitting Bull jumped over the Crazy Horse')
    print e.extract_url('http://www.theatlantic.com/technology/archive/12/06/hey-brother-can-you-spare-a-hubble-dod-sure-have-two/258061/')
    print e.extract_url('http://money.cnn.com/2012/06/04/technology/groupon-stock-6-billion/index.htm')


if __name__ == "__main__":
    main()
