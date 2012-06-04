import math
import os.path
from random import Random

class BloomFilter:
    """
    http://en.wikipedia.org/wiki/Bloom_filter

    A Bloom Filter provides a fast, low-memory mechanism to check for the likely existance of a
    string in a large dictionary of strings.  Each value in the dictionary is hashed into a BitSet
    (like a hashtable, except that the actual value isn't stored, just the hash key).

    Also like a hashtable, there is a potential for collisions, but without the actual stored values 
    present, there is no way to determine whether the value being tested actually exists in the 
    dictionary, or simply another value with the same hash.

    These collisions allow for false positives, but not false negatives.  For this reason, all positives
    returned from a Bloom Filter should be checked against the actual dictionary.

    To reduce the number of false positives (caused by collisions), the range of permissible hash-values
    may be increased (num_bytes), additionally each value can be hashed multiple times (num_probes).

    Constructing this bitset with a ~10MM entry dictionary takes several minutes, so DATAFILE was
    introduced to persist the final bitset to disk for a quick startup (once the bitset is built)
    """

    DATAFILE = '../data/bf.dat'


    def __init__(self, num_bytes, num_probes, iterable=()):
        """
        num_bytes -- The size/range of the memory allocated for hash-keys
        num_probes -- The number of hash functions used
        iterable -- The dictionary to use (should be a sorted file)
        """
        self.num_probes = num_probes
        self.num_bins = num_bytes * 8

        if os.path.exists(self.DATAFILE):
            self.load(self.DATAFILE)
        else:
            self.array = bytearray(num_bytes)
            self.update(iterable, self.DATAFILE)

    def get_probes(self, key):
        random = Random(key).random
        return (int(random() * self.num_bins) for _ in range(self.num_probes))

    def load(self, datafile):
        with open(datafile, 'rb') as f:
            self.array = bytearray(f.read())

    def save(self, datafile):
        with open(datafile, 'wb') as f:
            f.write(self.array)

    def update(self, keys, datafile):
        """
        Called to regenerate the BloomFilter bitset
        keys -- The dictionary entries
        datafile -- Where to persist the bitset when finalized
        """
        count = 0
        for key in keys:
            count = count + 1
            for i in self.get_probes(key.strip()):
                self.array[i//8] |= 2 ** (i%8)

        self.save(datafile)

        fp_rate = (1 - math.exp(-self.num_probes*(count+0.5) / (self.num_bins - 1))) ** self.num_probes 
        print 'BF: Indexed %(#)d items.  False positive rate is %(pct).2f pct' % { '#':count, 'pct': round(fp_rate*100,2) }


    def __contains__(self, key):
        """
        Convenience magic method for testing likely membership of a term in the dictionary
        Usage:  if (term in bloomfilter_instance):
                    print term
        """
        return all(self.array[i//8] & (2 ** (i%8)) for i in self.get_probes(key.strip()))
