import hashlib

a = 'abcd'
a_hash = hashlib.sha256(a.encode()).hexdigest()
print(a_hash)
print(len(a_hash))


def get_block_hash(block):
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = sorted(block['transaction']['data'].copy().items())
    data = sorted(data.items())
    return hashlib.sha256(str(data).encode()).hexdigest()



