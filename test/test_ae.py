import ctypes
import random

# Path to the compiled 32-bit DLL
dll_path = r"D:\secure_sys\rijndael starter code\rijndael.dll"
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
    plaintext = bytes([0x32, 0x88, 0x31, 0xe0, 0x43, 0x5a, 0x31, 0x37,
                       0xf6, 0x30, 0x98, 0x07, 0xa8, 0x8d, 0xa2, 0x34])
    key = bytes([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                 0x24, 0x7b, 0x6b, 0x3b, 0x61, 0x0c, 0xd0, 0x3c])
    
    expected_ciphertext = bytes([0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb,
                                  0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32])

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