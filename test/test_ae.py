import os
import ctypes
import pytest
from Crypto.Cipher import AES as PyAES

# Load DLL
dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../rijndael.dll'))
lib = ctypes.CDLL(dll_path)

# Set function signatures
lib.aes_encrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
lib.aes_encrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)

lib.aes_decrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
lib.aes_decrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)

# Helpers
def ptr_to_bytes(ptr, length=16):
    return bytes((ptr[i] for i in range(length)))

def make_buffers():
    data = os.urandom(16)
    buf = (ctypes.c_ubyte * 16)(*data)  # Create a c_ubyte array
    original = bytes(buf)
    return buf, original

def make_key():
    key = os.urandom(16)
    return (ctypes.c_ubyte * 16)(*key), key  # Create a c_ubyte array for the key

def to_c_buffer(block):
    return (ctypes.c_ubyte * 16)(*block)

# Tests

def test_known_vector():
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    plaintext = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
    expected_ciphertext = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")

    pt_buf = to_c_buffer(plaintext)
    key_buf = to_c_buffer(key)

    cipher_ptr = lib.aes_encrypt_block(pt_buf, key_buf)
    actual_cipher = ptr_to_bytes(cipher_ptr)

    assert actual_cipher == expected_ciphertext, f"Expected {expected_ciphertext.hex()} but got {actual_cipher.hex()}"

    # Decrypt and check
    ct_buf = to_c_buffer(actual_cipher)
    plain_ptr = lib.aes_decrypt_block(ct_buf, key_buf)
    decrypted = ptr_to_bytes(plain_ptr)

    assert decrypted == plaintext, "Decryption does not match original plaintext"

@pytest.mark.parametrize("i", range(3))
def test_random_encrypt_decrypt(i):
    buf, original = make_buffers()
    key_buf, key_raw = make_key()

    # Encrypt
    enc_ptr = lib.aes_encrypt_block(buf, key_buf)
    cipher = ptr_to_bytes(enc_ptr)

    # Decrypt
    ct_buf = to_c_buffer(cipher)
    dec_ptr = lib.aes_decrypt_block(ct_buf, key_buf)
    decrypted = ptr_to_bytes(dec_ptr)

    assert decrypted == original, "Decrypted block doesn't match original"

def test_compare_with_pycryptodome():
    buf, original = make_buffers()
    key_buf, key_raw = make_key()

    # DLL Encrypt
    enc_ptr = lib.aes_encrypt_block(buf, key_buf)
    c_cipher = ptr_to_bytes(enc_ptr)

    # Python Encrypt
    py_cipher = PyAES.new(key_raw, PyAES.MODE_ECB).encrypt(original)

    assert c_cipher == py_cipher, "C DLL encryption and Python encryption do not match"