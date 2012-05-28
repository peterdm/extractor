# Split a query into word n-grams

class NGramFilter:
    def __init__(self, maxgram):
        self.maxgram = maxgram

    def generate(self, query):
        terms = query.split(' ')
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
        return iter(self.generate(query))

            
