"""
Split a query into word n-grams
"""
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
        query = query.replace(',', ' ')
        terms = query.split(' ')
	for t in range(0, len(terms)): # trim any  commas, periods, etc..
            terms[t] = terms[t].strip(",.\'<>!?() ")

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

            
