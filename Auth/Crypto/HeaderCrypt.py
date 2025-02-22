import hmac
from hashlib import sha1


class HeaderCrypt(object):

    ENCRYPT_HEADER_SIZE = 4
    DECRYPT_HEADER_SIZE = 6

    def __init__(self, session_key: bytes):
        self.crypt_key = self._generate_key(session_key)
        self.send_i = 0
        self.send_j = 0
        self.recv_i = 0
        self.recv_j = 0

    def encrypt(self, data: bytes):
        assert len(data) >= self.ENCRYPT_HEADER_SIZE
        encrypted_header = [0] * self.ENCRYPT_HEADER_SIZE

        for index in range(self.ENCRYPT_HEADER_SIZE):
            self.send_i %= len(self.crypt_key)
            enc = (data[index] ^ self.crypt_key[self.send_i]) + self.send_j
            enc %= 0x100
            self.send_i += 1
            encrypted_header[index] = self.send_j = enc

        return bytes(encrypted_header) + data[self.ENCRYPT_HEADER_SIZE:]

    def decrypt(self, data: bytes):
        assert len(data) >= self.DECRYPT_HEADER_SIZE
        decrypted_header = [0] * self.DECRYPT_HEADER_SIZE

        for index in range(self.DECRYPT_HEADER_SIZE):
            self.recv_i %= len(self.crypt_key)
            dec = (data[index] - self.recv_j) ^ self.crypt_key[self.recv_i]
            dec %= 0x100
            self.recv_i += 1
            self.recv_j = data[index]
            decrypted_header[index] = dec

        return bytes(decrypted_header) + data[self.DECRYPT_HEADER_SIZE:]

    def _generate_key(self, session_key):
        # according to Mangos this is static hash
        seed = b'8\xa7\x83\x15\xf8\x92%0q\x98g\xb1\x8c\x04\xe2\xaa'
        hashed = hmac.new(seed, session_key, sha1)
        return hashed.digest()
