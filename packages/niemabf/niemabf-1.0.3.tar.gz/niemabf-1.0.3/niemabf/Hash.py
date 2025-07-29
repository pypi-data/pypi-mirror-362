# non-standard imports
from mmh3 import hash as mmh3_hash

def mmh3_hash_niemabf(key, seed):
    '''
    NiemaBF wrapper for `mmh3.hash`, which returns a signed `int` by default (we want unsigned)

    Args:
        key (str): The input string to hash
        seed (int): The seed value of the hash function

    Returns:
        int: The hash value
    '''
    return mmh3_hash(key=key, seed=seed, signed=False)

def mmh3_hash_niemabf_int(key, seed):
    '''
    NiemaBF wrapper to compute mmh3.hash on an `int` by converting it to `str` first

    Args:
        key (int): The input `int` to hash
        seed (int): The seed value of the hash function

    Returns:
        int: The hash value
    '''
    return mmh3_hash_niemabf(str(key), seed)

def mmh3_hash_niemabf_iterable(key, seed):
    '''
    NiemaBF wrapper to compute mmh3.hash on iterable data

    Args:
        key (iterable): The input iterable data to hash
        seed (int): The seed value of he hash function

    Returns:
        int: The hash value
    '''
    return mmh3_hash_niemabf(''.join(str(HASH_FUNCTIONS[DEFAULT_HASH_FUNCTION[type(x)]](x,seed)) for x in key), seed)

# hash functions
HASH_FUNCTIONS = {
    'mmh3': mmh3_hash_niemabf,                   # https://mmh3.readthedocs.io/en/stable/api.html#mmh3.hash
    'mmh3_int': mmh3_hash_niemabf_int,           # convert int to bytes, and then use mmh3
    'mmh3_iterable': mmh3_hash_niemabf_iterable, # use mmh3 on each element in an iterable
}

# default hash function for each type
DEFAULT_HASH_FUNCTION = {
    int:  'mmh3_int',
    list: 'mmh3_iterable',
    set:  'mmh3_iterable',
    str:  'mmh3',
}
