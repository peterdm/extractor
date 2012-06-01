import math
import os.path
from random import Random

class BloomFilter:
    # http://en.wikipedia.org/wiki/Bloom_filter
    DATAFILE = '../data/bf.dat'


    def __init__(self, num_bytes, num_probes, iterable=()):
        self.num_probes = num_probes
        self.num_bins = num_bytes * 8

        if os.path.exists(self.DATAFILE):
            self.load(self.DATAFILE)
        else:
            self.array = bytearray(num_bytes)
            self.update(iterable)
            self.save(self.DATAFILE)

    def get_probes(self, key):
        random = Random(key).random
        return (int(random() * self.num_bins) for _ in range(self.num_probes))

    def load(self, datafile):
        with open(datafile, 'rb') as f:
            self.array = bytearray(f.read())

    def save(self, datafile):
        with open(datafile, 'wb') as f:
            f.write(self.array)

    def update(self, keys):
        count = 0
        for key in keys:
            count = count + 1
            for i in self.get_probes(key.strip()):
                self.array[i//8] |= 2 ** (i%8)

        fp_rate = (1 - math.exp(-self.num_probes*(count+0.5) / (self.num_bins - 1))) ** self.num_probes 
        print 'BF: Indexed %(#)d items.  False positive rate is %(pct).2f pct' % { '#':count, 'pct': round(fp_rate*100,2) }

    def __contains__(self, key):
        return all(self.array[i//8] & (2 ** (i%8)) for i in self.get_probes(key.strip()))
