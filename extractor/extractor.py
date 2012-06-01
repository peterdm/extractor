import time
from bloomfilter import BloomFilter
from ngramfilter import NGramFilter
from searcher import Searcher

# ask for string, filter for ngrams, for each ngram, collect if bf && searcher, return collection

class Extractor:
    BF_HASHES  = 5
    BF_BYTES   = 8192 * 1024  # 8MB

    def __init__(self, max_gram_size, dictionary_file, use_bloomfilter=False):
        self.ngfilter = NGramFilter(max_gram_size)
        self.searcher = Searcher(dictionary_file)
        if use_bloomfilter:
            f = open(dictionary_file)
            self.bloom = BloomFilter(self.BF_BYTES, self.BF_HASHES, iter(f))
        else:
            self.bloom = None
    

    def extract(self, text, case_sensitive=False):
        extracts = []

	t1 = time.time()

        if (not case_sensitive):
            text = text.lower()

        for gram in self.ngfilter.filter(text):
            if (self.bloom and not gram in self.bloom):
                continue
            elif (gram in self.searcher):
                extracts.append(gram)

        t2 = time.time()
        print 'extract returned in %0.3f ms' % ((t2-t1)*1000.0)
       
        return set(extracts)



def main():
    e = Extractor(3, '../output/dictionary.txt', True)
    print e.extract('The Band played on the waterfront')
    print e.extract('Fanta Orange is the Chess Club soda fountain favorite')
    print e.extract('the baby sitting Bull jumped over the Crazy Horse')

if __name__ == "__main__":
    main()
