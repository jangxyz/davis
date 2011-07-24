#!/usr/bin/python


def encode_data(data):
    ''' convert data object to encoded string

    >>> encode_data([2,5,6])
    '1 2\n2 5\n3 6'
    >>> encode_data([(1,2), (2,5), (3,6)])
    '1 2\n2 5\n3 6'
    '''
    if isinstance(data[0], (int,basestring)):
        x = range(1, len(data)+1)
        data = zip(x, data)
    return "\n".join([str(x)+" "+str(y) for x,y in data])


def decode_data(datastr):
    ''' convert data string into list of tuples
    
    #>>> decode_data('1 2\n2 5\n3 6')
    #[(1,2), (2,5), (3,6)]
    '''
    return [tuple(line.split(" ")) for line in datastr.strip().split("\n")]

def normalize_data(data):
    return decode_data(encode_data(data))


if __name__ == '__main__':
    import doctest
    doctest.testmod()



# vim: sts=4 et
