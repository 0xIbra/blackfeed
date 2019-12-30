from hashlib import md5

def hashit(content):
    return md5(content).hexdigest()