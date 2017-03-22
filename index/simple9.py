_payload = [(1, 28), (2, 14), (3, 9), (4, 7), (5, 5), (7, 4), (9, 3), (14, 2), (28, 1)]


def _encode(c, nums):
    sz, bits = _payload[c]
    rv = c << 28
    assert len(nums) <= sz
    for i, n in enumerate(nums):
        x = n << bits * (sz - i - 1)
        rv |= x
    return rv


def _decode(num):
    c = num >> 28
    sz, bits = _payload[c]
    rv = []
    for i in range(sz):
        mask = (1 << ((sz - i) * bits)) - 1
        num &= mask
        x = num >> ((sz - 1 - i) * bits)
        rv.append(x)
    return rv


def _bits_for_num(x):
    for _, count in reversed(_payload):
        if x < 2 ** count:
            return count
    return None


def _compress_head(nums):
    for i, (bits, sz) in enumerate(_payload):
        cls = len(_payload) - 1 - i
        head = nums[:sz]
        if all([_bits_for_num(x) <= bits for x in head]):
            return _encode(cls, head), sz
    return None


def encode_arr(nums):
    cp = nums[:]
    rv = []
    while len(cp) > 0:
        x, offset = _compress_head(cp)
        rv.append(x)
        cp = cp[offset:]
    return rv


def decode_arr(arr):
    return sum(map(lambda x: _decode(x), arr), [])
