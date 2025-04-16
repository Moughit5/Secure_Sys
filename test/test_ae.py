import ctypes
import os
import random

# Load compiled C library (assumes rijndael.so was built)
rijndael = ctypes.CDLL(os.path.abspath("./rijndael.so"))

# Define ctypes argument and return types
rijndael.aes_encrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
rijndael.aes_encrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)

rijndael.aes_decrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
rijndael.aes_decrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)


def random_block():
    return bytes([random.randint(0, 255) for _ in range(16)])

def test_encrypt_decrypt():
    for _ in range(3):
        plaintext = random_block()
        key = random_block()

        pt_buf = (ctypes.c_ubyte * 16)(*plaintext)
        key_buf = (ctypes.c_ubyte * 16)(*key)

        cipher_ptr = rijndael.aes_encrypt_block(pt_buf, key_buf)
        cipher = ctypes.string_at(cipher_ptr, 16)

        decrypt_ptr = rijndael.aes_decrypt_block((ctypes.c_ubyte * 16).from_buffer_copy(cipher), key_buf)
        decrypted = ctypes.string_at(decrypt_ptr, 16)

        print("Plaintext :", plaintext.hex())
        print("Key       :", key.hex())
        print("Cipher    :", cipher.hex())
        print("Decrypted :", decrypted.hex())

        assert decrypted == plaintext, "Decryption failed"

if __name__ == "__main__":
    test_encrypt_decrypt()
