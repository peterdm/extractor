"""
Split a query into word n-grams
"""
SINGLE_QUOTE_MAP = {
        0x2018: 39,
        0x2019: 39,
        0x201A: 39,
        0x201B: 39,
        0x2039: 39,
        0x203A: 39,
}

DOUBLE_QUOTE_MAP = {
        0x00AB: 34,
        0x00BB: 34,
        0x201C: 34,
        0x201D: 34,
        0x201E: 34,
        0x201F: 34,
}

def convert_smart_quotes(str):
        return str.translate(DOUBLE_QUOTE_MAP).translate(SINGLE_QUOTE_MAP)


class NGramFilter:
    
    def __init__(self, maxgram):
        """
        maxgram -- the longest number of words allowed in an ordered permutation
        """
        self.maxgram = maxgram

    
    def generate(self, query):
        """
        query -- the phrase to split into n-grams
        """
        query = query.replace('-',' ') # (e.g. "Japanese-inspired") TODO: Copy out the token variation
        splits = query.split(' ')
        terms = []
        for t in splits: # trim any  commas, periods, etc..
            if t is not None:
                try:
                    t = unicode(t)
                    t = convert_smart_quotes(t)
                    t = t.strip(",.\'<>!?() ")
                    terms.append(t)
                except:
                    pass
        
        phrases = []
        for head in range(0,len(terms)):
            newterm = []
            for tail in range(head, len(terms)):
                newterm.append(terms[tail])
                phrases.append(' '.join(newterm))
                if len(newterm) == self.maxgram:
                    break
        return phrases

    
    def filter(self, query):
        """
        Filter is a convenience method.  It returns an iterator over the n-grams for the query provided.
        """
        return iter(self.generate(query))
            
            
