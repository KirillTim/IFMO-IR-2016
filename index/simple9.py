payload = [(1, 28), (2, 14), (3, 9), (4, 7), (5, 5), (7, 4), (9, 3), (14, 2), (28, 1)]


def encode(c, nums):
    sz, bits = payload[c]
    rv = c << 28
    assert len(nums) <= sz
    for i, n in enumerate(nums):
        x = n << bits * (sz - i - 1)
        rv |= x
    return rv


def decode(num):
    c = num >> 28
    sz, bits = payload[c]
    rv = []
    for i in range(sz):
        mask = (1 << ((sz - i) * bits)) - 1
        num &= mask
        x = num >> ((sz - 1 - i) * bits)
        rv.append(x)
    return rv