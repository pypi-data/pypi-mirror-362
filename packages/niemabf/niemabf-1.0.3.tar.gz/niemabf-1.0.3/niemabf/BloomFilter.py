# NiemaBF imports
from niemabf.BitArray import BitArray
from niemabf.common import open_file, NIEMABF_VERSION
from niemabf.Hash import HASH_FUNCTIONS

# standard imports
from pickle import dump as pdump, load as pload

# useful constants
DUMP_KEYS = ['niemabf_version', 'k', 'bits', 'hash_func_key', 'num_inserts']

class BloomFilter:
    '''Bloom Filter class'''
    def __init__(self, k, m, hash_func='mmh3'):
        '''
        Initialize a new Bloom Filter

        Args:
            k (int): The number of hash functions to use in this Bloom Filter (must be positive)
            m (int): The number of bits to use in this Bloom Filter (must be multiple of 8)
            hash_func (str): The hash function to use in this Bloom Filter
        '''
        if not isinstance(k, int):
            raise TypeError("`k` must be type `int`, but received: `%s`" % type(k))
        if k < 1:
            raise ValueError("`k` must be positive, but received: %s" % k)
        if hash_func not in HASH_FUNCTIONS:
            raise ValueError("Invalid hash function (%s). Options: %s" % (hash_func, ', '.join(sorted(HASH_FUNCTIONS.keys()))))
        self.niemabf_version = NIEMABF_VERSION
        self.k = k
        self.m = m
        self.bits = BitArray(m)
        self.hash_func_key = hash_func
        self.hash_func = HASH_FUNCTIONS[hash_func]
        self.num_inserts = 0

    def __len__(self):
        '''
        Return the total number of insert operations into this Bloom Filter (duplicate inserts will be double-counted)

        Returns:
            int: The total number of insert operations into this Bloom Filter
        '''
        return self.num_inserts

    def __getstate__(self):
        '''
        Get the state (core instance variables) of this Bloom Filter

        Returns:
            dict: The state (core instance variables) of this Bloom Filter
        '''
        state = dict()
        for k in DUMP_KEYS:
            state[k] = getattr(self, k)
        return state

    def insert(self, x):
        '''
        Insert an element into this Bloom Filter

        Args:
            x (object): The element to insert
        '''
        self.num_inserts += 1
        for i in range(self.k):
            self.bits[self.hash_func(x, i) % self.m] = 1

    def find(self, x):
        '''
        Find an element in this Bloom Filter

        Args:
            x (object): The element to find

        Returns:
            bool: `False` if `x` definitely does not exist in this Bloom Filter, otherwise `True`
        '''
        for i in range(self.k):
            if self.bits[self.hash_func(x, i) % self.m] == 0:
                return False
        return True

    def dump(self, fn):
        '''
        Dump this Bloom Filter into a given file

        Args:
            fn (str): The name of the file into which this Bloom Filter should be dumped
        '''
        with open_file(fn, mode='wb') as f:
            pdump(self, f)

    def load(fn):
        '''
        Load a Bloom Filter from a given file

        Args:
            fn (str): The name of the file from which to load a Bloom Filter

        Returns:
            BloomFilter: The loaded Bloom Filter
        '''
        with open_file(fn, mode='rb') as f:
            bf = pload(f)
        bf.m = len(bf.bits)
        bf.hash_func = HASH_FUNCTIONS[bf.hash_func_key]
        return bf
