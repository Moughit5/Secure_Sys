import ctypes
import random
import os

# Use a relative path to the compiled DLL
dll_path = os.path.join(os.path.dirname(__file__), '../rijndael.dll')
rijndael = ctypes.CDLL(dll_path)

# Define argument and return types for AES functions
rijndael.aes_encrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
rijndael.aes_encrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)

rijndael.aes_decrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
rijndael.aes_decrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)

def random_block():
    """Generate a random 16-byte block."""
    return bytes([random.randint(0, 255) for _ in range(16)])

def test_full_aes():
    """Test AES encryption and decryption with random plaintext and keys."""
    for i in range(3):
        plaintext = random_block()
        key = random_block()

        pt_buf = (ctypes.c_ubyte * 16)(*plaintext)
        key_buf = (ctypes.c_ubyte * 16)(*key)

        # Encrypt the plaintext
        cipher_ptr = rijndael.aes_encrypt_block(pt_buf, key_buf)
        cipher = ctypes.string_at(cipher_ptr, 16)

        # Decrypt the ciphertext
        ct_buf = (ctypes.c_ubyte * 16).from_buffer_copy(cipher)
        plain_ptr = rijndael.aes_decrypt_block(ct_buf, key_buf)
        decrypted = ctypes.string_at(plain_ptr, 16)

        print(f"Test {i+1}")
        print("Plaintext :", plaintext.hex())
        print("Key       :", key.hex())
        print("Cipher    :", cipher.hex())
        print("Decrypted :", decrypted.hex())

        assert decrypted == plaintext, "Decryption does not match original!"

def test_known_values():
    """Test AES encryption and decryption with known values."""
    plaintext = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    expected_ciphertext = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")

    pt_buf = (ctypes.c_ubyte * 16)(*plaintext)
    key_buf = (ctypes.c_ubyte * 16)(*key)

    # Encrypt the plaintext
    cipher_ptr = rijndael.aes_encrypt_block(pt_buf, key_buf)
    cipher = ctypes.string_at(cipher_ptr, 16)

    print("Expected Ciphertext:", expected_ciphertext.hex())
    print("Actual Ciphertext  :", cipher.hex())

    assert cipher == expected_ciphertext, "Encryption does not match expected ciphertext!"

    # Decrypt the ciphertext
    ct_buf = (ctypes.c_ubyte * 16).from_buffer_copy(cipher)
    plain_ptr = rijndael.aes_decrypt_block(ct_buf, key_buf)
    decrypted = ctypes.string_at(plain_ptr, 16)

    print("Decrypted Plaintext:", decrypted.hex())
    assert decrypted == plaintext, "Decryption does not match original!"

if __name__ == "__main__":
    test_known_values()  # Test with known values
    test_full_aes()      # Test with random values