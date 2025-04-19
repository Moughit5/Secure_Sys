from Crypto.Cipher import AES

def test_aes_vector():
    # FIPS-197 Appendix B Test Vector
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")  # 128-bit key
    plaintext = bytes.fromhex("3243f6a8885a308d313198a2e0370734")  # Column-major ordered block

    expected_ciphertext = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")

    cipher = AES.new(key, AES.MODE_ECB)
    actual_ciphertext = cipher.encrypt(plaintext)

    print("Expected Ciphertext:", expected_ciphertext.hex())
    print("Actual Ciphertext  :", actual_ciphertext.hex())

    assert actual_ciphertext == expected_ciphertext, "Mismatch in ciphertext!"

if __name__ == "__main__":
    test_aes_vector()
