# non-standard imports
from numpy import uint8, zeros

# useful constants
UINT8_0 = uint8(0)
UINT8_1 = uint8(1)

class BitArray:
    '''Bit Array class'''
    def __init__(self, m):
        '''
        Initialize a new Bit Array

        Args:
            m (int): The number of bits to use in this Bit Array (must be multiple of 8)
        '''
        if not isinstance(m, int):
            raise TypeError("`m` must be type `int`, but received: `%s`" % type(m))
        if (m < 8) or ((m % 8) != 0):
            raise ValueError("`m` must be a positive multiple of 8, but received: %s" % m)
        self.m = m
        self.arr = zeros(self.m // 8, dtype=uint8, order='C')

    def __len__(self):
        '''
        Return the length (in bits) of this Bit Array

        Returns:
            int: The length (in bits) of this Bit Array
        '''
        return self.m

    def __str__(self):
        '''
        Return the string representation of this Bit Array

        Returns:
            str: The string representation of this Bit Array
        '''
        return ' '.join(format(v, 'b').zfill(8) for v in self.arr)

    def __getitem__(self, i):
        '''
        Return the value of the `i`-th bit

        Args:
            i (int): The index of the bit whose value to return

        Returns:
            int: The value of the `i`-th bit (1 or 0)
        '''
        return (self.arr[i // 8] >> (7 - (i % 8))) & UINT8_1

    def __setitem__(self, i, v):
        '''
        Set the value of the `i`-th bit

        Args:
            i (int): The index of the bit whose value to set
            v (int): The value to set the `i`-th bit (1 or 0)
        '''
        arr_ind = i // 8; offset = 7 - (i % 8)
        self.arr[arr_ind] = (self.arr[arr_ind] & (~(UINT8_1 << offset))) | ((v != 0) << offset)
