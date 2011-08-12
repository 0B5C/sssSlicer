import hashlib
class Crypto:
    def shaHashing(self, hashMe ):
        return hashlib.sha512(hashMe).hexdigest()