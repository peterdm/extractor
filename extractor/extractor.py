import bloomfilter
import ngramfilter
import searcher

# ask for string, filter for ngrams, for each ngram, collect if bf && searcher, return collection

class Extractor:
    BF_HASHES  = 5
    BF_BYTES   = 512 * 1024  # 512kb 

    def __init__(self, max_gram_size, dictionary_file, use_bloomfilter=False):
        self.ngfilter = NGramFilter(max_gram_size)
        self.searcher = Searcher(dictionary_file)
        if use_bloomfilter:
            f = open(dictionary_file)
            self.bloom = BloomFilter(self.BF_BYTES, self.BF_HASHES, iter(f))
        else:
            self.bloom = None

    def extract(self, text):
        extracts = []
        for gram in self.ngfilter.filter(text):
            if (self.bloom and not gram in self.bloom):
                continue
            elif (gram in self.searcher):
                extracts.append(gram)
        return set(extracts)
